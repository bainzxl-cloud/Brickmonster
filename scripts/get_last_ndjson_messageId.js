const fs = require('fs');
const path = process.argv[2];
try {
  if (!path || !fs.existsSync(path)) process.exit(0);
  const lines = fs.readFileSync(path, 'utf8').split(/\r?\n/).filter(l => l.trim().length);
  if (!lines.length) process.exit(0);
  const obj = JSON.parse(lines[lines.length - 1]);
  if (obj && obj.messageId != null) process.stdout.write(String(obj.messageId));
} catch (e) {
  // emit nothing
}
