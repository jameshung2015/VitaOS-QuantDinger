# QuantDinger 中国市场增强实施方案

## 1. 目标

为 QuantDinger 增加一条清晰、可维护的中国市场技术路线:

- `Tushare` 负责 `CNStock` 与 `CNETF` 的历史数据、基础信息、研究与回测
- `QMT` 负责实时校验、账户读取与执行入口
- 中国 ETF 独立建模为 `CNETF`
- 当前 `Docker Desktop` 主栈保持不动
- `QMT` 采用 Windows 本地桥接预留，但本轮不实现

## 2. 当前现状

已确认的现状如下:

- 当前仓库内存在 `CNStock` 市场数据通道
- 当前 `CNStock` 默认对 UI 和 Agent API 隐藏
- 当前中国市场数据链路主要是:
  - `TwelveData`
  - `Tencent`
  - `yfinance`
  - `AkShare`
- 当前仓库内没有实际接入:
  - `Tushare`
  - `xtquant`
  - `QMT`
- 当前中国市场种子数据只有 A 股个股，没有独立中国 ETF 市场模型

## 3. 目标架构

### 3.1 市场划分

- `CNStock`
  - A 股个股
- `CNETF`
  - 沪深场内 ETF

不采用把 ETF 继续混入 `CNStock` 的做法，以免后续在搜索、展示、分析与执行上持续混淆。

### 3.2 数据职责

- `Tushare`
  - 历史日线
  - 历史分钟线
  - 基础信息
  - ETF 元数据
  - 研究与回测主数据源
- `QMT`
  - 实时行情校验
  - 账户与持仓读取
  - 下单与撤单

### 3.3 部署职责

- `Docker Desktop`
  - 继续承载 QuantDinger 前端、后端、Postgres、Redis
- `Windows 本地`
  - 未来承载 `QMT bridge`
  - 由桥接服务与 `xtquant/xtdata` 交互

## 4. 实施阶段

## Phase 0

- 建立本地环境基线说明
- 建立统一修改记录
- 固定远端与分支约定

本阶段只做文档与边界固定，不做功能实现。

## Phase 1

- 接入 `Tushare`
- 将 `CNStock` 历史数据主链路改为:
  - `Tushare -> 现有 fallback`
- 增加中国市场相关配置项:
  - `ENABLE_TUSHARE`
  - `TUSHARE_TOKEN`
- 统一中国证券代码格式:
  - `600519.SH`
  - `159915.SZ`

## Phase 2

- 新增独立市场 `CNETF`
- 完成以下能力:
  - ETF 市场枚举
  - ETF 搜索
  - ETF 观察列表
  - ETF K 线
  - ETF 元数据
  - ETF 分析入口

## Phase 3

- 增补 `QMT Windows bridge` 设计文档
- 定义后端到桥接层的接口契约
- 明确部署要求、错误语义与降级策略

本阶段只做设计，不写执行代码。

## 5. 设计约束

### 5.1 远端约束

- 后续应将协作远端切换为:
  - `origin = jameshung2015/QuantDinger`
  - `upstream = brokermr810/QuantDinger`
- 不应直接在上游仓库上记录试验性分析或本地环境文档

### 5.2 配置约束

- 不在文档中记录真实密钥
- 不提交 `backend_api_python/.env`
- 所有新增配置项都先写入 `env.example`

### 5.3 数据职责约束

- `Tushare` 是中国市场历史数据主源
- `QMT` 是实时与执行预留项，不是研究主数据源
- `CNETF` 不能退回为 `CNStock` 的一个模糊子类型

### 5.4 风险约束

- 当前本地仓库已有脏工作区:
  - `README.md`
  - `frontend/dist/index.html`
- 后续功能分支不得无意覆盖这两项

## 6. 接口预留

本轮只固定接口方向，不实现。

### 6.1 后端配置项

- `ENABLE_TUSHARE`
- `TUSHARE_TOKEN`
- `ENABLE_QMT_BRIDGE`
- `QMT_BRIDGE_BASE_URL`
- `QMT_BRIDGE_TOKEN`

### 6.2 桥接接口族

- `/bridge/qmt/quote`
- `/bridge/qmt/klines`
- `/bridge/qmt/account`
- `/bridge/qmt/positions`
- `/bridge/qmt/order`
- `/bridge/qmt/cancel`

### 6.3 市场枚举

- `CNStock`
- `CNETF`
- `HKStock`
- `USStock`
- `Crypto`
- `Forex`
- `Futures`
- `MOEX`

## 7. 验证要求

### 7.1 基线验证

- 基线文档准确记录本地路径、远端、分支、脏工作区和 Docker 运行态

### 7.2 Tushare 验证

- `CNStock` 优先命中 `Tushare`
- 在 `Tushare` 不可用时有明确降级路径

### 7.3 CNETF 验证

- `CNETF` 可被搜索、可看图、可分析
- ETF 与 A 股个股不会混市场

### 7.4 QMT 设计验证

- 文档能清晰回答:
  - 桥接服务跑在哪里
  - Docker 主栈如何调用
  - 失败时如何降级
  - 哪些能力本轮不实现

## 8. 当前结论

当前最合理的执行顺序是:

1. 固定本地环境基线
2. 优先实现 `Tushare`
3. 再实现独立市场 `CNETF`
4. 最后补 `QMT Windows bridge` 设计，不落实现

这一路径能在不扰动当前 Docker 主栈的前提下，先把中国市场研究链路做稳，再为未来的本地券商执行留出干净接口。
