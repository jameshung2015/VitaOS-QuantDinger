# 前端修改快速参考

## 三地址概览

| 用途 | 路径 | 说明 |
|------|------|------|
| **源代码** | `D:\app\QuantDinger-Vue` | ✅ 修改源码在这里，**不要 push** |
| **编译输出** | `D:\app\QuantDinger-Vue\dist` | npm run build 的输出位置 |
| **项目部署** | `D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist` | 同步到这里后 Docker 会读取 |
| **Docker 挂载** | 容器内：`/usr/share/nginx/html` | Nginx 服务静态文件的位置 |

---

## 修改流程（5 分钟）

### 1️⃣ 修改源代码
```bash
# 打开源代码编辑器
cd D:\app\QuantDinger-Vue

# 修改 .vue/.js/.css 等文件
# 示例：修改 src/views/ai-analysis/index.vue 的样式
code .
```

### 2️⃣ 编译
```bash
npm run build

# ✅ 成功输出：Build complete. The `dist` directory is ready to be deployed.
```

### 3️⃣ 同步到项目目录
```powershell
# PowerShell
Copy-Item -Path "D:\app\QuantDinger-Vue\dist\*" `
          -Destination "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist" `
          -Recurse -Force
```

### 4️⃣ 更新 Docker
```bash
# 在项目目录
cd D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger

# 更新容器
docker cp "frontend\dist\." quantdinger-frontend:/usr/share/nginx/html/

# 重启容器
docker-compose restart quantdinger-frontend
```

### 5️⃣ 验证效果
```
浏览器打开：http://localhost:8888
按 Ctrl+Shift+R 清除缓存
查看修改是否生效
```

---

## 常用命令速查

### 开发阶段
```bash
cd D:\app\QuantDinger-Vue

# 启动开发服务器（自动热更新）
npm run serve
# 访问 http://localhost:8080

# 检查代码语法
npm run lint

# 运行单元测试
npm run test:unit
```

### 编译部署
```bash
# 生产编译（包含优化）
npm run build

# 预览编译后的结果
npm run preview

# 检查编译大小
npm run build -- --report
```

### Docker 操作
```bash
# 查看前端容器状态
docker ps --filter "name=quantdinger-frontend"

# 查看容器日志
docker logs quantdinger-frontend -f

# 进入容器（调试）
docker exec -it quantdinger-frontend bash

# 验证文件已同步
docker exec quantdinger-frontend ls -la /usr/share/nginx/html/

# 重启容器
docker-compose restart quantdinger-frontend

# 完整重建
docker-compose down
docker-compose up -d --build
```

---

## 项目文件结构

### 源代码位置（需要修改的文件）
```
D:\app\QuantDinger-Vue\
├── src/
│   ├── views/                     # 页面组件（通常改这里）
│   │   ├── ai-asset-analysis/    # ← 修改样式的示例位置
│   │   │   └── index.vue
│   │   ├── dashboard/
│   │   ├── indicator-ide/
│   │   └── ...
│   │
│   ├── components/                # 公共组件
│   │   ├── QuickTradePanel/
│   │   └── ...
│   │
│   ├── locales/                   # 国际化文本
│   │   ├── zh-CN.json            # 中文
│   │   └── en-US.json            # 英文
│   │
│   ├── store/                     # 全局状态管理
│   │   ├── modules/
│   │   │   ├── app.js           # 应用全局状态
│   │   │   └── ...
│   │   └── index.js
│   │
│   ├── api/                       # API 调用
│   │   └── ...
│   │
│   ├── App.vue                    # 根组件
│   └── main.js                    # 入口文件
│
├── public/                        # 静态资源（不编译）
├── dist/                          # 编译输出（npm run build 生成）
├── vue.config.js                  # Vue CLI 配置
├── package.json                   # 依赖和脚本配置
└── ...
```

### 部署位置
```
D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\
├── frontend/
│   └── dist/                      # ← 同步编译结果到这里
│       ├── index.html
│       ├── js/
│       │   ├── app.[hash].js
│       │   ├── chunk-vendors.[hash].js
│       │   ├── lang-zh-CN.[hash].js
│       │   └── lang-en-US.[hash].js
│       ├── css/
│       │   ├── app.[hash].css
│       │   └── chunk-vendors.[hash].css
│       ├── img/
│       └── fonts/
│
├── docker-compose.yml             # Docker 容器配置
└── ...
```

