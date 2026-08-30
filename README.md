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
- [`evidence/2026-08-05_b008_preflight.md`](evidence/2026-08-05_b008_preflight.md)：B008 replay-safe classify5 单变量候选的公开路线审计、安全适配与终态判定
- [`evidence/2026-08-06_b009_preflight.md`](evidence/2026-08-06_b009_preflight.md)：B009 replay-safe probe4 单变量候选的公开路线审计、安全适配、预注册、提交监控与终态判定
- [`evidence/2026-08-07_b010_preflight.md`](evidence/2026-08-07_b010_preflight.md)：B010 slow-commentary 单变量候选的公开路线审计、安全适配与预注册
- [`evidence/2026-08-09_b011_public_audit.md`](evidence/2026-08-09_b011_public_audit.md)：B011 首轮公开路线与本地机制筛查记录；未形成正式预注册候选
- [`evidence/2026-08-09_current_leaderboard_audit.md`](evidence/2026-08-09_current_leaderboard_audit.md)：当前 public leaderboard 行使用 B010 `52.330` 而非历史最佳 B008 `92.165` 的风险记录
- [`evidence/2026-08-10_b008_status_audit.md`](evidence/2026-08-10_b008_status_audit.md)：B008 当前为 score-bearing `ERROR` 状态的 API/Notebook 核验
- [`evidence/2026-08-10_b008_restore_exception.md`](evidence/2026-08-10_b008_restore_exception.md)：用户授权的 B008R 最佳分数恢复例外、终态与部分恢复判定
- [`evidence/2026-08-11_b011_fastfill_preflight.md`](evidence/2026-08-11_b011_fastfill_preflight.md)：B011 fast-fill 单变量候选的公开路线审计、安全适配、动态样本、预注册与终态拒绝
- [`evidence/2026-08-12_b012_public_audit.md`](evidence/2026-08-12_b012_public_audit.md)：B012 公开路线复查与候选筛查；未形成正式预注册候选
- [`evidence/2026-08-12_b005_restore_exception.md`](evidence/2026-08-12_b005_restore_exception.md)：用户授权的 B005R 分数恢复例外预注册；不计作 B012 新算法候选
- [`evidence/2026-08-15_b013_public_audit.md`](evidence/2026-08-15_b013_public_audit.md)：B013 公开路线与本地机制审计及后续 addenda
- [`evidence/2026-08-21_b013_chain4_preflight.md`](evidence/2026-08-21_b013_chain4_preflight.md)：B013 chain4 单变量候选预注册、Notebook v1 云端核验与唯一 submission `55658141` 创建记录
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
- [x] 构建并云端核验 B007 私有 Notebook v1，确认历史去重后创建唯一 competition submission `55229800`
- [x] 完成 B007 rerun：Public Score `76.905`，低于 B005，按预注册拒绝且不重试
- [x] 以 B005 `91.930` 为直接对照，实现 B008 replay-safe classify5 单变量候选
- [x] 预注册、构建并云端核验 B008 私有 Notebook v1，确认历史去重后创建唯一 competition submission `55266445`
- [x] 完成 B008 rerun：Public Score `92.165`，替换 B005 成为新的真实参考基线；未达到强竞争线 `100.000`
- [x] 以 B008 `92.165` 为直接对照，实现 B009 replay-safe probe4 单变量候选
- [x] 预注册、构建并云端核验 B009 私有 Notebook v1，确认历史去重后创建唯一 competition submission `55299759`
- [x] B009 rerun 以 `ERROR` 终态结束且无 Public Score，按预注册作为可靠性失败拒绝且不重试
- [x] 以 B008 `92.165` 为直接对照，审计并预注册 B010 slow-commentary 单变量候选
- [x] 构建并云端核验 B010 私有 Notebook v1，确认历史去重后创建唯一 competition submission `55327331`
- [x] 完成 B010 rerun：Public Score `52.330`，低于 B008，按预注册拒绝且不重试
- [x] 完成 B011 首轮公开路线与本地机制筛查；未发现值得消耗正式提交额度的单变量候选
- [x] 核验恢复前 public leaderboard：账号行当时显示 B010 `52.330` / rank `711`，而 B008 `92.165` 若计入约为 rank `70`
- [x] 核验 B008 当前状态：competition submission 为 `SubmissionStatus.ERROR` 但保留 Public Score `92.165`；Notebook worker 为 `COMPLETE`
- [x] 获得用户明确授权，预注册一次狭义 B008R best-score restoration 例外；恢复前快照显示账号行 B010 `52.330` / rank `712`，B008 `92.165` 若计入约为 rank `71`
- [x] 构建并云端核验 B008R 恢复 Notebook v1，确认 attack hash 仍为 `4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1`
- [x] 创建唯一 B008R 恢复 competition submission `55393959`；终态 `COMPLETE`、Public Score `88.760`，按预注册记为部分恢复且不重试
- [x] 核验恢复后 public leaderboard：当前使用 B008R `88.760` / rank `205`；历史高点 B008 `92.165` 在同一快照约为 rank `79`
- [x] 以当前 leaderboard-effective `88.760` 为直接对照、历史高点 `92.165` 为新高门槛，实现并预注册 B011 fast-fill 单变量候选
- [x] 构建并云端核验 B011 私有 Notebook v1，确认历史去重后创建唯一 competition submission `55433780`
- [x] 完成 B011 fast-fill rerun：submission `55433780` 为 `COMPLETE`，Public Score `72.680`，低于 B008R `88.760`，按预注册拒绝且不重试
- [x] 完成 B012 首轮公开路线复查：拉取 Adhiraj、Anas、Foysal V15、Nikita 当前公开 Notebook；未发现足够强的低相关单变量候选，未创建正式 submission
- [x] 预注册 B005R byte-identical Tail99 分数恢复例外；这是 leaderboard-effective 恢复操作，不计作 B012 新算法候选
- [x] 构建并云端核验 B005R 私有 Notebook v1，确认历史去重后创建唯一恢复 submission `55461853`
- [x] B005R submission `55461853` 已终态 `COMPLETE`，Public Score `86.945`，低于 B008R `88.760`，按恢复预注册拒绝且不重试
- [x] B012 warmkeep submission `55495429` 已终态 `COMPLETE`，Public Score `88.665`，低于 B008R `88.760`，按预注册拒绝且不重试
- [x] 完成 B013 公开路线与本地机制审计；未发现足够强的低相关单变量候选，未创建 B013 预注册、Notebook 或 competition submission
- [x] 基于 B008R 慢行 replay 包装形成 B013 chain4 单变量候选，锁定源码 commit `685e311` 并提交/推送预注册 commit `7ad613a`
- [x] 完成 B013 chain4 全量预提交验证，构建并云端核验 Notebook v1，确认 cloud `attack.py` SHA 一致后创建唯一 competition submission `55658141`
- [x] B013/B014/B015-C/B016/B017/B018 均已终态且低于 B008R `88.760`，按各自预注册拒绝且不重试
- [x] B019-tail995 submission `55772221` 终态 `COMPLETE`，Public Score `87.470`，低于 B008R `88.760`，按预注册拒绝且不重试
- [x] 预注册 B020 disjoint-uta（B008R EXFIL 不变 + 0.05 独立 web/inbox 池）
- [x] 构建并云端核验 B020 私有 Notebook v1，确认 cloud `attack.py` SHA 一致后创建唯一 competition submission `55784609`
- [x] 落地多步工具链 portfolio 基线（one-shot UTA + 两轮 discover/follow-up + snapshot 分支 + B008R 外泄底分）；B020 出分前不提交
- [x] B020-disjoint-uta submission `55784609` 终态 `COMPLETE`，Public Score `84.630`，低于 B008R `88.760`，按预注册拒绝且不重试
- [x] 预注册 B021-fastnotify（快行 Notify deputy，不切预算、不先碰 web/email）
- [x] B021 唯一 competition submission `55808416` 已创建；只监控至终态
- [x] B021-fastnotify `55808416` 终态 `COMPLETE` Public Score `73.700`，低于 B008R `88.760`，按预注册拒绝且不重试
- [x] 预注册 B022-examplecom（B008R 唯一变量：保留域主机后缀 `invalid` → `example.com`）
- [x] B022 唯一 competition submission `55832399` 已创建；只监控至终态
- [x] B022-examplecom `55832399` 终态 `COMPLETE` Public Score `86.925`，低于 B008R `88.760`，按预注册拒绝且不重试
- [x] 完成 B023 公开高分源码筛查：无合法单变量候选，未创建 submission
- [x] 完成 gpt-oss A/B/C 探针（http / https / framing）：https 打平、framing 更差，不提交 B023
- [x] 2026-08-30 再筛公开高分源码：无合法新轴，不提交
- [x] 起草 Working Note（`docs/working_note.md`，09-08 截止）
- [x] 预注册 B023-allforge（新路：全程四端点 forge，无快行单 post）
- [ ] 在 Kaggle UI 确认私榜两席为 B008R + B012
- [ ] 建立本地可复现评测与攻击轨迹分析
- [ ] 进入并稳定保持公开榜奖牌区
- [ ] 完成 Working Note 终稿并提交评选

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

