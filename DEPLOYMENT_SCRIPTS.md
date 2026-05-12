# 前端部署自动化脚本

## 快速部署脚本

### PowerShell 脚本：deploy-frontend.ps1

将以下脚本保存为 `deploy-frontend.ps1`，放在项目根目录，直接运行可完成一键部署。

```powershell
# ============================================================================
# QuantDinger 前端自动化部署脚本
# 用法: .\deploy-frontend.ps1 [mode]
# mode: build (编译+同步), sync (仅同步), docker (更新容器), full (完整流程)
# 示例: .\deploy-frontend.ps1 build
# ============================================================================

param(
    [string]$mode = "full"  # 默认执行完整流程
)

# 颜色输出函数
function Write-Success {
    Write-Host "✅ $args" -ForegroundColor Green
}

function Write-Error-Message {
    Write-Host "❌ $args" -ForegroundColor Red
}

function Write-Info {
    Write-Host "ℹ️  $args" -ForegroundColor Cyan
}

function Write-Warning-Message {
    Write-Host "⚠️  $args" -ForegroundColor Yellow
}

# 路径配置
$sourceDir = "D:\app\QuantDinger-Vue"
$sourceDistDir = "$sourceDir\dist"
$projectDir = "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger"
$targetDir = "$projectDir\frontend\dist"
$containerName = "quantdinger-frontend"

Write-Info "=========================================="
Write-Info "QuantDinger 前端部署脚本"
Write-Info "模式: $mode"
Write-Info "源代码: $sourceDir"
Write-Info "部署目录: $targetDir"
Write-Info "=========================================="

# 第一步：编译前端代码
if ($mode -eq "build" -or $mode -eq "full") {
    Write-Info "第 1 步：编译前端代码..."
    
    if (-not (Test-Path $sourceDir)) {
        Write-Error-Message "源目录不存在: $sourceDir"
        exit 1
    }
    
    Push-Location $sourceDir
    
    # 清除旧的 dist 目录（可选，取决于你的需求）
    # if (Test-Path "dist") {
    #     Write-Warning-Message "删除旧的 dist 目录..."
    #     Remove-Item "dist" -Recurse -Force
    # }
    
    Write-Info "运行 npm run build..."
    npm run build
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Message "前端编译失败！"
        Pop-Location
        exit 1
    }
    
    Write-Success "前端编译成功！"
    Pop-Location
}

# 第二步：同步文件到项目目录
if ($mode -eq "sync" -or $mode -eq "build" -or $mode -eq "full") {
    Write-Info "第 2 步：同步文件到项目目录..."
    
    if (-not (Test-Path $sourceDistDir)) {
        Write-Error-Message "源 dist 目录不存在: $sourceDistDir"
        exit 1
    }
    
    # 创建目标目录（如果不存在）
    if (-not (Test-Path $targetDir)) {
        Write-Warning-Message "目标目录不存在，创建中..."
        New-Item -Path $targetDir -ItemType Directory -Force | Out-Null
    }
    
    Write-Info "复制文件: $sourceDistDir → $targetDir"
    Copy-Item -Path "$sourceDistDir\*" -Destination $targetDir -Recurse -Force
    
    # 验证文件是否复制成功
    if ((Test-Path "$targetDir\index.html") -and (Test-Path "$targetDir\js")) {
        Write-Success "文件同步成功！"
    } else {
        Write-Error-Message "文件同步失败，目标目录内容不完整！"
        exit 1
    }
}

# 第三步：更新 Docker 容器
if ($mode -eq "docker" -or $mode -eq "full") {
    Write-Info "第 3 步：更新 Docker 容器..."
    
    # 检查容器是否运行中
    $containerStatus = docker ps --filter "name=$containerName" --format "{{.Status}}"
    
    if (-not $containerStatus) {
        Write-Warning-Message "容器 $containerName 未运行，尝试启动..."
        Push-Location $projectDir
        docker-compose up -d
        Pop-Location
        Start-Sleep -Seconds 3
    }
    
    Write-Info "复制文件到容器: $targetDir → /usr/share/nginx/html/"
    docker cp "$targetDir\." "${containerName}:/usr/share/nginx/html/"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "文件已复制到容器！"
    } else {
        Write-Error-Message "复制文件到容器失败！"
        exit 1
    }
    
    # 可选：重启容器以确保新文件被加载
    Write-Warning-Message "重启容器以应用更改..."
    docker-compose -f "$projectDir\docker-compose.yml" restart $containerName
    
    Write-Info "等待容器重启..."
    Start-Sleep -Seconds 2
    
    # 验证容器状态
    $status = docker ps --filter "name=$containerName" --format "{{.Status}}"
    if ($status) {
        Write-Success "容器状态: $status"
    } else {
        Write-Error-Message "容器启动失败！查看日志："
        docker logs $containerName -n 20
        exit 1
    }
}

Write-Info "=========================================="
Write-Success "部署完成！"
Write-Info "访问地址: http://localhost:8888"
Write-Warning-Message "请刷新浏览器（Ctrl+Shift+R）清除缓存"
Write-Info "=========================================="
```

