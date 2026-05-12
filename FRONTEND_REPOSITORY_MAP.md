# QuantDinger 前端开发地图

## 项目仓库地图

### 🔵 源代码仓库 (Source Repository)
```
D:\app\QuantDinger-Vue
└── ✅ 仅本地使用，不上传到远程
└── ✅ 所有源码修改都在这里进行
└── ✅ 编译后产物放入 dist/ 目录
```

**用途：**
- 📝 修改 Vue 组件、样式、逻辑
- 🔨 编译前端代码
- 📦 生成部署所需的文件

**不能做：**
- ❌ git push 到远程（限制本地使用）
- ❌ 作为部署源（分离源码和构建产物）

---

### 🟡 项目部署目录 (Deployment Directory)
```
D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger
│
├── frontend/
│   └── dist/  ← 同步编译结果到这里
│       ├── index.html
│       ├── js/
│       ├── css/
│       └── img/
│
├── FRONTEND_MODIFICATION_GUIDE.md    ← 完整修改指南
├── FRONTEND_QUICK_REFERENCE.md       ← 快速参考
├── DEPLOYMENT_SCRIPTS.md             ← 自动化脚本
├── docker-compose.yml
├── docker/
│   ├── frontend.Dockerfile
│   ├── nginx.conf
│   └── ...
└── ...
```

**用途：**
- 🐳 Docker 容器从这里读取静态文件
- 📦 版本控制和项目管理
- 📋 记录开发规范和流程

**特点：**
- ✅ 包含编译产物（dist/）
- ✅ 包含 Docker 容器配置
- ✅ 包含文档说明

---

### 🟢 Docker 容器内部 (Container Runtime)
```
Docker 容器: quantdinger-frontend
│
└── /usr/share/nginx/html/  ← Nginx 根目录
    ├── index.html
    ├── js/
    ├── css/
    └── ...
```

**用途：**
- 🌐 提供前端网页服务
- 🔄 映射到宿主机 frontend/dist/

**映射关系：**
```
宿主机                                    容器内
D:\...Agents\projects\QuantDinger\       /usr/share/nginx/html/
    └── frontend/dist/ ←─────────────────────→ /
         ├── index.html
         ├── js/
         └── ...
```

---

## 修改流程示意图

```
┌─────────────────────────────────────┐
│  1️⃣  修改源代码                      │
│  D:\app\QuantDinger-Vue\src\        │
│  ├── views/                         │
│  ├── components/                    │
│  └── styles/                        │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  2️⃣  编译生成部署文件                │
│  npm run build                       │
│  ├── dist/index.html ✨             │
│  ├── dist/js/*.js ✨                │
│  └── dist/css/*.css ✨              │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  3️⃣  同步到项目部署目录              │
│  Copy dist → frontend/dist          │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  4️⃣  更新 Docker 容器                │
│  docker cp → /usr/share/nginx/      │
│  docker-compose restart             │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  5️⃣  在浏览器验证                     │
│  http://localhost:8888              │
│  Ctrl+Shift+R 刷新缓存               │
└─────────────────────────────────────┘
```

---

## 文件夹对应关系

### 源代码中的文件
```
D:\app\QuantDinger-Vue\src\views\
├── ai-analysis/
│   └── index.vue              ← 修改样式、逻辑
│       ├── <template>         ← HTML 结构
│       ├── <script>           ← JavaScript 逻辑
│       └── <style scoped>     ← CSS 样式（修改这里）
│
├── dashboard/
│   └── index.vue
│
├── settings/
│   └── index.vue
│
└── ...
```

### 编译后的输出
```
D:\app\QuantDinger-Vue\dist\
├── index.html
├── js/
│   ├── app.[hash].js          ← 主应用代码
│   ├── chunk-vendors.js       ← 第三方库
│   ├── lang-zh-CN.js          ← 中文语言包
│   └── lang-en-US.js          ← 英文语言包
├── css/
│   ├── app.[hash].css         ← 应用样式
│   └── chunk-vendors.css      ← 库的样式
├── img/
├── fonts/
└── ...
```

### 部署到项目目录
```
D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist\
├── index.html                 ← 复制自 dist/
├── js/                        ← 复制自 dist/js/
├── css/                       ← 复制自 dist/css/
├── img/                       ← 复制自 dist/img/
└── ...                        ← 复制自 dist/
```

