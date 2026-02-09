$ErrorActionPreference='Stop'
$port=5173
$base = (Resolve-Path .).Path

$mime = @{ 
  '.html'='text/html; charset=utf-8'
  '.css'='text/css; charset=utf-8'
  '.js'='text/javascript; charset=utf-8'
  '.json'='application/json; charset=utf-8'
  '.jpg'='image/jpeg'
  '.jpeg'='image/jpeg'
  '.png'='image/png'
  '.webp'='image/webp'
}

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://127.0.0.1:$port/")
$listener.Start()
Write-Host "LISTEN http://127.0.0.1:$port/" 

while ($listener.IsListening) {
  $ctx = $listener.GetContext()
  try {
    $path = $ctx.Request.Url.AbsolutePath
    if ($path -eq '/' -or [string]::IsNullOrWhiteSpace($path)) { $path = '/index.html' }
    $rel = $path.TrimStart('/') -replace '/', '\\'
    $file = Join-Path $base $rel
    if (!(Test-Path -LiteralPath $file)) {
      $ctx.Response.StatusCode = 404
      $bytes = [Text.Encoding]::UTF8.GetBytes('not found')
      $ctx.Response.OutputStream.Write($bytes,0,$bytes.Length)
      $ctx.Response.Close()
      continue
    }

    $ext = [IO.Path]::GetExtension($file).ToLower()
    if ($mime.ContainsKey($ext)) { $ctx.Response.ContentType = $mime[$ext] }

    $buf = [IO.File]::ReadAllBytes($file)
    $ctx.Response.StatusCode = 200
    $ctx.Response.OutputStream.Write($buf,0,$buf.Length)
    $ctx.Response.Close()
  } catch {
    try { $ctx.Response.StatusCode = 500; $ctx.Response.Close() } catch {}
  }
}