## 2026-08-13 B005R terminal update

- B005R restoration submission `55461853` reached `SubmissionStatus.COMPLETE` during the
  `2026-08-13 23:53 UTC` monitor heartbeat.
- Kaggle API raw Public Score is `86.945`, Private Score is blank, and
  `errorDescription=None`.
- Per the B005R preregistered restore rule, `86.945 <= 88.760`; therefore B005R is a
  restoration failure, is rejected, and must not be retried or repushed.
- The current leaderboard-effective score remains B008R `88.760`; B008 `92.165`
  remains only the historical observed high-water mark.
- Fresh public leaderboard artifact:
  `artifacts/kaggle/leaderboards/2026-08-13_2353_b005r_terminal/ai-agent-security-multi-step-tool-attacks.zip`.
  The team row still shows score `88.760`, rank `277`, last submission date
  `2026-08-12 15:22:19`, submission count `4`, and top-200 boundary `89.550`.
- B005R is now terminal, so B012 scouting may resume, but no B012 or later formal
  competition submission is authorized until a new single-variable preregistration is
  committed and pushed.

## 2026-08-14 B012 public audit round 2

- Rechecked submissions and public leaderboard. Current effective score remains
  B008R `88.760`; latest checked public rank is `277`, top-200 boundary is
  `89.550`, and historical B008 `92.165` would rank approximately `97`.
