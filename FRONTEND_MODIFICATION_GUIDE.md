# 前端修改规则与工作流程

## 概述

本指南说明如何修改和部署 QuantDinger 前端代码。

**关键原则：**
- ✅ **源代码仓库**：`D:\app\QuantDinger-Vue`（仅本地使用，**不要 push** 到远程）
- ✅ **项目部署目录**：`D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger`
- ✅ **Docker 镜像部署**：前端 nginx 容器从此项目目录复制文件

---

## 修改工作流程

### 1. 修改源代码
```bash
# 在源代码仓库中修改文件
cd D:\app\QuantDinger-Vue

# 修改相关的 .vue/.jsx/.js/.css 等文件
# 示例：修改样式、UI、功能等
```

**前端项目结构：**
```
D:\app\QuantDinger-Vue\
├── src\
│   ├── views\              # 页面组件
│   │   ├── ai-analysis\    # AI 分析页面
│   │   ├── dashboard\
│   │   └── ...
│   ├── components\         # 公共组件
│   ├── locales\            # 国际化（i18n）
│   │   ├── index.js
│   │   ├── en-US.json
│   │   └── zh-CN.json
│   ├── store\              # Vuex 状态管理
│   │   └── modules\
│   │       ├── app.js      # 全局应用状态（语言、主题等）
│   ├── api\                # API 调用封装
│   └── ...
├── vue.config.js           # Vue CLI 构建配置
├── package.json
└── dist\                   # 构建输出目录（仅在编译后出现）
```

### 2. 编译前端项目

```bash
# 进入源代码目录
cd D:\app\QuantDinger-Vue

# 安装依赖（首次或更新依赖时）
npm install

# 开发模式（可选，用于本地测试）
npm run serve    # 启动开发服务器 (http://localhost:8080)

# 生产环境编译
npm run build    # 构建到 dist/ 目录
```

**编译输出：**
- 输出位置：`D:\app\QuantDinger-Vue\dist\`
- 包含文件：`index.html`、`js/`、`css/`、`img/` 等

### 3. 更新项目部署目录

```bash
# 编译完成后，同步 dist 文件到项目部署目录
# 使用 robocopy（Windows）或类似工具

# 方法 A：手动复制（使用 PowerShell）
Copy-Item -Path "D:\app\QuantDinger-Vue\dist\*" `
          -Destination "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist" `
          -Recurse -Force

# 方法 B：使用 robocopy
robocopy "D:\app\QuantDinger-Vue\dist" `
         "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist" `
         /MIR /E

# 方法 C：使用 PowerShell 自动化脚本
$sourceDir = "D:\app\QuantDinger-Vue\dist"
$targetDir = "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist"
if (Test-Path $sourceDir) {
    Remove-Item $targetDir -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item $sourceDir -Destination $targetDir -Recurse
    Write-Host "✅ Frontend files synchronized successfully"
} else {
    Write-Host "❌ Source directory not found: $sourceDir"
}
```

**部署目录结构：**
```
D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\
├── frontend\
│   └── dist\               # 前端编译输出
│       ├── index.html
│       ├── js\
│       ├── css\
│       └── img\
├── docker-compose.yml      # Docker 容器编排
└── ...
```

### 4. Docker 部署更新

#### 方式 A：直接更新容器内文件（快速热更新）

```bash
# 仅适用于 CSS/图片等静态资源的快速修改
cd D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger

# 复制新文件到运行中的容器
docker cp "frontend\dist\." quantdinger-frontend:/usr/share/nginx/html/

# 验证文件是否复制成功
docker exec quantdinger-frontend ls -la /usr/share/nginx/html/index.html

# 刷新浏览器查看效果（F5 或 Ctrl+Shift+R 清除缓存）
```

#### 方式 B：重建容器镜像（推荐用于重大更新）

```bash
# 停止旧容器
cd D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger
docker-compose down

# 重新构建镜像
docker-compose up -d --build

# 或者只重建前端镜像
docker-compose up -d --build quantdinger-frontend

# 等待容器启动完成
docker-compose ps
docker logs quantdinger-frontend
```

#### Dockerfile 位置
- 前端 Dockerfile：`docker/frontend.Dockerfile`（如果存在）
- nginx 配置：`docker/nginx.conf`（如果存在）
- Docker Compose：`docker-compose.yml`（项目根目录）

**Docker 容器内的静态文件位置：**
```
容器内路径：/usr/share/nginx/html
映射关系：宿主机 frontend/dist → 容器 /usr/share/nginx/html
```

### 5. 验证部署

```bash
# 检查容器状态
docker ps | grep quantdinger-frontend

# 查看容器日志
docker logs quantdinger-frontend -f

# 检查文件是否同步
docker exec quantdinger-frontend ls -R /usr/share/nginx/html/ | head -20

# 测试应用访问
# 在浏览器打开：http://localhost:8888（或配置的端口）
# Ctrl+Shift+R 刷新清除浏览器缓存
```

---

## 常见修改场景

### 场景 1：修改样式（CSS/SCSS）

```bash
# 1. 修改源文件
vim D:\app\QuantDinger-Vue\src\views\ai-analysis\index.vue
# 或修改其他 .vue 或 .css 文件

