Add-Type -AssemblyName System.Drawing

$W = 1200
$H = 800
$margin = 80

# Plot range
$xmin = -3.0; $xmax = 3.0
$ymin = -27.0; $ymax = 27.0

function sx([double]$x){
  return [int]($margin + ($x - $xmin) * ($W - 2*$margin) / ($xmax - $xmin))
}
function sy([double]$y){
  return [int]($H - $margin - ($y - $ymin) * ($H - 2*$margin) / ($ymax - $ymin))
}

$outDir = 'C:\Users\bainz\clawd\outputs\plots'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$outPath = Join-Path $outDir 'y_equals_x_cubed.png'

$bmp = New-Object System.Drawing.Bitmap($W, $H)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(60,153,153,153), 1)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255,17,17,17), 3)
$curvePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255,31,79,255), 5)

$font = New-Object System.Drawing.Font('Segoe UI', 11)
$fontTitle = New-Object System.Drawing.Font('Segoe UI', 16, [System.Drawing.FontStyle]::Bold)
$brush = [System.Drawing.Brushes]::Black

$x0 = sx 0
$y0 = sy 0

$xticks = @(-3,-2,-1,0,1,2,3)
$yticks = @(-20,-10,0,10,20)

# Grid
foreach($t in $xticks){
  $x = sx $t
  $g.DrawLine($gridPen, $x, $margin, $x, $H-$margin)
}
foreach($t in $yticks){
  $y = sy $t
  $g.DrawLine($gridPen, $margin, $y, $W-$margin, $y)
}

# Axes
$g.DrawLine($axisPen, $margin, $y0, $W-$margin, $y0)
$g.DrawLine($axisPen, $x0, $margin, $x0, $H-$margin)

# Ticks + labels
foreach($t in $xticks){
  $x = sx $t
  $g.DrawLine($axisPen, $x, $y0-6, $x, $y0+6)
  $s = $t.ToString()
  $sz = $g.MeasureString($s, $font)
  $g.DrawString($s, $font, $brush, $x - $sz.Width/2, $y0 + 8)
}
foreach($t in $yticks){
  $y = sy $t
  $g.DrawLine($axisPen, $x0-6, $y, $x0+6, $y)
  if($t -ne 0){
    $s = $t.ToString()
    $sz = $g.MeasureString($s, $font)
    $g.DrawString($s, $font, $brush, $x0 - $sz.Width - 10, $y - $sz.Height/2)
  }
}

# Curve y=x^3
$pts = New-Object System.Collections.Generic.List[System.Drawing.PointF]
for($i=0; $i -le 800; $i++){
  $x = $xmin + ($xmax - $xmin) * $i / 800.0
  $y = [math]::Pow($x, 3)
  $pts.Add([System.Drawing.PointF]::new((sx $x), (sy $y)))
}
$g.DrawLines($curvePen, $pts.ToArray())

# Title
$title = 'Graph of y = x^3'
$tsz = $g.MeasureString($title, $fontTitle)
$g.DrawString($title, $fontTitle, $brush, ($W-$tsz.Width)/2, 20)

$bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()

Write-Output $outPath