### 进入 Docker 容器
```
容器内 /usr/share/nginx/html/
├── index.html                 ← 复制自 frontend/dist/
├── js/                        ← 复制自 frontend/dist/js/
├── css/                       ← 复制自 frontend/dist/css/
└── ...                        ← 映射自宿主机 frontend/dist/
```

---

## 重要文件说明

### 编译配置
```
D:\app\QuantDinger-Vue\
├── vue.config.js              # Vue CLI 构建配置
│   ├── webpack 配置
│   ├── devServer 配置
│   └── 编译优化选项
│
├── package.json               # npm 依赖和脚本
│   ├── dependencies           # 运行时依赖
│   ├── devDependencies        # 开发依赖
│   └── scripts                # npm run build 等命令
│
├── tsconfig.json              # TypeScript 配置（如使用）
├── .eslintrc.js               # ESLint 代码检查
└── babel.config.js            # Babel 配置（JS 转换）
```

### 部署配置
```
D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\
├── docker-compose.yml         # Docker 容器编排
│   └── 定义 frontend、backend 等服务
│
├── docker/
│   ├── frontend.Dockerfile    # 前端镜像定义
│   ├── nginx.conf             # Nginx 服务器配置
│   └── ...
│
├── .dockerignore              # Docker 构建忽略文件
└── ...
```

---

## 常用路径速查

| 目的 | 路径 | 说明 |
|------|------|------|
| **编辑源码** | `D:\app\QuantDinger-Vue\src\views\ai-analysis\index.vue` | 修改 Vue 页面 |
| **修改样式** | `D:\app\QuantDinger-Vue\src\views\*\*.vue` | 编辑 `<style>` 部分 |
| **编译命令** | `cd D:\app\QuantDinger-Vue && npm run build` | 生成 dist/ |
| **同步命令** | `Copy-Item dist\* ..\...\Agents\projects\QuantDinger\frontend\dist -Recurse -Force` | 复制编译产物 |
| **Docker 部署** | `docker cp frontend\dist\. quantdinger-frontend:/usr/share/nginx/html/` | 更新容器文件 |
| **访问应用** | `http://localhost:8888` | 浏览器验证 |

---

## 开发和部署的分离

### ✅ 为什么要分离源码和部署目录？

| 方面 | 源码目录 | 部署目录 |
|------|--------|--------|
| **位置** | `D:\app\QuantDinger-Vue` | `D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger` |
| **用途** | 开发修改 | 版本管理、Docker 容器 |
| **内容** | 原始 .vue/.js 文件 | 编译后的 .html/.js/.css |
| **Git** | ❌ 不 push | ✅ 可以 push（记录历史） |
| **大小** | ~500MB（node_modules） | ~50MB（dist 文件） |
| **变化频率** | 高（开发时频繁改） | 低（编译后稳定） |

### 优点：
- 🔒 源码不会被误上传
- 📦 部署目录包含完整的构建产物
- 🔄 易于版本控制和回滚
- 🐳 Docker 容器有稳定的部署源

---

## 快速导航

```
修改 Vue 文件？
└── D:\app\QuantDinger-Vue\src\views\

修改样式？
└── D:\app\QuantDinger-Vue\src\views\...\index.vue
    └── <style lang="less" scoped> 部分

修改国际化文本？
└── D:\app\QuantDinger-Vue\src\locales\
    ├── zh-CN.json
    └── en-US.json

更新 Nginx 配置？
└── D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\docker\nginx.conf

更新 Docker 镜像？
└── D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\docker\frontend.Dockerfile

更新部署脚本？
└── D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\deploy-frontend.ps1
```

---

## 常见误区

❌ **错误做法：**
1. 直接修改 `frontend\dist\` 中的 JavaScript 文件（编译时会覆盖）
2. 在 Docker 容器内修改文件（容器重启后会丢失）
3. 在源代码目录 push 代码到远程（违反本地开发规范）
4. 编译后不同步文件（Docker 仍使用旧版本）

✅ **正确做法：**
1. 修改源代码 `D:\app\QuantDinger-Vue\src\`
2. 编译 `npm run build`
3. 同步到项目目录 `frontend\dist\`
4. 更新 Docker 容器
5. 浏览器刷新验证

---

**最后更新：** 2026-05-12