# 2. 编译
cd D:\app\QuantDinger-Vue && npm run build

# 3. 同步到项目目录
Copy-Item -Path "D:\app\QuantDinger-Vue\dist\*" `
          -Destination "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist" `
          -Recurse -Force

# 4. 更新容器
docker cp "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist\." `
           quantdinger-frontend:/usr/share/nginx/html/

# 5. 浏览器刷新测试
# Ctrl+Shift+R 清除缓存后查看效果
```

### 场景 2：修改 Vue 组件逻辑

```bash
# 1. 修改组件文件
vim D:\app\QuantDinger-Vue\src\views\dashboard\index.vue
# 或修改 src/components/ 下的组件

# 2. 如果修改涉及 webpack/构建配置，需要完整重建
cd D:\app\QuantDinger-Vue && npm run build

# 3. 验证编译是否有错误
# 如果编译失败，查看终端错误信息

# 4. 同步文件
Copy-Item "D:\app\QuantDinger-Vue\dist\*" `
          "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist" `
          -Recurse -Force

# 5. 重启容器（JS 逻辑变化需要重启）
docker-compose restart quantdinger-frontend
docker logs quantdinger-frontend
```

### 场景 3：修改国际化文本（i18n）

```bash
# 1. 修改语言文件
vim D:\app\QuantDinger-Vue\src\locales\zh-CN.json
vim D:\app\QuantDinger-Vue\src\locales\en-US.json

# 2. 编译
cd D:\app\QuantDinger-Vue && npm run build

# 3. 同步并重启
Copy-Item "D:\app\QuantDinger-Vue\dist\*" `
          "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist" `
          -Recurse -Force
docker-compose restart quantdinger-frontend
```

### 场景 4：添加新的 npm 依赖

```bash
# 1. 安装新依赖
cd D:\app\QuantDinger-Vue
npm install [package-name]

# 2. 如果使用了新依赖，修改相关 .vue 文件

# 3. 编译（新依赖会被打包进去）
npm run build

# 4. 同步并重启容器
Copy-Item "D:\app\QuantDinger-Vue\dist\*" `
          "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist" `
          -Recurse -Force
docker-compose restart quantdinger-frontend
```

---

## 编译故障排除

### 问题：Webpack 版本冲突

**症状：** `Cannot find module 'webpack/lib/rules/BasicEffectRulePlugin'`

**解决：**
```bash
cd D:\app\QuantDinger-Vue
npm install webpack@5 --save-dev
# 确保 vue.config.js 中正确引用 webpack
```

### 问题：编译缓存导致样式未更新

**症状：** 修改了 CSS 但浏览器显示旧样式

**解决：**
```bash
# 清除 npm 缓存
npm cache clean --force

# 删除 dist 目录后重新编译
rm -r dist
npm run build

# 浏览器清除缓存：Ctrl+Shift+R 或进入开发者工具 → 禁用缓存
```

### 问题：Docker 容器仍然显示旧内容

**症状：** 更新了文件但容器仍显示旧版本

**解决：**
```bash
# 确保文件已同步到正确位置
docker exec quantdinger-frontend cat /usr/share/nginx/html/index.html

# 强制重启容器
docker-compose restart quantdinger-frontend

# 或重新启动整个 Docker 环境
docker-compose down
docker-compose up -d --build
```

---

## 性能优化建议

1. **开发时使用 npm run serve**
   - 快速热模块重载（HMR）
   - 不需要每次手动编译

2. **生产编译时使用 npm run build**
   - 生成优化的代码
   - 包括代码分割、压缩等

3. **使用 Docker 容器多阶段构建**
   - 减少镜像大小
   - 提高部署速度

4. **设置 nginx 缓存策略**
   - 为静态资源设置合适的 Cache-Control 头
   - 避免用户获取过期的文件

---

## 检查清单

修改前端后，完整部署前请检查：

- [ ] 源代码修改已完成（D:\app\QuantDinger-Vue）
- [ ] npm run build 编译成功，无错误
- [ ] dist/ 目录包含所有必要文件
- [ ] 文件已同步到项目目录（frontend/dist）
- [ ] Docker 容器已更新（docker cp 或重建）
- [ ] 浏览器已清除缓存（Ctrl+Shift+R）
- [ ] 在浏览器中验证修改效果
- [ ] Docker 日志无错误：docker logs quantdinger-frontend

---

## 快速参考命令

```bash
# 完整修改和部署流程（一条命令）
cd D:\app\QuantDinger-Vue && `
npm run build && `
Copy-Item "dist\*" "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist" -Recurse -Force && `
cd "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger" && `
docker-compose restart quantdinger-frontend && `
Write-Host "✅ Frontend deployment complete!"
```

---

## 最后更新

- **日期：** 2026-05-12
- **修改人：** AI Assistant
- **更新内容：** 创建初始前端修改规则文档
