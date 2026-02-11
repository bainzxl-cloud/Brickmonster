$url='https://www.ebay.ca/sch/i.html?_nkw=LEGO+75157&LH_Sold=1&LH_Complete=1'
$html=(Invoke-WebRequest -UseBasicParsing $url).Content
$len=$html.Length
$take=[Math]::Min(2000,$len)
$html.Substring(0,$take)
