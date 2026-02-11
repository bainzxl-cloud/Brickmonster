$root = 'C:\Users\bainz'
$pattern = '*0129*'
Get-ChildItem -Path $root -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -like $pattern -or $_.BaseName -like $pattern } |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 50 FullName,Length,LastWriteTime
