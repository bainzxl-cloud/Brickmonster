$url = 'https://www.ebay.ca/sch/i.html?_nkw=LEGO+75157&LH_Sold=1&LH_Complete=1'
$html = (Invoke-WebRequest -UseBasicParsing $url).Content
$matches = [regex]::Matches($html, 'C\s*\$\s*([0-9]+(?:\.[0-9]{2})?)')
$nums = @()
foreach ($m in $matches) { $nums += [double]$m.Groups[1].Value }
# Heuristic cleanup: remove obvious filter UI values (0, 1000) and extreme outliers
$nums = $nums | Where-Object { $_ -ge 20 -and $_ -le 800 } | Sort-Object
$count = $nums.Count
if ($count -eq 0) { throw 'No prices found after filtering' }
$min = $nums[0]
$max = $nums[$count - 1]
if ($count % 2 -eq 1) { $median = $nums[($count - 1) / 2] } else { $median = ($nums[$count/2 - 1] + $nums[$count/2]) / 2 }
[pscustomobject]@{ count = $count; min = $min; median = $median; max = $max; currency = 'CAD'; url=$url } | ConvertTo-Json -Compress
