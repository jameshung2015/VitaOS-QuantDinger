# QuantDinger 前端开发文档索引

## 📚 文档导航

### 🚀 快速开始
- **[快速参考](FRONTEND_QUICK_REFERENCE.md)** - ⭐ 推荐首先阅读
  - 三地址概览
  - 5 步修改流程
  - 常用命令
  - 快速问题解决

### 📖 详细指南
- **[完整修改指南](FRONTEND_MODIFICATION_GUIDE.md)** - 深入了解每个步骤
  - 项目结构说明
  - 修改工作流程详解
  - 常见修改场景
  - 故障排除
  - 性能优化建议

### 🔧 自动化部署
- **[部署脚本文档](DEPLOYMENT_SCRIPTS.md)** - 一键部署方案
  - PowerShell 自动化脚本
  - Bash 脚本（Linux/Mac）
  - VS Code 任务集成
  - 辅助检查脚本

### 🗺️ 项目地图
- **[开发地图](FRONTEND_REPOSITORY_MAP.md)** - 理解项目结构
  - 三个仓库关系
  - 文件流动图
  - 路径对应关系
  - 常见误区

---

## 🎯 使用场景速查

### 我想修改 UI 样式
1. 打开 [快速参考](FRONTEND_QUICK_REFERENCE.md)
2. 按照"修改流程（5 分钟）"执行
3. 关键文件：`D:\app\QuantDinger-Vue\src\views\*\index.vue` 中的 `<style>` 部分

### 我想修改功能逻辑
1. 查看 [完整修改指南](FRONTEND_MODIFICATION_GUIDE.md) → 场景 2
2. 修改 `src\` 下的 Vue 文件
3. 完整重新编译和部署

### 我想自动部署
1. 参考 [部署脚本文档](DEPLOYMENT_SCRIPTS.md)
2. 运行 `.\deploy-frontend.ps1 full`
3. 脚本会自动完成编译、同步、Docker 更新

### 我想理解项目结构
1. 查看 [开发地图](FRONTEND_REPOSITORY_MAP.md)
2. 了解三个仓库的关系
3. 快速找到需要修改的文件

---

## 📋 三个关键位置

```
┌─────────────────────────────────────────┐
│  源代码（修改这里）                      │
│  D:\app\QuantDinger-Vue                 │
│  ✅ 仅本地使用，不 push                  │
│  ⚡ npm run build 在这里编译             │
└─────────────────────────────────────────┘
              ↓ 编译输出到
┌─────────────────────────────────────────┐
│  项目部署目录（同步这里）                 │
│  D:\document\Obsidian\vaults\...\      │
│  ...Projects\QuantDinger\frontend\dist  │
│  ✅ 可以版本控制                         │
│  🐳 Docker 从这里读取文件                │
└─────────────────────────────────────────┘
              ↓ docker cp 复制到
┌─────────────────────────────────────────┐
│  Docker 容器（提供网页服务）             │
│  容器内：/usr/share/nginx/html          │
│  访问：http://localhost:8888             │
│  🌐 nginx 在这里提供前端网页             │
└─────────────────────────────────────────┘
```

---

## ⚙️ 工作流程简图

```
1. 修改源码
   D:\app\QuantDinger-Vue\src\...
           ↓
2. npm run build
   生成 dist/ 文件夹
           ↓
