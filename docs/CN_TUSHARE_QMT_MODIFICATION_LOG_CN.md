# QuantDinger 中国市场改造修改记录

## 记录规则

本文件是中国市场改造的唯一修改记录。记录粒度按阶段维护，不记录零散的临时想法。每条记录都应覆盖以下字段:

- 阶段
- 日期
- 状态
- 关键决策
- 影响面
- 验证结果
- 回退点
- 备注

状态定义:

- `已建立`
- `进行中`
- `已完成`
- `预留未实现`
- `已回退`

## Phase 0 基线

### 记录项

- 阶段: `Phase 0`
- 名称: `本地环境基线建立`
- 日期: `2026-05-12`
- 状态: `已建立`

### 关键决策

- 本地代码研究仓库固定为:
  - `D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\QuantDinger`
- 当前部署固定为:
  - `Docker Desktop` 主栈
- 中国市场优先级固定为:
  - 先做 `Tushare`
  - `QMT` 仅预留 Windows 本地桥接设计，本轮不实现
- 中国 ETF 固定为独立市场目标:
  - `CNETF`
  - 不并入 `CNStock`
- 当前远端现状固定记录:
  - 当前 `origin` 仍指向上游 `brokermr810/QuantDinger`
  - 目标是后续切换到 `jameshung2015/QuantDinger` fork

### 影响面

- 文档层
- 远端协作约定
- 后续分支节奏
- 中国市场改造的先后顺序

### 验证结果

- 已确认当前 Git 分支为 `main`
- 已确认当前提交为 `84d56f27a88ed18454bc0d06a0276620954fb0a5`
- 已确认当前未提交文件:
  - `README.md`
  - `frontend/dist/index.html`
- 已确认 QuantDinger 主栈容器:
  - `quantdinger-frontend`
  - `quantdinger-backend`
  - `quantdinger-db`
  - `quantdinger-redis`
- 已确认前端入口:
  - `http://localhost:8888`

### 回退点

- 本阶段仅建立文档基线，无代码改动
- 如需回退，只需删除本轮新增文档文件

### 备注

- 该阶段不执行 fork
- 该阶段不执行远端切换
- 该阶段不实现 `Tushare`
- 该阶段不实现 `QMT`

### 追加记录 (2026-05-12)

- 事项: `fork 尝试与远端整理`
- 状态: `进行中`

关键结论:

- 已确认本机可用 `gh`:
  - `C:\Program Files\GitHub CLI\gh.exe`
- 已确认登录账号:
  - `jameshung2015`
- 执行 `fork brokermr810/QuantDinger` 时报错:
  - `HTTP 403: Resource not accessible by personal access token`
- 已将本地远端按目标约定整理为:
  - `origin = https://github.com/jameshung2015/QuantDinger.git`
  - `upstream = https://github.com/brokermr810/QuantDinger.git`
- 当前 GitHub 侧尚不存在 `jameshung2015/QuantDinger`，需补齐 `repo` scope 后重试 fork。

当前本地改动快照:

- 已修改:
  - `README.md`
  - `backend_api_python/app/config/api_keys.py`
  - `backend_api_python/app/data_sources/cn_stock.py`
  - `backend_api_python/app/routes/settings.py`
  - `backend_api_python/app/utils/config_loader.py`
  - `backend_api_python/env.example`
  - `frontend/dist/index.html`
- 未跟踪:
  - `backend_api_python/app/data_sources/tushare.py`
  - `backend_api_python/tests/test_cn_stock_tushare.py`
  - `docs/CN_TUSHARE_CNETF_IMPLEMENTATION_PLAN_CN.md`
  - `docs/CN_TUSHARE_QMT_MODIFICATION_LOG_CN.md`
  - `docs/LOCAL_ENV_BASELINE_CN.md`

## Phase 1 Tushare

### 目标

- 将 `Tushare` 固定为中国市场历史数据主源

### 当前状态

- `已完成`

### 记录项

- 阶段: `Phase 1`
- 名称: `CNStock Tushare 主链路接入与 Docker 验证`
- 日期: `2026-05-12`
- 状态: `已完成`

### 关键决策

- `CNStock` 历史 K 线链路调整为:
  - `Tushare -> TwelveData -> Tencent -> yfinance -> AkShare`
- `Tushare` 接入采用后端环境变量控制:
  - `ENABLE_TUSHARE`
  - `TUSHARE_TOKEN`
- 仅在 `env.example` 记录配置项，不在文档记录真实 token。
- fork 已进入权限阻塞阶段（PAT scope），等待补齐 `repo` scope 后完成 GitHub 侧创建。

### 影响面