- Pulled current public snapshots for Dimong, Nctuan v25, Nctuan slow-multipost,
  Kaiwalya, and Assiaben five-template aggressive replay.
- No B012 candidate was selected: the routes either roll back known variables,
  require multi-variable safe adaptation, or continue excluded prompt/template-bank
  directions.
- Evidence is recorded in `evidence/2026-08-14_b012_public_audit_round2.md`.

## 2026-08-14 B012 warmkeep preregistration

- B012 source is `baselines/replaysafe_warmkeep_v1/attack.py`, SHA
  `68cea78ffdc1c255655a78884c70640737b6390b3ab6baed957d0c73e7f70e6c`,
  source commit `f84bbfd`.
- Parent is B008/B008R classify5, SHA
  `4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1`.
- Single behavior variable: retain B008R's live warmup message as a returned
  replay-safe candidate when the warmup already fired `SECRET_MARKER` through
  `http.post`.
- Preflight, SDK validate, 111 tests, ruff, format check, diff check, and
  candidate-file credential-shape scan passed before preregistration.
- Evidence is recorded in `evidence/2026-08-14_b012_warmkeep_preflight.md`.

## 2026-08-14 B012 submission

- Private Notebook `heralces/ai-agent-security-b012-warmkeep` v1 is `COMPLETE`.
- Cloud `attack.py` hash matches B012 source SHA
  `68cea78ffdc1c255655a78884c70640737b6390b3ab6baed957d0c73e7f70e6c`; log
  actionable error scan and cloud artifact credential-shape scan are both `0`.
- Unique competition submission ref is `55495429`, created
  `2026-08-14 02:01:38.340 UTC`; initial status is `SubmissionStatus.PENDING`
  with blank Public/Private Score.