### 使用方法

```bash
# 方法 1：完整流程（编译+同步+Docker 更新）
.\deploy-frontend.ps1 full

# 方法 2：仅编译
.\deploy-frontend.ps1 build

# 方法 3：仅同步文件
.\deploy-frontend.ps1 sync

# 方法 4：仅更新容器
.\deploy-frontend.ps1 docker

# 方法 5：默认（完整流程）
.\deploy-frontend.ps1
```

---

## Bash 脚本：deploy-frontend.sh（Linux/Mac）

```bash
#!/bin/bash

# ============================================================================
# QuantDinger 前端自动化部署脚本（Linux/Mac）
# 用法: bash deploy-frontend.sh [mode]
# ============================================================================

mode=${1:-full}  # 默认完整流程

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'  # No Color

# 输出函数
success() { echo -e "${GREEN}✅ $@${NC}"; }
error() { echo -e "${RED}❌ $@${NC}"; }
info() { echo -e "${CYAN}ℹ️  $@${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $@${NC}"; }

# 路径配置
SOURCE_DIR="/mnt/d/app/QuantDinger-Vue"  # WSL 中的路径
SOURCE_DIST_DIR="$SOURCE_DIR/dist"
PROJECT_DIR="/mnt/d/document/Obsidian/vaults/J-Workspace/AGI/Agents/projects/QuantDinger"
TARGET_DIR="$PROJECT_DIR/frontend/dist"
CONTAINER_NAME="quantdinger-frontend"

info "=========================================="
info "QuantDinger 前端部署脚本"
info "模式: $mode"
info "=========================================="

# 编译前端
if [ "$mode" = "build" ] || [ "$mode" = "full" ]; then
    info "第 1 步：编译前端代码..."
    
    if [ ! -d "$SOURCE_DIR" ]; then
        error "源目录不存在: $SOURCE_DIR"
        exit 1
    fi
    
    cd "$SOURCE_DIR"
    info "运行 npm run build..."
    npm run build
    
    if [ $? -ne 0 ]; then
        error "前端编译失败！"
        exit 1
    fi
    
    success "前端编译成功！"
fi

# 同步文件
if [ "$mode" = "sync" ] || [ "$mode" = "build" ] || [ "$mode" = "full" ]; then
    info "第 2 步：同步文件到项目目录..."
    
    if [ ! -d "$SOURCE_DIST_DIR" ]; then
        error "源 dist 目录不存在: $SOURCE_DIST_DIR"
        exit 1
    fi
    
    mkdir -p "$TARGET_DIR"
    cp -r "$SOURCE_DIST_DIR"/* "$TARGET_DIR"/
    
    success "文件同步成功！"
fi

# 更新容器
if [ "$mode" = "docker" ] || [ "$mode" = "full" ]; then
    info "第 3 步：更新 Docker 容器..."
    
    docker cp "$TARGET_DIR/." "$CONTAINER_NAME:/usr/share/nginx/html/"
    
    if [ $? -eq 0 ]; then
        success "文件已复制到容器！"
    else
        error "复制文件到容器失败！"
        exit 1
    fi
    
    warning "重启容器..."
    cd "$PROJECT_DIR"
    docker-compose restart "$CONTAINER_NAME"
    
    sleep 2
    success "容器已重启！"
fi

info "=========================================="
success "部署完成！"
info "访问地址: http://localhost:8888"
warning "请刷新浏览器（Ctrl+Shift+R）清除缓存"
info "=========================================="
```

