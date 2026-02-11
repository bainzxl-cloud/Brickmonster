$root = 'C:\Users\bainz'
$pattern = '*240*test*2016*'
Get-ChildItem -Path $root -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -like $pattern -or $_.BaseName -like $pattern } |
  Sort-Object Length -Descending |
  Select-Object -First 50 FullName,Length,LastWriteTime
