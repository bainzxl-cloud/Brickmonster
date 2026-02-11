$src = 'C:\Users\bainz\Pictures\Clawdbot\saved_20260129_012824.jpg'
$dstDir = 'C:\Users\bainz\Downloads'
New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
$dst = Join-Path $dstDir (Split-Path $src -Leaf)
Move-Item -Force $src $dst
Write-Output $dst