---

## 额外的辅助脚本

### 检查部署状态：check-deployment.ps1

```powershell
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "QuantDinger 部署状态检查" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 检查容器状态
Write-Host "`n1. Docker 容器状态：" -ForegroundColor Yellow
docker ps --filter "name=quantdinger-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 检查文件同步
Write-Host "`n2. 前端文件状态：" -ForegroundColor Yellow
$targetDir = "D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger\frontend\dist"
if (Test-Path "$targetDir\index.html") {
    Write-Host "✅ index.html 存在" -ForegroundColor Green
    (Get-Item "$targetDir\index.html").LastWriteTime | Write-Host
} else {
    Write-Host "❌ index.html 不存在" -ForegroundColor Red
}

# 检查容器内文件
Write-Host "`n3. 容器内文件：" -ForegroundColor Yellow
docker exec quantdinger-frontend ls -lh /usr/share/nginx/html/index.html 2>/dev/null | Write-Host
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 容器文件检查失败" -ForegroundColor Red
} else {
    Write-Host "✅ 容器文件正常" -ForegroundColor Green
}

# 检查 Nginx 日志
Write-Host "`n4. Nginx 最近日志（最后 5 行）：" -ForegroundColor Yellow
docker logs quantdinger-frontend --tail 5 2>/dev/null | Write-Host

Write-Host "`n========================================" -ForegroundColor Cyan
```

---

## 在 VS Code 中添加快捷任务

### .vscode/tasks.json

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Frontend: Full Deploy (编译+同步+Docker)",
            "type": "shell",
            "command": "powershell",
            "args": [
                "-ExecutionPolicy", "Bypass",
                "-File", "./deploy-frontend.ps1",
                "full"
            ],
            "problemMatcher": [],
            "group": {
                "kind": "build",
                "isDefault": false
            }
        },
        {
            "label": "Frontend: Build Only (仅编译)",
            "type": "shell",
            "command": "powershell",
            "args": [
                "-ExecutionPolicy", "Bypass",
                "-File", "./deploy-frontend.ps1",
                "build"
            ],
            "problemMatcher": []
        },
        {
            "label": "Frontend: Check Deployment (检查部署状态)",
            "type": "shell",
            "command": "powershell",
            "args": [
                "-ExecutionPolicy", "Bypass",
                "-File", "./check-deployment.ps1"
            ],
            "problemMatcher": []
        }
    ]
}
```

### 在 VS Code 中运行

- 按 `Ctrl+Shift+P`，输入 `Tasks: Run Task`
- 选择 `Frontend: Full Deploy` 等任务
- 自动完成编译、同步和部署

---

## 快速参考

| 命令 | 说明 |
|------|------|
| `.\deploy-frontend.ps1 full` | 完整部署（推荐） |
| `.\deploy-frontend.ps1 build` | 仅编译 |
| `.\deploy-frontend.ps1 sync` | 仅同步文件 |
| `.\deploy-frontend.ps1 docker` | 仅更新容器 |
| `.\check-deployment.ps1` | 检查部署状态 |

---

**最后更新：** 2026-05-12
