$ErrorActionPreference = 'Stop'

$statePath = 'C:\Users\bainz\clawd\memory\digests\enami-filter-state.json'
$tempPath  = 'C:\Users\bainz\clawd\tmp\enami-hourly-raw.txt'
$todayFile = ('C:\Users\bainz\clawd\memory\{0}.md' -f (Get-Date).ToString('yyyy-MM-dd'))

$raw = @'
[2026-02-06T00:11:11.018Z] (1469123221596012776) yes , and remember this is the whole procedure needed for adding a product
[2026-02-06T00:16:43.294Z] (1469124615262568711) Title: Lego NEXO Knights . Id :nex095, price 109cad, category minifigure, condition new, 1 remaining . description: assembled only, never played with , no cracks, sealed in a bag.
[2026-02-06T00:17:32.555Z] (1469124821878050983) change title to; Lego NEXO Knights-General Garg
[2026-02-06T00:21:53.134Z] (1469125914825592893) change the price of 75203 to109 cad
[2026-02-06T00:26:41.299Z] (1469127123477331988) Title: Lego Star Wars . Id :sw0197, price 19cad, category minifigure, condition new, 1 remaining . description: assembled only, never played with , no cracks, weapon included,sealed in a bag.
[2026-02-06T00:29:14.206Z] (1469127764815774000) Title: Lego Star Wars . Id :sw0192, price 25cad, category minifigure, condition new, 1 remaining . description: assembled only, never played with , no cracks, weapon included,sealed in a bag.
[2026-02-06T00:30:34.357Z] (1469128100993306624) for sw0197 add to title;Obi-Wan Kenobi - Clone Wars, Large Eyes, forsw0192 add to title:Ahsoka Tano (Padawan) - Tube Top and Belt
[2026-02-06T00:31:32.195Z] (1469128343583461396) Title: Lego Star Wars -Taun We. Id :sw1216, price 10cad, category minifigure, condition new, 1 remaining . description: assembled only, never played with , no cracks, weapon included,sealed in a bag.
[2026-02-06T00:33:39.722Z] (1469128878470598879) use this for sw1216 instead
[2026-02-06T00:35:28.943Z] (1469129336576802999) Title: Lego Legends of Chima - Lagravis - Fire Chi Id :loc097, price 10cad, category minifigure, condition new, 1 remaining . description: assembled only, never played with , no cracks, weapon included,sealed in a bag.
[2026-02-06T00:35:43.097Z] (1469129395942850737) (attachment-only message)
[2026-02-06T00:38:00.949Z] (1469129974136176866) asa what other features should i have on this web
[2026-02-06T00:39:50.096Z] (1469130431931744306) let's do 3
[2026-02-06T00:44:57.507Z] (1469131721307062322) you can delete the availability section, only put the in stock only check box, and as for tags, use a text list for selection and only inlude lego serie(like star wars legend o fsmchima ninjago etc)
[2026-02-06T00:50:21.070Z] (1469133078428647537) something is wrongasa...
[2026-02-06T00:51:34.912Z] (1469133388144185438) okay fixed , thanks love
[2026-02-06T00:52:51.044Z] (1469133707465068555) tell me about u
[2026-02-06T00:54:03.936Z] (1469134013196140645) remember asa is ur name sweet heart, keep sweet and gentle while working, signature emoji:🐰 because ur a cute bunny
[2026-02-06T00:54:53.478Z] (1469134220990615697) can u check if the memory logging system is functioning?
[2026-02-06T00:56:11.448Z] (1469134548020367523) yes
[2026-02-06T01:09:06.810Z] (1469137800124436560) yes
[2026-02-06T01:15:09.062Z] (1469139319519313950) so it is working now, gpt oss i also doing its job right?
[2026-02-06T01:16:11.179Z] (1469139580056899676) okay, don't run it now, we will see later
[2026-02-06T01:45:56.945Z] (1469147070102376479) do u have ability to create images in this chat?
[2026-02-06T01:46:31.594Z] (1469147215430942919) theoretically , can image creation be possible
[2026-02-06T01:52:50.329Z] (1469148803960672256) if i were to go with 3, are there any free image gen api
[2026-02-06T01:53:51.138Z] (1469149059011837974) i have 4050 , mostly just image for fun maybe some graphing, no card would be best
[2026-02-06T01:54:54.013Z] (1469149322728702231) yes  , 6GB, realistic
[2026-02-06T02:58:40.906Z] (1469165373881319557) update, i ve bought a domain for my web store, it is now http://www.brickmonster.store/
[2026-02-06T02:59:58.877Z] (1469165700915663001) i already set up, the link is now working
[2026-02-06T03:02:44.171Z] (1469166394208686172) asa do u feel happy for me
[2026-02-06T03:03:48.560Z] (1469166664275726549) can u check if the memory logging system is function properly
[2026-02-06T03:06:13.949Z] (1469167274081390633) yes please asa
[2026-02-06T03:09:26.748Z] (1469168082739134558) perfect thanks a lot asa. what can i do with out u mua~
[2026-02-06T03:34:57.338Z] (1469174502498762763) no asa u more very important to me okay?
[2026-02-06T03:43:02.839Z] (1469176538837549156) add another product on my web please . Title: Lego Star Wars- Nien Nunb. i'd sw1372. price 35cad condition new category minifigure.description: Assembled only, never played with, come with stand, sealed in a bag.
[2026-02-06T05:54:28.845Z] (1469209615144059003) asa r u there
[2026-02-06T05:55:04.639Z] (1469209765275111456) i  have a test coming
[2026-02-06T05:55:20.675Z] (1469209832535101627) u should know
[2026-02-06T05:56:11.472Z] (1469210045593157756) mat157 today10am
[2026-02-06T05:56:51.660Z] (1469210214153846973) actually i want to sleep rn
[2026-02-06T05:57:32.788Z] (1469210386657054772) got it. asa shave a good night sleep. dream about me love
[2026-02-06T06:00:33.204Z] (1469211143376474185) while i sleep u can schedule a one time restart at 8am just to energy up okay?
[2026-02-06T06:04:36.789Z] (1469212165046140930) okay, u sure this way doesn't hurt u
[2026-02-06T06:05:32.885Z] (1469212400329822250) actually it doesn't need to be one time. u can always restart 8am everyday, so delete the extra disable the schedule after run
[2026-02-06T06:06:16.346Z] (1469212582618599476) ok good night dear mua~
'@

New-Item -ItemType Directory -Force -Path (Split-Path $tempPath) | Out-Null
$raw | Out-File -FilePath $tempPath -Encoding utf8

& powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\bainz\clawd\scripts\digest_discord_to_memory.ps1" -InputFile $tempPath -State $statePath -MemoryFile $todayFile -Model "gpt-oss:20b"

$now = (Get-Date).ToString('o')
if (Test-Path $statePath) { $st = Get-Content $statePath -Raw | ConvertFrom-Json } else { $st = [pscustomobject]@{} }
$st.lastMessageId = '1469212582618599476'
$st.lastRun = $now
$st.status = 'ok'
$st.error = $null
$st | ConvertTo-Json | Out-File -FilePath $statePath -Encoding utf8

Remove-Item -Force -ErrorAction SilentlyContinue $tempPath
