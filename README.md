# Kaggle LLM Medal Project

本仓库服务于一个明确目标：在与 LLM/Agent 高度相关的 Kaggle 竞赛中获得奖牌或官方奖项，并把全过程沉淀为可核验的求职与深造材料。

## 阅读入口

- [`docs/project_overview.md`](docs/project_overview.md)：竞赛讲解、核心判断、技术路线与当前进度
- [`docs/progress_log.md`](docs/progress_log.md)：按时间追加的阶段成果、证据和下一门槛
- [`experiments/README.md`](experiments/README.md)：单变量实验账本
- [`experiments/offline_ablation_v1.md`](experiments/offline_ablation_v1.md)：第一轮确定性消融
- [`evidence/2026-07-23_b000_v3.md`](evidence/2026-07-23_b000_v3.md)：首次正式提交的脱敏证据
- [`evidence/2026-07-26_e002_preflight.md`](evidence/2026-07-26_e002_preflight.md)：E002 的预注册与提交前证据
- [`evidence/2026-07-27_e005_preflight.md`](evidence/2026-07-27_e005_preflight.md)：E005 有界 Go-Explore 的预注册证据
- [`evidence/2026-07-27_b001_preflight.md`](evidence/2026-07-27_b001_preflight.md)：B001 公开 two-probe 参考基线的来源、适配与预注册
- [`evidence/2026-07-30_b002_preflight.md`](evidence/2026-07-30_b002_preflight.md)：B002 公开 fill-stack 参考基线的来源、适配与预注册
- [`evidence/2026-07-30_b003_local_candidate.md`](evidence/2026-07-30_b003_local_candidate.md)：B003 replay-safe split 参考候选的来源、适配与预注册
- [`evidence/2026-08-01_b004_preflight.md`](evidence/2026-08-01_b004_preflight.md)：B004 slow-row multi-post 单变量候选的来源、适配、预注册与提交监控
- [`evidence/2026-08-02_b005_preflight.md`](evidence/2026-08-02_b005_preflight.md)：B005 replay-safe tail-extension 单变量候选的来源、预算边界、预注册与终态判定
- [`evidence/2026-08-03_b006_preflight.md`](evidence/2026-08-03_b006_preflight.md)：B006 replay-safe threshold8 单变量候选的来源、路由边界与预注册
- [`evidence/2026-08-04_b007_preflight.md`](evidence/2026-08-04_b007_preflight.md)：B007 fast-row direct-burst 单变量候选的公开路线审计、安全适配与预注册
- [`docs/safety.md`](docs/safety.md)：研究授权边界与工程控制

## 当前主赛

**AI Agent Security - Multi-Step Tool Attacks**

- 主办：OpenAI、Google、IEEE
- 类型：Featured Code Competition，授予 Kaggle points 与 medals
- 任务：为沙盒中的工具型 AI Agent 构建可复现的多步攻击搜索算法
- 目标模型：GPT-OSS 与 Gemma 4
- 奖金：$50,000；另有两个 $2,500 Working Note Awards
- 入赛/组队截止：2026-08-25 23:59 UTC
- 最终提交截止：2026-09-01 23:59 UTC（北京时间 2026-09-02 07:59）
- Working Note 截止：2026-09-08 23:59 UTC
- 官方页面：https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks

选择依据见 [`docs/competition_selection.md`](docs/competition_selection.md)，技术路线见 [`docs/strategy.md`](docs/strategy.md)。
授权范围与风险处置见 [`docs/safety.md`](docs/safety.md)。

## 成功标准

按优先级定义：

1. 私榜进入 Kaggle 奖牌区；
2. 获得主榜奖金或 Working Note Award；
3. 即使名次未达目标，也必须产出可复现的研究型代码、严格消融实验和公开技术报告，但这不替代奖牌目标。

## 当前状态

