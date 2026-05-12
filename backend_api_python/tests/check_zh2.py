import re, os

base = r"D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist\js"

with open(os.path.join(base, 'app.b688a4b5.js'), encoding='utf-8') as f:
    c = f.read()

# Find zh-CN sections (Chinese characters around market keys)
# Look for 美股 which is zh-CN for US Stock
idx = c.find('\u7f8e\u80a1')  # 美股
while idx != -1:
    start = max(0, idx-200)
    end = min(len(c), idx+400)
    print(f"\n--- 美股 at {idx} ---")
    print(repr(c[start:end]))
    idx = c.find('\u7f8e\u80a1', idx+1)
    if idx > 200000:
        break  # limit output