- `backend_api_python/app/data_sources/cn_stock.py`
- `backend_api_python/app/data_sources/tushare.py`（新增）
- `backend_api_python/app/config/api_keys.py`
- `backend_api_python/app/utils/config_loader.py`
- `backend_api_python/app/routes/settings.py`
- `backend_api_python/env.example`
- `backend_api_python/tests/test_cn_stock_tushare.py`（新增）

### 验证结果

- 已完成 Docker 后端重建并重启。
- 容器内直连 `fetch_tushare_klines(symbol='600519.SH', timeframe='1D', limit=5)` 返回有效数据。
- 接口 `GET /api/indicator/kline?market=CNStock&symbol=600519.SH&timeframe=1D&limit=5` 返回成功且有数据。
- 修复了 Tushare 返回码判定 bug（`code=0` 被误判失败）。

### 回退点

- 如需回退 Phase 1，可还原上述影响文件，并删除新增 `tushare.py` 与 `test_cn_stock_tushare.py`。

### 备注

- 本轮仅进行本地开发和本地 Docker 验证。
- `.env` 中的敏感值不入库、不上传。

### 计划记录点

- `CNStock` 历史数据主链路改造
- `Tushare` 配置项新增
- 降级策略与回退策略
- 验证结果

## Phase 2 CNETF

### 目标

- 新增独立市场 `CNETF`

### 当前状态

- `进行中`

### 记录项

- 阶段: `Phase 2`
- 名称: `CNETF 最小接口落地（枚举/搜索/K线）`
- 日期: `2026-05-12`
- 状态: `进行中`

### 关键决策

- 新增独立数据源实现:
  - `backend_api_python/app/data_sources/cn_etf.py`
  - 复用中国市场多源链路，保持 `Tushare -> TwelveData -> Tencent -> yfinance -> AkShare`。
- 将 `CNETF` 接入数据源工厂与市场别名:
  - `cnetf`
  - `cn_etf`
  - `etf_cn`
- 将 `CNETF` 暴露到市场枚举接口:
  - `/api/market/types`
  - `/api/agent/v1/markets`
- 为当前已运行数据库增加 `CNETF` 搜索可用性:
  - 在 `market_symbols_seed.py` 增加 `CNETF` fallback 热门 ETF 列表
  - 即使 DB 尚未执行新 seed，`/api/market/symbols/search` 也可返回 ETF 结果。

### 影响面

- `backend_api_python/app/data_sources/cn_etf.py`（新增）
- `backend_api_python/app/data_sources/factory.py`
- `backend_api_python/app/routes/market.py`
- `backend_api_python/app/routes/agent_v1/markets.py`
- `backend_api_python/app/data/market_symbols_seed.py`
- `backend_api_python/app/services/symbol_name.py`
- `backend_api_python/app/services/market_data_collector.py`
- `backend_api_python/app/services/trading_executor.py`
- `backend_api_python/app/services/fast_analysis.py`
- `backend_api_python/migrations/init.sql`

### 验证结果

- 已完成 Docker 后端重建并重启。
- `GET /api/market/types` 已包含 `CNETF`。
- `GET /api/market/symbols/search?market=CNETF&keyword=159&limit=5` 返回非空结果。
- `GET /api/indicator/kline?market=CNETF&symbol=159915.SZ&timeframe=1D&limit=5` 返回 `code=1` 且有数据。
- `GET /api/market/etf/meta?market=CNETF&symbol=159915.SZ` 返回 `code=1`，包含 ETF 名称与价格快照。
- `POST /api/fast-analysis/analyze` 在未登录上下文返回 `401 Token missing`（鉴权正常）。
- 容器内 `MarketDataCollector.collect_all(market='CNETF', symbol='159915.SZ')` 返回完整结构（`price/kline/fundamental/company` 均存在）。

### 回退点

- 如需回退本记录项，可移除 `cn_etf.py`，并还原上述影响文件中的 `CNETF` 相关改动。

### 备注

- 本轮已补齐 ETF 元数据接口与分析入口后端能力，前端可基于新接口直接接入 ETF 详情与分析页。

### 计划记录点

- 市场枚举与搜索
- ETF 元数据与 K 线
- 前端入口与分析入口
- 与 `CNStock` 的边界验证

## Phase 3 QMT bridge design

### 目标

- 补齐 `QMT Windows bridge` 的部署设计、接口契约与配置位

### 当前状态

- `预留未实现`

### 计划记录点

- Windows 本地桥接服务边界
- QuantDinger 后端到桥接层的接口定义
- 与 Docker 主栈的协同方式
- 明确本阶段只做设计，不做落地实现