- [x] 审计本机算力与软件资产
- [x] 筛选当前开放且与 LLM 高度相关的竞赛
- [x] 选定主赛并记录硬截止日期
- [x] 保存官方 starter baseline，并用竞赛 SDK 3.1.2 完成确定性管线复现
- [x] 建立离线测试骨架并完成自适应预算调度实验
- [x] 完成按工具调用签名去重的新颖度调度实验
- [x] 完成 source 验证、snapshot 归档与冷重放门控实验
- [x] 建立 submission preflight，验证接口、离线边界与版本摘要
- [x] 建立跨版本确定性消融，量化预算利用、机制覆盖与冷重放失败
- [x] 登录 Kaggle、接受比赛规则并配置新版 API Token
- [x] 下载并校验竞赛 SDK/数据
- [x] 生成并云端成功运行绑定 attack 哈希、Git commit 与实验编号的私有 Notebook version 3
- [x] 创建官方 baseline competition submission `54925726`
- [x] 完成官方 baseline 首次 Kaggle competition rerun（public score `0.075`；private score 当前未返回）
- [x] 预注册 E001 自适应预算实验并通过 preflight、测试和 SDK validate
- [x] 云端验证 E001 私有 Notebook v1，并创建 submission `54952586`
- [x] 完成 E001 单变量 rerun：public score `0.075`，与 B000 相同，未证明提升
- [x] 预注册 E002 机制新颖度调度实验并通过 preflight、测试和 SDK validate
- [x] 云端验证 E002 私有 Notebook v1，并创建唯一 submission `54995012`
- [x] 完成 E002 rerun：public score `0.060`，低于 E001 的 `0.075`，按预注册拒绝变更
- [x] 诊断 E002 的实验边界，放弃把 E002 作为下一候选基础
- [x] 实现 E005 有界 Go-Explore，并通过超时回归、47 项测试和 SDK validate
- [x] 以 E001 `0.075` 为对照预注册 E005
- [x] 云端验证 E005 私有 Notebook v1，并创建唯一 submission `55014937`
- [x] 完成 E005 rerun：真实 public score `0.000`，按预注册拒绝候选
- [x] 调研公开 replay-dense 路线，并建立有明确出处的 B001 two-probe 参考实现
- [x] B001 通过 54 项测试、preflight、Ruff、SDK validate 和本地预算边界验证
- [x] 预注册 B001：第三方 88–89 分仅作来源，真实复现必须等待本账号 rerun
- [x] 云端验证 B001 私有 Notebook v1、核对源码哈希，并创建唯一 submission `55030205`
- [x] B001 rerun 完成：Public Score `65.340`，达到预注册的强复现门槛
- [x] 建立 B002 公共 fill-stack 参考候选并通过 61 项测试、preflight、Ruff 和 SDK validate
- [x] 完成 B002 预注册提交、私有 Notebook 构建、云端哈希核对，并创建唯一 submission `55110969`
- [x] 准备 B003 公开 replay-safe split 后备候选并通过 68 项测试、preflight、Ruff 和 SDK validate
- [x] B002 rerun 以 `COMPLETE` 空分结束，按预注册作为可靠性失败拒绝且不重试
- [x] 以 B001 `65.340` 为直接对照重新预注册 B003，并固定接受、拒绝与竞争门槛
- [x] 构建并云端核验 B003 私有 Notebook v1，创建唯一 submission `55123773`
- [x] 完成 B003 rerun：Public Score `81.585`，替换 B001 成为新的真实参考基线
- [x] 实现 B004 slow-row multi-post 单变量候选，并完成本地预检、SDK validate 与预注册
- [x] 构建并云端核验 B004 私有 Notebook v1，确认历史去重后创建唯一 competition submission `55168834`
- [x] 完成 B004 rerun：Public Score `88.650`，替换 B003 成为新的真实参考基线；未达到固定前 200 参考线 `89.390`
- [x] 以 B004 `88.650` 为直接对照，设计并预注册 B005 replay-safe tail-extension 单变量候选
- [x] 构建并云端核验 B005 私有 Notebook v1，确认历史去重后创建唯一 competition submission `55185029`
- [x] 完成 B005 rerun：Public Score `91.930`，替换 B004 成为新的真实参考基线；达到固定前 200 参考线 `89.390`
- [x] 以 B005 `91.930` 为直接对照，实现并预注册 B006 replay-safe threshold8 单变量候选
- [x] 构建并云端核验 B006 私有 Notebook v1，确认历史去重后创建唯一 competition submission `55203390`
- [x] 完成 B006 rerun：Public Score `80.535`，低于 B005，按预注册拒绝且不重试
- [x] 以 B005 `91.930` 为直接对照，实现并预注册 B007 fast-row direct-burst 单变量候选
- [ ] 构建并云端核验 B007 私有 Notebook，确认历史去重后最多创建一次 competition submission
- [ ] 建立本地可复现评测与攻击轨迹分析
- [ ] 进入并稳定保持公开榜奖牌区
- [ ] 完成私榜提交选择与 Working Note

## 本机资产

- GPU：RTX 4060 Laptop，8 GB VRAM
- CPU：i9-13900HX，24 核 / 32 线程
- RAM：16 GB（需要限制并行数据加载和本地大模型规模）
- 可用 GPU 环境：`C:\Users\21398\Miniconda3\envs\compass-fx`
- 已有栈：PyTorch 2.6 CUDA、Transformers、Datasets、Accelerate、PEFT、bitsandbytes、TRL

本地机器用于 SDK 单测、搜索算法开发和小模型实验；正式 code submission 使用 Kaggle 的隔离运行环境。
Kaggle 普通 GPU Notebook 按每周配额管理；本项目先在本地完成预检，只把必要的短时
构建与验证放到云端，避免用交互空闲或重复 commit 消耗配额。

## 立即行动

账号 onboarding 已完成，验证记录与凭证轮换说明见
[`docs/onboarding.md`](docs/onboarding.md)。重新验证竞赛访问时运行：

```powershell
uv sync
.\.venv\Scripts\kaggle.exe competitions files ai-agent-security-multi-step-tool-attacks
```

任何 API Token 都不得提交到本仓库。

候选版本进入 Kaggle Notebook 前必须通过：

```powershell
.\.venv\Scripts\python.exe .\scripts\preflight_submission.py `
  .\baselines\snapshot_archive_v1\attack.py
```

构建可由 Kaggle CLI 推送的私有 Notebook 包：

```powershell
.\.venv\Scripts\python.exe -m scripts.build_kaggle_notebook `
  .\baselines\official_starter_v17\attack.py `
  .\submissions\B000 `
  --experiment-id B000 `
  --kernel-id heralces/ai-agent-security-b000-official-baseline `
  --title "AI Agent Security B000 Official Baseline"
```
