$src = 'C:\Users\bainz\.clawdbot\media\inbound\8994b8b5-7bdd-427b-9a16-c265765885bd.jpg'
$dstDir = 'C:\Users\bainz\Pictures\Clawdbot'
New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
$dst = Join-Path $dstDir ("saved_{0}.jpg" -f (Get-Date -Format 'yyyyMMdd_HHmmss'))
Copy-Item -Force $src $dst
Write-Output $dst