3. 同步到项目目录
   Copy-Item dist/* ../.../QuantDinger/frontend/dist
           ↓
4. 更新 Docker
   docker cp frontend/dist/. quantdinger-frontend:/usr/share/nginx/html/
           ↓
5. 验证效果
   浏览器打开 http://localhost:8888
   Ctrl+Shift+R 刷新
           ↓
   ✅ 修改生效！
```

---

## 📝 文件说明

### FRONTEND_QUICK_REFERENCE.md
**适合：** 快速查阅、日常开发
- 三地址一览表
- 5 步修改流程
- 常用命令速查
- 常见问题 Q&A
- **阅读时间：** ~5 分钟

### FRONTEND_MODIFICATION_GUIDE.md
**适合：** 深入学习、故障排除
- 详细的修改步骤
- 常见修改场景（CSS、组件、i18n、依赖）
- 详细的故障排除指南
- 性能优化建议
- **阅读时间：** ~20 分钟

### DEPLOYMENT_SCRIPTS.md
**适合：** 自动化部署
- PowerShell 脚本（完整代码）
- Bash 脚本（Linux/Mac）
- VS Code 任务集成
- 辅助脚本说明
- **阅读时间：** ~10 分钟（脚本包含完整注释）

### FRONTEND_REPOSITORY_MAP.md
**适合：** 理解项目架构
- 三个仓库的关系和用途
- 文件结构对应图
- 修改流程示意图
- 常见误区说明
- **阅读时间：** ~15 分钟

### FRONTEND_MODIFICATION_RULES.md（本文件）
**适合：** 导航和快速查阅
- 文档索引
- 使用场景速查
- 流程简图
- 文件说明

---

## 🔗 相关外部资源

### 技术栈文档
- [Vue 2 官方文档](https://v2.vuejs.org/)
- [vue-i18n 国际化](https://kazupon.github.io/vue-i18n/)
- [Vuex 状态管理](https://vuex.vuejs.org/)
- [Ant Design Vue 组件库](https://1x.antdv.com/)
- [Less 样式预处理](http://lesscss.org/)

### 构建和部署
- [Vue CLI 官方文档](https://cli.vuejs.org/)
- [Webpack 文档](https://webpack.js.org/)
- [Nginx 文档](https://nginx.org/)
- [Docker 文档](https://docs.docker.com/)

### 代码编辑
- [VS Code 官方文档](https://code.visualstudio.com/docs)
- [Vetur 扩展](https://marketplace.visualstudio.com/items?itemName=octref.vetur) - Vue 支持
- [ESLint 扩展](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) - 代码检查

---

## 📞 常见问题快速答案

| 问题 | 答案 | 详情 |
|------|------|------|
| **修改后不生效？** | Ctrl+Shift+R 清除缓存 | [快速参考](FRONTEND_QUICK_REFERENCE.md) |
| **编译出错？** | 清除缓存、重新安装依赖 | [完整指南](FRONTEND_MODIFICATION_GUIDE.md) |
| **如何自动部署？** | 使用 `.\deploy-frontend.ps1` | [部署脚本](DEPLOYMENT_SCRIPTS.md) |
| **哪些文件不能改？** | Docker 容器内的文件 | [开发地图](FRONTEND_REPOSITORY_MAP.md) |
| **源码应该在哪修改？** | `D:\app\QuantDinger-Vue` | [开发地图](FRONTEND_REPOSITORY_MAP.md) |

---

## 🎓 学习路径

### 新手入门
1. ✅ 阅读 [快速参考](FRONTEND_QUICK_REFERENCE.md) (5 分钟)
2. ✅ 按照"修改流程"完成第一次修改 (10 分钟)
3. ✅ 查看 [开发地图](FRONTEND_REPOSITORY_MAP.md) 了解结构 (15 分钟)

### 进阶学习
1. ✅ 详读 [完整修改指南](FRONTEND_MODIFICATION_GUIDE.md) (20 分钟)
2. ✅ 学习 [部署脚本](DEPLOYMENT_SCRIPTS.md) 中的自动化 (10 分钟)
3. ✅ 根据需要参考相关技术文档

### 故障排除
1. ✅ 查看 [快速参考](FRONTEND_QUICK_REFERENCE.md) 中的常见问题
2. ✅ 阅读 [完整指南](FRONTEND_MODIFICATION_GUIDE.md) 中的故障排除章节
3. ✅ 使用 `.\check-deployment.ps1` 检查部署状态

---

## ✅ 检查清单

开始修改前：
- [ ] 已安装 Node.js 和 npm
- [ ] 已阅读 [快速参考](FRONTEND_QUICK_REFERENCE.md)
- [ ] Docker Desktop 正在运行
- [ ] 可以访问 http://localhost:8888

修改完成后：
- [ ] 源代码已修改（D:\app\QuantDinger-Vue）
- [ ] npm run build 执行成功
- [ ] 文件已同步到项目目录
- [ ] Docker 容器已更新
- [ ] 浏览器已刷新（Ctrl+Shift+R）
- [ ] 效果已验证

遇到问题时：
- [ ] 查看相关文档
- [ ] 运行 `.\check-deployment.ps1` 检查状态
- [ ] 检查 Docker 日志：`docker logs quantdinger-frontend`

---

## 📞 获取帮助

1. **快速问题？** → 查看 [快速参考](FRONTEND_QUICK_REFERENCE.md) 的 Q&A
2. **故障排除？** → 参考 [完整指南](FRONTEND_MODIFICATION_GUIDE.md) 中的排故部分
3. **自动化部署？** → 使用 [部署脚本](DEPLOYMENT_SCRIPTS.md) 或 `.\check-deployment.ps1`
4. **理解架构？** → 阅读 [开发地图](FRONTEND_REPOSITORY_MAP.md)

---

## 📊 文档关系图

```
                    FRONTEND_MODIFICATION_RULES.md (本文)
                              ↓
                    ┌─────────┼─────────┐
                    ↓         ↓         ↓
           ┌────────────┐ ┌──────────────┐ ┌──────────────┐
           │ 快速参考    │ │ 完整修改指南  │ │ 部署脚本文档  │
           │ Quick Ref  │ │ Complete Gd. │ │  Scripts    │
           └────────────┘ └──────────────┘ └──────────────┘
                    ↑         ↑         ↑
                    └─────────┼─────────┘
                              ↓
                    开发地图（Repository Map）
                    用于理解项目架构
```

---

## 🌟 最佳实践

1. **修改前**
   - 确保已理解 [开发地图](FRONTEND_REPOSITORY_MAP.md) 中的三个仓库关系
   - 备份重要代码或使用 Git 分支

2. **修改中**
   - 一次只修改一个功能或样式
   - 在本地开发服务器 (npm run serve) 中快速测试
   - 保持代码清晰和注释充分

3. **修改后**
   - 完整编译（npm run build）而不是部分编译
   - 验证文件已同步到项目目录
   - 清除浏览器缓存后再验证效果
   - 保存修改记录到项目日志

4. **部署时**
   - 使用自动化脚本（推荐）
   - 或按照 [快速参考](FRONTEND_QUICK_REFERENCE.md) 中的 5 步流程手动执行
   - 验证 Docker 容器正确更新

---

## 版本历史

| 日期 | 版本 | 更新内容 |
|------|------|--------|
| 2026-05-12 | v1.0 | 初始版本，创建所有文档 |

---

## 许可证和维护

- **维护者：** AI Assistant
- **最后更新：** 2026-05-12
- **用途：** QuantDinger 前端开发规范和工作流程
- **适用范围：** 本地开发，不包含生产部署

---

## 总结

这套文档为 QuantDinger 前端开发提供了完整的规范和工作流程：

✅ **快速开始** - 通过 [快速参考](FRONTEND_QUICK_REFERENCE.md) 在 5 分钟内完成第一次修改

✅ **完整理解** - 通过 [完整指南](FRONTEND_MODIFICATION_GUIDE.md) 深入学习每个步骤

✅ **自动化部署** - 通过 [部署脚本](DEPLOYMENT_SCRIPTS.md) 一键完成编译、同步、Docker 更新

✅ **架构认知** - 通过 [开发地图](FRONTEND_REPOSITORY_MAP.md) 理解三个仓库的关系和文件流动

**强烈推荐：** 首先阅读 [快速参考](FRONTEND_QUICK_REFERENCE.md)，了解基本流程，然后根据需要参考其他文档。
