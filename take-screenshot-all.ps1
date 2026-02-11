Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Capture all monitors using VirtualScreen
$vs = [System.Windows.Forms.SystemInformation]::VirtualScreen
$bitmap = New-Object System.Drawing.Bitmap $vs.Width, $vs.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($vs.Left, $vs.Top, 0, 0, $vs.Size)

$outDir = 'C:\Users\bainz\clawd\screenshots'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$outPath = Join-Path $outDir ("screenshot_all_{0}.png" -f (Get-Date -Format 'yyyyMMdd_HHmmss'))
$bitmap.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()

Write-Output $outPath