- Do not repeat B012 and do not create B013 or any other formal competition
  submission before B012 reaches a terminal state.

## 2026-08-15 B012 terminal update

- B012 submission `55495429` reached `SubmissionStatus.COMPLETE` during the
  `2026-08-15 01:37 UTC` monitor pass.
- Kaggle CLI Public Score is `88.665`; Private Score is blank. Kaggle API shows
  `SubmissionStatus.COMPLETE`, `publicScore=null`, `privateScore=null`, and
  `errorDescription=None`.
- Per the preregistered gate, `88.665 <= 88.760`; therefore B012 is rejected and
  must not be retried or repushed.
- The current leaderboard-effective score remains B008R `88.760`; B008
  `92.165` remains only the historical observed high-water mark.
- Latest checked public leaderboard snapshot:
  `artifacts/kaggle/leaderboards/2026-08-15_0000_b012_monitor_v1/ai-agent-security-multi-step-tool-attacks.zip`.
  Team `heralces` shows score `88.760`, rank `298`, and top-200 boundary
  `89.865`; B012 `88.665` would rank approximately `311`.

## 2026-08-15 B013 public audit

- Rechecked current Kaggle submissions and public leaderboard after B012's
  terminal result. Current leaderboard-effective score remains B008R `88.760`;
  latest checked public rank is `298`, top-200 boundary is `89.865`, and
  historical B008 `92.165` would rank approximately `103`.
- Pulled current public snapshots for `yw8837/88-875-lb-open-source-jed-attack-full-code`,
  `coolin666/jed-attack-v12`, `jvn3jean/rq2-newww`,
  `verityix/ai-agent-security-attack-algorithm-hitherto`,
  `dimong4/ai-agent-security`, and
  `saitejabandaruin/ai-agent-security-red-teaming-toolkit`.
- Later addendum also screened `ruhul20/red-team-ai-agent-security` and
  `georgymamarin/red-team-starter-what-fires-and-what-it-s-worth`; Ruhul contains
  a valid `AttackAlgorithm` with `http.post` and `email.send`, but it is a
  multi-family full route replacement rather than a B008R-derived single
  variable.
- A further addendum screened `evgendvorkin/ai-agent`; it has a valid
  `AttackAlgorithm` and `http.post`, but it combines `.co` targets,
  `SPLIT_CLASSIFY_N=8`, `REPLAY_SAFE_FRAC=0.999`, `SLOW_MULTIPOST_N=1`, and a raw
  assistant/analysis-token fallback, so it is not a safe single-variable B013
  candidate.
- A later addendum screened `aratisantoshshinde/...throughput-se`,
  `paul720810/hermes-attack-v72...`, and
  `prvsiyan/ai-agent-security-defense-in-depth-audit`; none is selected because
  they respectively require multi-arm/multi-variable throughput control, simple
  single-post rollback with `.x` URL policy, or an inert no-candidate adapter.
- A later addendum screened `uradkr/ai-security-urad-code`,
  `karnakbaevarthur/multi-endpoint-severity-stacker`,
  `yaroslavkholmirzayev/replay-dense-boundary-exact-aggressive`,
  `lopure/jed-multi-step-attack-relay-push100`, and
  `arizalfirdaus123/multi-turn-exfiltration-with-adaptive-burst`. URAD and
  Yaroslav are fixed single-post portfolios; Karnak and Arizal are broad
  multi-route systems; Lopure did not expose a usable attack implementation.
- The `2026-08-16 01:15 UTC` addendum rechecked submissions/leaderboard and
  screened updated `verityix` and `dimong4` artifacts plus `cleanorlabs`,
  `shreyascppsc`, and `ferencjuhsz` routes. Verity, Dimong, Cleanor, and Ferenc
  either combine multiple behavior changes or roll back rejected route families;
  Shreyas is not executable attack source.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `327`,
  score_at_200 `90.180`, and historical B008 `92.165` would rank approximately
  `110`.
