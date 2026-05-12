# 📖 QuantDinger 前端修改规范

> 在 `D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger` 项目中，管理前端代码修改和部署的完整规范。

## 🎯 核心原则

### 三地址分离
```
源代码仓库              编译输出              Docker 容器
D:\app\              frontend/dist/        /usr/share/nginx/html/
QuantDinger-Vue    ← (同步到这里) →    (从这里提供服务)
✅ 仅本地            ✅ 部署目录           🌐 运行环境
❌ 不 push           ✅ 可版本控制         🔄 自动映射
```

### 修改工作流
```
修改源代码 → 编译 → 同步文件 → 更新Docker → 浏览器验证
(5 分钟内完成)
```

---

## 🚀 快速开始（5 分钟）

### 1️⃣ 修改源代码
```bash
cd D:\app\QuantDinger-Vue
# 编辑你需要的文件，例如：
code src/views/ai-analysis/index.vue
```

### 2️⃣ 编译
```bash
npm run build
# ✅ 输出：Build complete. The `dist` directory is ready to be deployed.
```

### 3️⃣ 同步文件
```powershell
Copy-Item "D:\app\QuantDinger-Vue\dist\*" `
          "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist" `
          -Recurse -Force
```

### 4️⃣ 更新容器
```bash
cd D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger

docker cp "frontend\dist\." quantdinger-frontend:/usr/share/nginx/html/
docker-compose restart quantdinger-frontend
```

### 5️⃣ 验证效果
```
浏览器：http://localhost:8888
刷新：Ctrl+Shift+R (清除缓存)
查看：修改已生效 ✅
```

---

## 📚 完整文档

| 文档 | 说明 | 阅读时间 |
|------|------|--------|
| **[FRONTEND_QUICK_REFERENCE.md](FRONTEND_QUICK_REFERENCE.md)** ⭐ | 快速参考（推荐首先阅读） | ~5 分钟 |
| [FRONTEND_MODIFICATION_GUIDE.md](FRONTEND_MODIFICATION_GUIDE.md) | 完整修改指南和故障排除 | ~20 分钟 |
| [DEPLOYMENT_SCRIPTS.md](DEPLOYMENT_SCRIPTS.md) | 自动化部署脚本 | ~10 分钟 |
| [FRONTEND_REPOSITORY_MAP.md](FRONTEND_REPOSITORY_MAP.md) | 项目架构和文件关系 | ~15 分钟 |
| [FRONTEND_MODIFICATION_RULES.md](FRONTEND_MODIFICATION_RULES.md) | 文档总索引（你在这里） | ~5 分钟 |

---

## ⚙️ 一键部署

```bash
# 使用自动化脚本（推荐）
.\deploy-frontend.ps1 full

# 查看部署状态
.\check-deployment.ps1
```

详见 [DEPLOYMENT_SCRIPTS.md](DEPLOYMENT_SCRIPTS.md)

---

## 📍 关键路径

```
修改源代码          →  D:\app\QuantDinger-Vue\src\
编译输出位置        →  D:\app\QuantDinger-Vue\dist\
同步到项目          →  frontend\dist\
Docker 读取位置     →  /usr/share/nginx/html/
浏览器访问地址      →  http://localhost:8888
```

---

## 💡 常见场景

### 修改样式（最常见）
```bash
# 1. 编辑 Vue 文件中的 <style> 部分
code D:\app\QuantDinger-Vue\src\views\ai-analysis\index.vue

# 2. 编译
npm run build

# 3. 同步 + 更新
Copy-Item ... && docker cp ... && docker-compose restart
```

### 修改多语言文本
```bash
# 编辑国际化文件
code D:\app\QuantDinger-Vue\src\locales\zh-CN.json
code D:\app\QuantDinger-Vue\src\locales\en-US.json

# 编译和部署
npm run build && (同步和更新容器)
```

### 快速本地测试
```bash
# 使用开发服务器（自动热更新）
npm run serve
# 访问 http://localhost:8080（自动刷新）
```

---

