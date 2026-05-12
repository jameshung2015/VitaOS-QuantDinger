import re, os

base = r"D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist\js"

with open(os.path.join(base, 'app.b688a4b5.js'), encoding='utf-8') as f:
    c = f.read()

# Find zh-CN context around indicator market keys
idx = c.find('dashboard.indicator.market.CNStock')
while idx != -1:
    start = max(0, idx-200)
    end = min(len(c), idx+400)
    print(f"\n--- dashboard.indicator.market.CNStock at {idx} ---")
    print(repr(c[start:end]))
    idx = c.find('dashboard.indicator.market.CNStock', idx+1)

# Also check the full zh-CN section for opportunities market CNStock
idx = c.find('aiAssetAnalysis.opportunities.market.CNStock')
while idx != -1:
    start = max(0, idx-200)
    end = min(len(c), idx+400)
    print(f"\n--- aiAssetAnalysis.opportunities.market.CNStock at {idx} ---")
    print(repr(c[start:end]))
    idx = c.find('aiAssetAnalysis.opportunities.market.CNStock', idx+1)