---

## 场景示例

### 🎨 修改 UI 样式（最常见）

**修改内容：** 改变 AI 分析页面的按钮颜色

```bash
# 1. 编辑源文件
# D:\app\QuantDinger-Vue\src\views\ai-analysis\index.vue
# 修改 <style lang="less" scoped> 部分

# 2. 编译
cd D:\app\QuantDinger-Vue && npm run build

# 3. 同步（PowerShell）
Copy-Item "dist\*" `
  "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist" `
  -Recurse -Force

# 4. 更新容器
docker cp "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist\." `
  quantdinger-frontend:/usr/share/nginx/html/

# 5. 验证
docker logs quantdinger-frontend
# 在浏览器访问 http://localhost:8888（Ctrl+Shift+R 刷新）
```

### 📝 修改多语言文本

**修改内容：** 更新中英文界面文本

```bash
# 1. 编辑国际化文件
# D:\app\QuantDinger-Vue\src\locales\zh-CN.json
# D:\app\QuantDinger-Vue\src\locales\en-US.json

# 2. 编译和部署（一条命令）
cd D:\app\QuantDinger-Vue && npm run build && `
Copy-Item "dist\*" `
  "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist" `
  -Recurse -Force && `
docker cp "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist\." `
  quantdinger-frontend:/usr/share/nginx/html/ && `
docker-compose restart quantdinger-frontend
```

### 🔧 修改组件逻辑

**修改内容：** 改变某个页面的功能或交互

```bash
# 1. 编辑组件
# D:\app\QuantDinger-Vue\src\views\dashboard\index.vue

# 2. 完整部署（需要重启容器）
cd D:\app\QuantDinger-Vue && npm run build
Copy-Item "dist\*" `
  "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist" `
  -Recurse -Force
cd "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger"
docker-compose restart quantdinger-frontend
```

---

## ⚠️ 常见问题

### Q: 修改后浏览器还是显示旧内容？
**A:** 
- ✅ 按 `Ctrl+Shift+R` 强制刷新（清除浏览器缓存）
- ✅ 检查文件是否同步：`docker exec quantdinger-frontend ls /usr/share/nginx/html/`
- ✅ 重启容器：`docker-compose restart quantdinger-frontend`

### Q: 编译出错 "Cannot find module 'webpack'"？
**A:** 
- ✅ 重新安装依赖：`npm install webpack@5 --save-dev`
- ✅ 清除缓存：`npm cache clean --force`
- ✅ 重新编译：`npm run build`

### Q: 能否在 `D:\document\Obsidian\...` 目录直接修改源码？
**A:** ❌ 不推荐。应始终在 `D:\app\QuantDinger-Vue` 修改源码，然后编译同步。这样做的原因：
- 源码和编译输出的分离
- 避免意外 push 到远程仓库
- 便于版本管理

### Q: Docker 容器文件位置在哪？
**A:** 容器内静态文件位置是 `/usr/share/nginx/html/`，对应宿主机路径 `D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist`

---

## 🚀 一键部署（推荐）

### 使用自动化脚本

```bash
# 完整流程（编译+同步+Docker更新）
.\deploy-frontend.ps1 full

# 查看部署状态
.\check-deployment.ps1
```

详见 [DEPLOYMENT_SCRIPTS.md](DEPLOYMENT_SCRIPTS.md)

---

## 📚 更多文档

- 📖 [完整修改指南](FRONTEND_MODIFICATION_GUIDE.md) - 详细说明和故障排除
- 🔧 [部署脚本文档](DEPLOYMENT_SCRIPTS.md) - 自动化脚本使用
- 🐳 [Docker 配置](../docker-compose.yml) - 容器配置

---

## 检查清单

修改后部署前：
- [ ] 源代码修改完成（D:\app\QuantDinger-Vue）
- [ ] npm run build 成功
- [ ] 文件已同步到项目目录
- [ ] Docker 容器已更新
- [ ] 浏览器已清除缓存（Ctrl+Shift+R）
- [ ] 在浏览器验证效果

---

**最后更新：** 2026-05-12
**维护人：** AI Assistant