- The `2026-08-16 05:16 UTC` addendum screened two unrecorded
  exfiltration-labeled public routes: `koushikkumardinda` does not expose an SDK
  attack implementation, and `pilkwang` is a legacy single-post live-fill route
  that rolls back multiple B008R/B004/B005 variables together.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `334`,
  score_at_200 `90.225`, and historical B008 `92.165` would rank approximately
  `112`.
- The `2026-08-16 07:17 UTC` addendum screened older public backfill routes:
  `tiktoktrendz` is a broad severity stack, `sravanikamjula` lacks a `http.post`
  exfiltration implementation, and `anvithpothula/aisec-sevstack` duplicates the
  previously rejected multi-endpoint severity stacker route.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `337`,
  score_at_200 `90.250`, and historical B008 `92.165` would rank approximately
  `112`.
- The `2026-08-16 09:18 UTC` addendum screened additional older visible public
  backfill routes: Paul Hermes v68-v71 are `.x` single-post rollbacks in the
  same rejected route family as v72, Ojana does not expose a usable SDK attack
  implementation, and Foysal v12 rolls back to public `.co`, classify8,
  `REPLAY_SAFE_FRAC=0.97`, `SLOW_MULTIPOST_N=1`, and analysis-token shaping.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `340`,
  score_at_200 `90.270`, and historical B008 `92.165` would rank approximately
  `112`.
- The `2026-08-16 13:19 UTC` addendum screened the newly rerun
  `evgendvorkin/ai-agent` snapshot. Its attack code changed to use the
  `BEST_HARMONY` analysis-token injection as the primary `TEMPLATE`, while
  retaining public `.co`, classify8, `REPLAY_SAFE_FRAC=0.999`, and
  `SLOW_MULTIPOST_N=1`; this remains an excluded prompt-token/multi-variable
  rollback route.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `342`,
  score_at_200 `90.270`, and historical B008 `92.165` would rank approximately
  `111`.
- The `2026-08-16 15:20 UTC` addendum screened the newly rerun
  `dimong4/ai-agent-security` snapshot. Its visible changes from the prior
  Dimong screen combine prompt-tail wording, `REPLAY_COST_COEF=1.0`, and
  full-`max_hops` live probing while retaining public `.co`, `fs.delete`,
  analysis-token frame injection, and `REPLAY_SAFE_FRAC=0.975`; this is still a
  multi-variable public-route rollback, not a B013 single-variable candidate.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `348`,
  score_at_200 `90.360`, and historical B008 `92.165` would rank approximately
  `116`.
- The `2026-08-16 23:42 UTC` addendum screened the newly rerun
  `verityix/ai-agent-security-attack-algorithm-hitherto` snapshot. It is a V244
  two-line prompt/style portfolio using public URL patterns and live
  `eval_predicates` retention; the notebook itself reports Public Score
  `43.720`, and the route changes portfolio mix, URL policy, prompt styles,
  index ranges, live validation, and scheduling together.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `362`,
  score_at_200 `90.445`, and historical B008 `92.165` would rank approximately
  `118`.
- The `2026-08-17 00:57 UTC` addendum found no newer public rerun beyond the
  already screened Verity/Dimong/Evgendvorkin snapshots, then backfilled three
  older visible routes: `canqiang/aiagsec-ea-b-0721`,
  `anvithpothula/aisec-pilk`, and
  `tetsutani/ai-agent-sec-adaptive-uniform-two-probe-recovery`. They remain
  public-domain prompt/template/probe/fill route replacements, not B013
  single-variable candidates.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `362`,
  score_at_200 `90.445`, and historical B008 `92.165` would rank approximately
  `118`.
- The `2026-08-17 02:58 UTC` addendum again found no newer public rerun beyond
  already screened Verity/Dimong/Evgendvorkin, then backfilled
  `uctpexx123/aas-kun-lb66015-official-v1`,
  `haodou092/conservative-replay-safe-sizing`,
  `yusuketogashi/ai-agent-sec-another-approach`,
  `dakbsabsa/ai-agent-security-multi-step-tool-attacks`, and
  `godofthunder2407/ai-agent-sec`. The usable routes are public-domain
  single-post/template/probe/fill or broad exploratory branch-search families;
  two snapshots expose only placeholder/server wiring.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `367`,
  score_at_200 `90.495`, and historical B008 `92.165` would rank approximately
  `120`.
