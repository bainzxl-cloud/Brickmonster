import re, statistics, pathlib
p = pathlib.Path(r"C:\Users\bainz\clawd\data\ebay_75157_sold_extract.txt")
text = p.read_text(encoding="utf-8", errors="ignore")
nums = [float(x) for x in re.findall(r"C\s*\$\s*([0-9]+(?:\.[0-9]{1,2})?)", text)]
nums = [x for x in nums if 20 <= x <= 800]
nums.sort()
print(len(nums))
if nums:
    print(nums[0], statistics.median(nums), nums[-1])