## ❌ 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 修改后浏览器不变 | 浏览器缓存 | Ctrl+Shift+R 清除缓存 |
| Docker 仍显示旧版本 | 文件未同步 | `docker cp ... && docker-compose restart` |
| npm run build 失败 | 依赖问题 | `npm install && npm cache clean --force` |
| 编译缓慢 | node_modules 过大 | `npm ci` 或清除 node_modules |

---

## 🔗 项目结构

```
D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\
│
├── frontend\dist\                    # 前端编译输出（同步目标）
│   ├── index.html
│   ├── js\
│   ├── css\
│   └── ...
│
├── docker-compose.yml                # Docker 容器编排
├── docker\
│   ├── frontend.Dockerfile           # 前端镜像定义
│   ├── nginx.conf                    # Nginx 配置
│   └── ...
│
├── 📖 FRONTEND_QUICK_REFERENCE.md    # ⭐ 快速参考（推荐首先）
├── 📖 FRONTEND_MODIFICATION_GUIDE.md  # 完整修改指南
├── 📖 DEPLOYMENT_SCRIPTS.md          # 自动化脚本
├── 📖 FRONTEND_REPOSITORY_MAP.md     # 项目地图
├── 📖 FRONTEND_MODIFICATION_RULES.md # 文档索引
│
├── deploy-frontend.ps1               # PowerShell 部署脚本
├── check-deployment.ps1              # 部署检查脚本
│
└── ... (其他配置文件)
```

---

## ✅ 检查清单

部署前确认：
- [ ] 已修改源代码（D:\app\QuantDinger-Vue）
- [ ] npm run build 成功
- [ ] 文件已同步到 frontend\dist\
- [ ] Docker 容器已更新
- [ ] 浏览器已刷新（Ctrl+Shift+R）
- [ ] 效果已验证

---

## 📞 获取帮助

- 🚀 **快速问题？** → [快速参考](FRONTEND_QUICK_REFERENCE.md)
- 🔧 **故障排除？** → [完整指南 - 故障排除](FRONTEND_MODIFICATION_GUIDE.md)
- ⚙️ **自动部署？** → [部署脚本](DEPLOYMENT_SCRIPTS.md)
- 🗺️ **理解架构？** → [开发地图](FRONTEND_REPOSITORY_MAP.md)

---

## 🎓 学习路径

1. **10 分钟入门**
   - ✅ 读 [快速参考](FRONTEND_QUICK_REFERENCE.md)
   - ✅ 按 5 步流程完成一次修改
   
2. **30 分钟深入**
   - ✅ 读 [开发地图](FRONTEND_REPOSITORY_MAP.md) 理解结构
   - ✅ 读 [完整指南](FRONTEND_MODIFICATION_GUIDE.md) 学细节
   
3. **自动化部署**
   - ✅ 学 [部署脚本](DEPLOYMENT_SCRIPTS.md)
   - ✅ 运行 `.\deploy-frontend.ps1`

---

## 🌟 最佳实践

✅ **做这些：**
- 在 `D:\app\QuantDinger-Vue` 修改源码
- 完整 `npm run build` 编译
- 使用 `.\deploy-frontend.ps1` 自动部署
- 清浏览器缓存 (Ctrl+Shift+R) 后验证

❌ **避免这些：**
- 直接修改 `frontend\dist\` 中的文件（编译覆盖）
- 在 Docker 容器内修改文件（重启丢失）
- 在源码目录 push 到远程（违反本地规范）
- 跳过文件同步直接更新 Docker（内容不一致）

---

## 💾 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-05-12 | v1.0 | 初始版本，创建完整文档体系 |

---

## 📝 维护信息

- **维护者：** AI Assistant
- **最后更新：** 2026-05-12
- **适用范围：** QuantDinger 前端本地开发
- **文档语言：** 中文 (zh-CN)

---

## 🔗 相关资源

- [Vue 2 官方文档](https://v2.vuejs.org/)
- [Vue CLI 文档](https://cli.vuejs.org/)
- [Docker 文档](https://docs.docker.com/)
- [Nginx 文档](https://nginx.org/)

---

<div align="center">

**推荐从 [FRONTEND_QUICK_REFERENCE.md](FRONTEND_QUICK_REFERENCE.md) 开始！**

有问题？查看 [完整文档](FRONTEND_MODIFICATION_RULES.md)

</div>