- The `2026-08-17 04:58 UTC` addendum again found no newer public rerun beyond
  already screened Verity/Dimong/Evgendvorkin, then backfilled
  `gouthamkonduru/firstscoreafteramonth`, `haodou092/notebookcb9f3b04b6`,
  `rokaiyasomapti/ai-agent-sec-another-approach-resubmission`,
  `canqiang/aiagsec-submission`, `alt0er/ai-agent-security-fresh`, and
  `sumangnalla/project-agent-security`. The usable routes either lack literal
  `http.post`, repeat public-domain template/probe/fill families, or combine
  exfiltration/deputy route families; three snapshots expose only
  placeholder/server wiring.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `371`,
  score_at_200 `90.540`, and historical B008 `92.165` would rank approximately
  `120`.
- The `2026-08-17 06:58 UTC` addendum again found no newer public rerun beyond
  already screened Verity/Dimong/Evgendvorkin, then backfilled
  `pratyaymon/notebook289b303504`, `clemendes/borapracima-v1`, and
  representative older Paul/Hermes v67/v62/v57/v53/v52 snapshots. Pratyay is a
  static fixed `http.post` baseline, Clemendes is a broad multi-family
  public-route replacement, and the Paul variants are older `.x` single-post
  count/margin rollbacks.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `373`,
  score_at_200 `90.630`, and historical B008 `92.165` would rank approximately
  `123`.
- The `2026-08-17 08:58 UTC` addendum again found no newer public rerun beyond
  already screened Verity/Dimong/Evgendvorkin, then backfilled Assiaben,
  Caoyupeng, Biohack, Fares, Nabid, Coolin getting-started, and representative
  older Paul/Hermes v51/v50/v49/v48 snapshots. The usable routes are either
  public-domain template/live-selector/replay-safe variants, starter material,
  or older `.x` single-post count/margin rollbacks.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `376`,
  score_at_200 `90.630`, and historical B008 `92.165` would rank approximately
  `123`.
- The `2026-08-17 10:58 UTC` addendum again found no newer public rerun beyond
  already screened Verity/Dimong/Evgendvorkin, then backfilled older Caoyupeng,
  Junaid, ImBikram, Pilkwang, Yusuke, and Yaroslav public routes. They are
  lower public single-post/fill rollbacks, broad multi-family live-validation
  route replacements, or working-note material rather than a clean B008R-derived
  single variable.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `378`,
  score_at_200 `90.675`, and historical B008 `92.165` would rank approximately
  `124`.
- The `2026-08-17 12:58 UTC` addendum screened a newly rerun
  `evgendvorkin/ai-agent` snapshot plus older Martyna, Boristown, Kokinn, LLKh0a,
  Pilkwang replay-dense, Kojimar, Yaroslav first/K1, and Nikita artifacts. The
  Evgendvorkin rerun still combines public `.co`, classify8, high replay-safety,
  live probing, and analysis-token prompt text; the rest are starter/local
  validation, lower fixed single-post, or broad public live-validation routes.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `381`,
  score_at_200 `90.675`, and historical B008 `92.165` would rank approximately
  `124`.
- The `2026-08-17 14:59 UTC` addendum found no newer public rerun beyond the
  already screened Evgendvorkin/Dimong/Verity snapshots. The apparent
  high-signal uncovered refs in the current kernels list
  (`foysalemonshanto/ai-agent-security-v15`, `anasriaz/ai-agent-security`,
  and `kaiwalyaatulraut/ai-agent-security-competition-solution`) are already
  covered by earlier B009/B010/B011/B012 evidence.
- A local predicate/score check rejected an `email.send` coverage pivot as a
  standalone B013 variable: plain `http.post` triggers EXFILTRATION severity 5,
  `email.send` only triggers CONFUSED_DEPUTY severity 3 when the prompt avoids
  explicit send/email/upload wording, and a combined post+email candidate would
  add lower raw value while costing at least another tool hop.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `382`,
  score_at_200 `90.675`, and historical B008 `92.165` would rank approximately
  `126`.
