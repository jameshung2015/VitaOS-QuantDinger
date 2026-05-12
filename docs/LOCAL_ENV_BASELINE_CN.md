# QuantDinger 本地环境基线说明

## 1. 文档目的

本文件是 QuantDinger 中国市场改造的唯一环境基线说明，用于在开始任何功能代码修改前固定当前仓库归属、运行边界、风险点和后续操作约束，避免误操作到错误远端、错误部署面或覆盖本地已有改动。

## 2. 当前基线快照

- 基线记录日期: 2026-05-12
- 本地代码路径: `D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger`
- 当前分支: `main`
- 当前提交: `84d56f27a88ed18454bc0d06a0276620954fb0a5`
- 当前 Git 远端:
  - `origin = https://github.com/brokermr810/QuantDinger.git`
- 当前 GitHub 目标账号:
  - `jameshung2015`
- 当前状态:
  - 本地仓库尚未切换到 `jameshung2015/QuantDinger` fork
  - 当前仓库仍直接跟踪上游 `brokermr810/QuantDinger`

## 3. 当前工作区风险边界

以下文件在建立基线时已经是未提交状态，不属于本轮中国市场方案的默认改动范围:

- `README.md`
- `frontend/dist/index.html`

后续任何功能分支都不得无意覆盖、回退或重新生成这两处改动，除非明确确认其来源和用途。

## 4. 本地部署基线

当前部署形态为 Docker Desktop 主栈，本地访问与容器状态如下:

- 前端:
  - 容器名: `quantdinger-frontend`
  - 镜像名: `quantdinger-frontend`
  - 访问地址: `http://localhost:8888`
  - 端口映射: `0.0.0.0:8888 -> 80/tcp`
  - 状态: `healthy`
- 后端:
  - 容器名: `quantdinger-backend`
  - 镜像名: `quantdinger-backend`
  - 地址: `127.0.0.1:5000`
  - 端口映射: `127.0.0.1:5000 -> 5000/tcp`
  - 状态: `healthy`
- 数据库:
  - 容器名: `quantdinger-db`
  - 镜像名: `postgres:16-alpine`
  - 地址: `127.0.0.1:5432`
  - 状态: `healthy`
- Redis:
  - 容器名: `quantdinger-redis`
  - 镜像名: `redis:7-alpine`
  - 地址: `127.0.0.1:6379`
  - 状态: `healthy`

说明:

- 本机还运行了与 QuantDinger 无关的其他容器，例如 `vane`、`nginx-files`、`recoll-webui`。后续核对部署状态时，应只以 `quantdinger-*` 容器为 QuantDinger 主栈依据。
- 当前前端与后端端口与 `docker-compose.yml` 默认配置一致。

## 5. 配置与依赖面

当前后端运行配置来自本地文件:

- `backend_api_python/.env`

后续分析和改动应参考模板文件:

- `backend_api_python/env.example`
- `docker-compose.yml`

当前已确认的重要配置边界:

- `ALLOW_LOCAL_DESKTOP_BROKERS=true`
  - 表示当前部署允许本地桌面券商型集成
  - 这为后续 `QMT Windows bridge` 预留了部署边界
- `SHOW_CN_STOCK=false`
  - 表示当前中国股票市场默认对 UI 隐藏
- 当前模板中已有:
  - `TWELVE_DATA_API_KEY`
  - `AKSHARE_TIMEOUT`
  - `YFINANCE_TIMEOUT`
- 当前模板中没有:
  - `TUSHARE_TOKEN`
  - `ENABLE_TUSHARE`
  - `ENABLE_QMT_BRIDGE`
  - `QMT_BRIDGE_BASE_URL`
  - `QMT_BRIDGE_TOKEN`

安全要求:

- 不在文档中记录 `.env` 的真实密钥值
- 不提交 `.env`
- 后续只记录配置项名称、用途和部署边界，不记录敏感内容

## 6. 当前功能实现边界

本轮中国市场工作以以下原则为准:

- 功能研究与代码修改发生在本地仓库:
  - `D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger`
- 运行验证优先对当前 Docker Desktop 部署做只读核对
- 优先实现:
  - `Tushare` 作为中国市场历史数据主源
- 预留但本轮不实现:
  - `国金 QMT` Windows 本地桥接
- 中国 ETF 目标方向:
  - 独立市场 `CNETF`
  - 不并入 `CNStock`

## 7. 远端与分支约定

本轮只固定约定，不执行远端变更。

目标远端约定:

- `origin = jameshung2015/QuantDinger`
- `upstream = brokermr810/QuantDinger`

建议分支节奏:

- `docs/local-env-baseline`
- `feat/tushare-cn-market`
- `feat/cnetf-market`
- `design/qmt-windows-bridge`

在完成 fork 与远端整理前，不应将中国市场分析记录直接推送到上游 `brokermr810/QuantDinger`。

## 8. 后续执行顺序

建议按以下顺序推进:

1. 先完成 fork 与远端整理
2. 保留当前脏工作区不动，确认其来源
3. 以本文件为基线建立修改记录
4. 从 `Tushare` 开始做中国市场数据接入
5. 在 `Tushare` 稳定后再扩展 `CNETF`
6. 最后补 `QMT Windows bridge` 设计文档和接口契约

## 9. 文档关系

本文件与以下文档共同构成本轮中国市场工作的最小文档集合:

- `docs/LOCAL_ENV_BASELINE_CN.md`
- `docs/CN_TUSHARE_QMT_MODIFICATION_LOG_CN.md`
- `docs/CN_TUSHARE_CNETF_IMPLEMENTATION_PLAN_CN.md`
