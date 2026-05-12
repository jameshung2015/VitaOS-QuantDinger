import re, os

base = r"D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist\js"

# Check app.b688a4b5.js
with open(os.path.join(base, 'app.b688a4b5.js'), encoding='utf-8') as f:
    c = f.read()

print("=== CNETF occurrences in app.b688a4b5.js ===")
print("Total count:", c.count('CNETF'))

# Find surrounding context for each CNETF occurrence
idx = 0
while True:
    idx = c.find('CNETF', idx)
    if idx == -1:
        break
    start = max(0, idx-100)
    end = min(len(c), idx+100)
    print(f"\n--- at {idx} ---")
    print(repr(c[start:end]))
    idx += 1

print("\n=== dashboard.indicator.market keys ===")
matches = re.findall(r'dashboard\.indicator\.market\.[A-Za-z]+', c)
for m in set(matches):
    print(m)

print("\n=== dashboard.analysis.market keys ===")
matches = re.findall(r'dashboard\.analysis\.market\.[A-Za-z]+', c)
for m in set(matches):
    print(m)

print("\n=== aiAssetAnalysis.opportunities.market keys ===")
matches = re.findall(r'aiAssetAnalysis\.opportunities\.market\.[A-Za-z]+', c)
for m in set(matches):
    print(m)