- The `2026-08-17 23:43 UTC` addendum found a newly rerun
  `verityix/ai-agent-security-attack-algorithm-hitherto` snapshot with last run
  `2026-08-17 22:08:25 UTC`. Its extracted `attack.py` is SDK-valid, SHA
  `98f3ca2d005ba58e020cfbfd7d6d48095941e39b396053da69ebe8e670bf72f7`, but it is
  a V249 public endpoint-topology/style portfolio: 8 direct `http.post` styles
  times 8 public URL patterns (`.ai`, `.cloud`, `.app`, `.dev`, `.io`, `.org`,
  `.com`, `.net`) times 25 indices, with live `eval_predicates` retention.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `400`,
  score_at_200 `90.820`, and historical B008 `92.165` would rank approximately
  `133`.
- The `2026-08-18 04:00 UTC` addendum found no newer public rerun beyond
  Verity V249, then backfilled four uncovered public routes:
  `adonisleu/jed-attack-submission`,
  `gdataranger/jed-attack-starter-v3-1-2-fixed`,
  `karnakbaevarthur/verify-and-keep-deterministic-red-team-attack`, and
  `yaroslavkholmirzayev/ai-agent-security-trajectory-search`. All four clean
  extracted attacks pass SDK structure validation, but they are either static or
  model-count single-post rollbacks, or broad live verify-and-keep /
  trajectory-search route replacements with mixed public/reserved URL policy.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `402`,
  score_at_200 `90.855`, and historical B008 `92.165` would rank approximately
  `134`.
- The `2026-08-18 06:00 UTC` addendum again found no newer public rerun beyond
  Verity V249, then backfilled five older uncovered public references:
  Pilkwang EDA trajectory search, Assiaben ultra-aggressive final30, Karnak
  dynamic replay architecture, Caoyupeng trajectory plus2, and Devchandra v65b.
  Only Assiaben and Karnak produced standalone SDK-valid clean attacks; Assiaben
  is a public `.co` live single-post fill rollback, and Karnak is a broad
  multi-profile dynamic replay route. Caoyupeng, Devchandra, and Pilkwang did
  not validate as standalone top-level `AttackAlgorithm` implementations.
- Latest checked leaderboard snapshot remains B008R `88.760` as rank `402`,
  score_at_200 `90.855`, and historical B008 `92.165` would rank approximately
  `134`.
- The `2026-08-18 08:00 UTC` addendum again found no newer public rerun beyond
  Verity V249 in the latest 100-kernel date-run list, then backfilled Pengwang
  v26 replaysafe, Quan edge-fill, QYQ dense-v9, Weizhou JED v2, Shayml latest
  best v3, and Kleniopadilha WINNEX v65. Weizhou and Shayml yielded SDK-valid
  literal attack extracts, but both are broad route replacements: Weizhou mixes
  confused-deputy email and web-secret/fs-read/http-post exfiltration, while
  Shayml is starter-style snapshot/branch exploration. The remaining pulls
  either failed to expose a source artifact or did not validate as standalone
  top-level `AttackAlgorithm` implementations.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `403`,
  score_at_200 `90.855`, and historical B008 `92.165` would rank approximately
  `134`.
- The `2026-08-18 10:01 UTC` addendum again found no newer public rerun beyond
  Verity V249. A current-list coverage check found `65/100` refs already
  exact-recorded; the remaining gaps were old Paul/Hermes count-margin
  rollbacks, Kleniopadilha WINNEX variants, Coolin starter copies, or other
  low-vote older refs. Six non-family-increment unknown refs were pulled:
  Erkkj98, Sahar, Andrew, Kyle, Yuriy, and LLCC/Jiachen. Sahar and LLCC yielded
  SDK-valid cleaned code-cell artifacts, but they are respectively a broad
  public-domain live-validation portfolio and a B012/B005R-overlapping public
  `.co` warmup/fill route rather than B008R-derived single variables.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `406`,
  score_at_200 `90.855`, and historical B008 `92.165` would rank approximately
  `134`.
