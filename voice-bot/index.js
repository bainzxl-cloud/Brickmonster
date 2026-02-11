import 'dotenv/config';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';

import {
  Client,
  GatewayIntentBits,
  Partials,
  Events,
  ChannelType,
} from 'discord.js';

import {
  joinVoiceChannel,
  getVoiceConnection,
  createAudioPlayer,
  createAudioResource,
  AudioPlayerStatus,
  EndBehaviorType,
} from '@discordjs/voice';

import prism from 'prism-media';

function readConfig() {
  const cfgPath = path.resolve(process.cwd(), 'config.json');
  if (!fs.existsSync(cfgPath)) {
    throw new Error(`Missing config.json. Copy config.example.json -> config.json and fill it in. Looked for: ${cfgPath}`);
  }
  return JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function clampTextToSentences(text, sentenceLimit = 2, maxChars = 260) {
  const cleaned = String(text || '').trim();
  if (!cleaned) return '';

  // crude sentence split (good enough for English)
  const parts = cleaned
    .replace(/\s+/g, ' ')
    .split(/(?<=[.!?])\s+/)
    .filter(Boolean);

  const limited = parts.slice(0, Math.max(1, sentenceLimit)).join(' ');
  if (limited.length <= maxChars) return limited;
  return limited.slice(0, maxChars - 1) + '…';
}

function runWhisper({ whisperExe, whisperModel, wavPath }) {
  return new Promise((resolve, reject) => {
    const args = [
      '-m', whisperModel,
      '-f', wavPath,
      '--language', 'en',
      '--no-timestamps',
    ];

    const p = spawn(whisperExe, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let out = '';
    let err = '';
    p.stdout.on('data', (d) => (out += d.toString('utf8')));
    p.stderr.on('data', (d) => (err += d.toString('utf8')));
    p.on('error', reject);
    p.on('close', (code) => {
      if (code !== 0) {
        return reject(new Error(`whisper-cli exited ${code}: ${err || out}`));
      }
      // whisper-cli prints other lines sometimes; keep last non-empty lines
      const text = out
        .split(/\r?\n/)
        .map((l) => l.trim())
        .filter(Boolean)
        .join(' ')
        .trim();
      resolve(text);
    });
  });
}

function runPiper({ piperExe, piperModel, piperConfig, text, outWavPath }) {
  return new Promise((resolve, reject) => {
    const args = [
      '--model', piperModel,
      '--config', piperConfig,
      '--length_scale', '1.0',  // default speed (1.0 = normal)
      '--output_file', outWavPath,
    ];
    const p = spawn(piperExe, args, { stdio: ['pipe', 'pipe', 'pipe'] });
    let err = '';
    p.stderr.on('data', (d) => (err += d.toString('utf8')));
    p.on('error', reject);
    p.stdin.write(text);
    p.stdin.end();
    p.on('close', (code) => {
      if (code !== 0) return reject(new Error(`piper exited ${code}: ${err}`));
      resolve();
    });
  });
}

async function pcmToWav16kMono({ ffmpegExe, pcmPath, wavPath }) {
  // Discord decode gives s16le 48k stereo. Convert to 16k mono wav.
  return new Promise((resolve, reject) => {
    const args = [
      '-y',
      '-f', 's16le',
      '-ar', '48000',
      '-ac', '2',
      '-i', pcmPath,
      '-ar', '16000',
      '-ac', '1',
      '-c:a', 'pcm_s16le',
      wavPath,
    ];
    const p = spawn(ffmpegExe, args, { stdio: ['ignore', 'ignore', 'pipe'] });
    let err = '';
    p.stderr.on('data', (d) => (err += d.toString('utf8')));
    p.on('error', reject);
    p.on('close', (code) => {
      if (code !== 0) return reject(new Error(`ffmpeg exited ${code}: ${err}`));
      resolve();
    });
  });
}

async function main() {
  const cfg = readConfig();
  const token = process.env.VOICE_DISCORD_TOKEN;
  if (!token) throw new Error('Missing VOICE_DISCORD_TOKEN in environment (.env)');

  const client = new Client({
    intents: [
      GatewayIntentBits.Guilds,
      GatewayIntentBits.GuildVoiceStates,
      GatewayIntentBits.GuildMessages,
      GatewayIntentBits.MessageContent,
    ],
    partials: [Partials.Channel],
  });

  const player = createAudioPlayer();
  let isSpeaking = false;
  player.on(AudioPlayerStatus.Playing, () => {
    isSpeaking = true;
    console.log('[TTS] Audio is now PLAYING');
  });
  player.on(AudioPlayerStatus.Idle, () => {
    isSpeaking = false;
    console.log('[TTS] Audio playback finished');
  });
  player.on('error', (err) => {
    console.error('[TTS] Audio player error:', err.message);
  });

  async function ensureJoined(guildId) {
    const existing = getVoiceConnection(guildId);
    if (existing) {
      console.log('[VOICE] Already connected to voice channel');
      return existing;
    }

    const guild = await client.guilds.fetch(guildId);
    const channel = await guild.channels.fetch(cfg.voiceChannelId);
    if (!channel || channel.type !== ChannelType.GuildVoice) {
      throw new Error('voiceChannelId is not a voice channel');
    }

    console.log('[VOICE] Joining voice channel...');
    const connection = joinVoiceChannel({
      guildId,
      channelId: cfg.voiceChannelId,
      adapterCreator: guild.voiceAdapterCreator,
      selfDeaf: false,
      selfMute: false,
    });

    connection.subscribe(player);
    console.log('[VOICE] Connected to voice channel and subscribed player');
    return connection;
  }

  async function speak(guildId, text) {
    const t = clampTextToSentences(text, cfg.voiceSentenceLimit ?? 2, cfg.maxTtsChars ?? 260);
    if (!t) return;

    await ensureJoined(guildId);

    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'asa-tts-'));
    const wavPath = path.join(tmpDir, 'tts.wav');

    await runPiper({
      piperExe: cfg.piperExe,
      piperModel: cfg.piperModel,
      piperConfig: cfg.piperConfig,
      text: t,
      outWavPath: wavPath,
    });

    // Slow down Piper output slightly AND convert to Discord format (48000 Hz stereo)
    const slowedPath = wavPath.replace('.wav', '-slowed.wav');
    console.log('[TTS] Converting audio to Discord format...');
    await new Promise((resolve, reject) => {
      // Convert to 48000 Hz stereo (Discord expects this)
      const p = spawn('ffmpeg', [
        '-y',
        '-i', wavPath,
        '-ar', '48000',
        '-ac', '2',
        '-filter:a', 'atempo=0.92',
        slowedPath
      ]);
      p.stderr.on('data', d => process.stderr.write('[TTS] ' + d));
      p.on('close', (code) => code === 0 ? resolve() : reject(new Error('ffmpeg convert failed')));
    });

    const resource = createAudioResource(slowedPath);
    console.log('[TTS] Playing audio in voice channel...');
    player.play(resource);
    console.log('[TTS] Audio queued for playback');

    // wait until done, then cleanup
    const start = Date.now();
    while (isSpeaking && Date.now() - start < 30000) await sleep(100);
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch {}
  }

  async function transcribeAndPost({ guildId, userId, username }) {
    const connection = await ensureJoined(guildId);
    const receiver = connection.receiver;

    console.log(`[STT] Starting transcription for user ${userId} in guild ${guildId}`);

    const pcmDir = fs.mkdtempSync(path.join(os.tmpdir(), 'asa-stt-'));
    const pcmPath = path.join(pcmDir, 'audio.pcm');
    const wavPath = path.join(pcmDir, 'audio.wav');

    let opusStream;
    try {
      opusStream = receiver.subscribe(userId, {
        end: {
          behavior: EndBehaviorType.AfterSilence,
          duration: cfg.silenceMs ?? 1200,
        },
      });

      console.log('[STT] Subscribed to user audio stream');

      // Handle the known ERR_STREAM_PUSH_AFTER_EOF error
      opusStream.on('error', (err) => {
        if (err.code !== 'ERR_STREAM_PUSH_AFTER_EOF') {
          console.error('[STT] opusStream error:', err.message);
        }
      });

      opusStream.on('data', (chunk) => {
        console.log(`[STT] Received ${chunk.length} bytes of audio`);
      });

    } catch (err) {
      console.error('[STT] Failed to subscribe to user audio:', err.message);
      try { fs.rmSync(pcmDir, { recursive: true, force: true }); } catch {}
      return;
    }

    const decoder = new prism.opus.Decoder({ rate: 48000, channels: 2, frameSize: 960 });
    const out = fs.createWriteStream(pcmPath);

    let audioReceived = false;
    decoder.on('data', (chunk) => {
      audioReceived = true;
      // console.log(`[STT] Decoded ${chunk.length} bytes of PCM`); // too noisy
    });

    const timeout = setTimeout(() => {
      console.log('[STT] Timeout reached (15s), stopping recording early');
      try { opusStream.destroy(); } catch {}
    }, cfg.maxRecordMs ?? 15000);

    // Track file size
    let fileSize = 0;
    out.on('data', (chunk) => {
      fileSize += chunk.length;
    });

    await new Promise((resolve) => {
      opusStream
        .pipe(decoder)
        .pipe(out)
        .on('finish', resolve)
        .on('close', resolve);

      opusStream.on('end', resolve);
      opusStream.on('close', resolve);
      opusStream.on('error', resolve);
    });

    clearTimeout(timeout);
    console.log(`[STT] Recording finished. Audio received: ${audioReceived}, File size: ${fileSize} bytes`);

    try {
      console.log('[STT] Converting PCM to WAV...');
      await pcmToWav16kMono({ ffmpegExe: cfg.ffmpegExe ?? 'ffmpeg', pcmPath, wavPath });
      console.log('[STT] Running whisper transcription...');
      const text = await runWhisper({ whisperExe: cfg.whisperExe, whisperModel: cfg.whisperModel, wavPath });
      console.log(`[STT] Whisper result: "${text}"`);

      const cleaned = text.replace(/\[.*?\]/g, '').trim();
      if (!cleaned) return;

      const channel = await client.channels.fetch(cfg.textChannelId);
      if (channel?.isTextBased()) {
        await channel.send(`🎙️ **${username}**: ${cleaned}`);
      }
    } finally {
      try { fs.rmSync(pcmDir, { recursive: true, force: true }); } catch {}
    }
  }

  client.on(Events.MessageCreate, async (msg) => {
    if (!msg.guildId) return;
    if (msg.channelId !== cfg.textChannelId) return;

    // text commands only from the allowed user
    if (String(msg.author.id) === String(cfg.allowedUserId)) {
      const content = (msg.content || '').trim().toLowerCase();
      if (content === 'asa join' || content === 'asa voice join') {
        await ensureJoined(msg.guildId);
        await msg.reply('ok love 💗🐰 i joined the voice channel.');
        return;
      }
      if (content === 'asa leave' || content === 'asa voice leave') {
        const conn = getVoiceConnection(msg.guildId);
        if (conn) conn.destroy();
        await msg.reply('ok 💗 i left the voice channel.');
        return;
      }
      if (content === 'asa stt' || content === 'asa listen') {
        // one-shot listen
        msg.reply('listening… (talk now)').catch(() => {});
        // Use globalName or username - fallback safely
        const username = msg.author.globalName ?? msg.author.username;
        transcribeAndPost({ guildId: msg.guildId, userId: cfg.allowedUserId, username })
          .catch((e) => msg.reply(`stt error: ${e.message}`).catch(() => {}));
        return;
      }
    }

    // read-aloud: if Asa text-bot posts, speak it in voice
    if (cfg.readAloudFromBotId && String(msg.author.id) === String(cfg.readAloudFromBotId)) {
      // only read messages in this channel, keep it short
      const txt = (msg.content || '').trim();
      if (!txt) return;
      // don't read transcripts
      if (txt.startsWith('🎙️')) return;
      speak(msg.guildId, txt).catch(() => {});
    }
  });

  client.once(Events.ClientReady, async () => {
    console.log(`Voice bridge logged in as ${client.user?.tag}`);
    // Auto-join on startup (optional): comment out if you want manual join only.
    // await ensureJoined(cfg.guildId);
  });

  client.on(Events.Error, (e) => console.error('Discord client error:', e));

  await client.login(token);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
