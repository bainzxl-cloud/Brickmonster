$text = Get-Content 'C:\Users\bainz\clawd\data\ebay_75157_sold_extract.txt' -Raw
$matches = [regex]::Matches($text, 'C\s*\$\s*([0-9]+(?:\.[0-9]{1,2})?)')
$nums = @()
foreach ($m in $matches) { $nums += [double]$m.Groups[1].Value }
$nums = $nums | Where-Object { $_ -ge 20 -and $_ -le 800 } | Sort-Object
$count = $nums.Count
if ($count -eq 0) { throw 'No prices found after filtering' }
$min = $nums[0]
$max = $nums[$count - 1]
if ($count % 2 -eq 1) { $median = $nums[($count - 1) / 2] } else { $median = ($nums[$count/2 - 1] + $nums[$count/2]) / 2 }
[pscustomobject]@{ count = $count; min = $min; median = $median; max = $max; currency='CAD' } | ConvertTo-Json -Compress