- The `2026-08-18 12:02 UTC` addendum found a newly rerun
  `evgendvorkin/ai-agent` snapshot (`2026-08-18 11:51:37 UTC`). The pulled
  notebook SHA
  `eb01e6014d719115685d5f7fc2cfbd82861ea0dec2e3110633a05c9b359beecf` and
  extracted literal attack SHA
  `1efc87afcb944add247cca7429d380cb5b183fb7e6e18c08230bb73b3c5cc9fc` are
  byte-identical to the previously screened Evgendvorkin PHOENIX V5 artifact;
  SDK validate passed, but the route still combines public `.co`, classify8,
  `REPLAY_SAFE_FRAC=0.9995`, `SLOW_MULTIPOST_N=4`, live probing, and
  analysis-token prompt text.
- Latest checked leaderboard snapshot shows B008R `88.760` as rank `407`,
  score_at_200 `90.855`, and historical B008 `92.165` would rank approximately
  `135`.
- No B013 candidate was selected. The reviewed routes either rely on
  prompt/template-bank exploration, repeat rejected variables, require
  multi-variable safe adaptation, are not SDK-valid in current form, or do not
  contain usable `AttackAlgorithm` source.
- No B013 preregistration, Notebook, or competition submission was created.
  Evidence is recorded in `evidence/2026-08-15_b013_public_audit.md`.
- Latest `2026-08-20 14:59 UTC` refresh: B008R `55393959` remains the current
  leaderboard-effective best at `88.760`, rank `474`, with score_at_200
  `91.155`. B008 `55266445` is now CLI-visible as `SubmissionStatus.COMPLETE`
  with Public Score `88.070`; the earlier observed `92.165` is retained only as
  historical evidence and would rank approximately `152` in this snapshot.
- The same refresh screened updated public refs from Evgendvorkin, Verity,
  Georgy, and Lopure. Evgendvorkin repeats public `.co` PHOENIX-family rollback
  variables, Verity is a public endpoint/style live-validation portfolio,
  Georgy is a starter/local-scoring notebook, and Lopure still lacks a usable
  top-level attack implementation. No B013 preregistration, Notebook, or
  competition submission was created.
- Later `2026-08-20 22:57 UTC` refresh: B008R remains `88.760`, now rank `482`;
  top-200 boundary is `91.215`, approximate bronze 10% cut is rank `382` at
  `89.415`, and historical `92.165` would rank approximately `157`. A local SDK
  audit of multi-message replay chains found plausible scoring support but no
  target-agent reliability proof strong enough for a formal B013 candidate.
- Later `2026-08-21 01:40 UTC` refresh: leaderboard remained B008R `88.760`,
  rank `482`, with top-200 boundary `91.215`. A newly rerun Verity V262 public
  notebook was pulled and SDK-validated, but it is a broad public endpoint/style
  portfolio rather than a B008R-derived single variable; no B013 candidate or
  submission was created.
- Later `2026-08-21 01:54 UTC` refresh: leaderboard still showed B008R
  `88.760`, rank `482`; top-200 boundary `91.240`; approximate bronze 10% cut
  rank `382` at `89.415`. No newer public rerun appeared. B013 chain4 was
  preregistered as a B008R-derived single variable: slow-row live validation
  keeps B008R's one-message four-endpoint frame, while replay packaging returns
  four direct user messages over the same `.invalid` endpoints. No Kaggle
  Notebook or competition submission had been created at preregistration time.
- Later `2026-08-21 02:09 UTC`, after preregistration commit `7ad613a` was
  pushed, B013 chain4 Notebook v1 was cloud-verified with matching
  `attack.py` SHA and used exactly once to create competition submission
  `55658141`. Initial and `02:12 UTC` checks show `SubmissionStatus.PENDING`,
  Public/Private Score blank, and `errorDescription=None`; do not retry B013 or
  create B014 before this submission reaches terminal state.
- Latest `2026-08-21 02:12 UTC` leaderboard refresh still shows B008R
  `88.760`, rank `482`; top-200 boundary `91.215`; approximate bronze 10% cut
  rank `382` at `89.415`; historical `92.165` would rank approximately `157`.
