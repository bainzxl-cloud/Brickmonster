param(
  [string]$OutPath = "C:\Users\bainz\clawd\outputs\plots\elasticity_types_demand.png"
)

Add-Type -AssemblyName System.Drawing

$W = 1400
$H = 900
$margin = 90

# Plot area ranges (Quantity Q on x, Price P on y)
$xmin = 0.0; $xmax = 10.0
$ymin = 0.0; $ymax = 10.0

function sx([double]$x){
  return [int]($margin + ($x - $xmin) * ($W - 2*$margin) / ($xmax - $xmin))
}
function sy([double]$y){
  return [int]($H - $margin - ($y - $ymin) * ($H - 2*$margin) / ($ymax - $ymin))
}

$outDir = Split-Path -Parent $OutPath
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$bmp = New-Object System.Drawing.Bitmap($W, $H)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.Clear([System.Drawing.Color]::White)

$gridPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(45,153,153,153), 1)
$axisPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255,20,20,20), 3)

$font = New-Object System.Drawing.Font('Segoe UI', 12)
$fontSmall = New-Object System.Drawing.Font('Segoe UI', 10)
$fontTitle = New-Object System.Drawing.Font('Segoe UI', 18, [System.Drawing.FontStyle]::Bold)
$brush = [System.Drawing.Brushes]::Black

# Grid
for($t=0; $t -le 10; $t+=1){
  $x = sx $t
  $y = sy $t
  $g.DrawLine($gridPen, $x, $margin, $x, $H-$margin)
  $g.DrawLine($gridPen, $margin, $y, $W-$margin, $y)
}

# Axes
$x0 = sx 0
$y0 = sy 0
$g.DrawLine($axisPen, $margin, $y0, $W-$margin, $y0)
$g.DrawLine($axisPen, $x0, $margin, $x0, $H-$margin)

# Axis labels
$g.DrawString('Quantity (Q)', $font, $brush, ($W/2)-60, $H-$margin+30)
$g.DrawString('Price (P)', $font, $brush, 15, ($H/2)-20)

# Title
$title = 'Demand Curves: Different Types of Price Elasticity'
$tsz = $g.MeasureString($title, $fontTitle)
$g.DrawString($title, $fontTitle, $brush, ($W-$tsz.Width)/2, 25)

# Helper to draw line with label
function DrawLineLabeled($x1,$y1,$x2,$y2,[System.Drawing.Color]$color,[string]$label,[int]$lx,[int]$ly){
  $pen = New-Object System.Drawing.Pen($color, 4)
  $g.DrawLine($pen, (sx $x1), (sy $y1), (sx $x2), (sy $y2))
  $g.DrawString($label, $fontSmall, (New-Object System.Drawing.SolidBrush($color)), $lx, $ly)
  $pen.Dispose()
}

# Perfectly inelastic (vertical)
DrawLineLabeled 5 1 5 9 ([System.Drawing.Color]::FromArgb(230,220,50,50)) 'Perfectly inelastic (E=0)' (sx 5)+10 (sy 9)+10

# Inelastic (steep)
DrawLineLabeled 3 9 6 1 ([System.Drawing.Color]::FromArgb(230,245,130,49)) 'Inelastic (0<E<1)' (sx 3)+10 (sy 7)

# Unitary elastic (mid slope)
DrawLineLabeled 1.5 9 8.5 1 ([System.Drawing.Color]::FromArgb(230,75,160,75)) 'Unitary elastic (E=1)' (sx 5) (sy 5)-25

# Elastic (flat)
DrawLineLabeled 1 6.5 9 3.5 ([System.Drawing.Color]::FromArgb(230,60,120,220)) 'Elastic (E>1)' (sx 7) (sy 3.7)-30

# Perfectly elastic (horizontal)
DrawLineLabeled 1 8 9 8 ([System.Drawing.Color]::FromArgb(230,145,75,200)) 'Perfectly elastic (E=∞)' (sx 6.2) (sy 8)-28

# Note
$note = 'Note: shapes are illustrative (not to exact scale). Elasticity varies along a straight-line demand curve.'
$g.DrawString($note, $fontSmall, $brush, $margin, $H-$margin+55)

$bmp.Save($OutPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()

Write-Output $OutPath
