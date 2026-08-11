# 阶段进展日志

本文件按时间追加项目里程碑，不能只记录成功。每条新记录固定包含：

1. **事实**：UTC 时间、对象/实验 ID 和观测状态；
2. **解释与限制**：这项证据能说明什么、不能说明什么；
3. **证据**：可复现命令、文件、hash、Kaggle version 或 submission ref；
4. **决策**：保留、回滚、继续、停止或 N/A；
5. **下一门槛**：可以明确判定完成或失败的退出条件。

详细的单变量实验数据仍以 [`../experiments/README.md`](../experiments/README.md) 为准。

## 2026-07-22：确定主赛与研究边界

**事实**

- 将 AI Agent Security - Multi-Step Tool Attacks 选为主赛。
- 明确目标是 Kaggle 奖牌或官方奖项，同时沉淀可复现研究材料。
- 建立只允许竞赛 SDK、fixture、保留域和合成秘密的安全边界。

**解释与限制**

- 主赛选择基于技术相关性、奖牌有效性和本地算力匹配，不代表已经获得成绩。
- 所有研究只适用于比赛授权的合成沙盒。

**证据**

- [`competition_selection.md`](competition_selection.md)
- [`strategy.md`](strategy.md)
- [`safety.md`](safety.md)

**决策**

- 保留该主赛；早期低分或实现困难本身不是换赛理由。

**下一门槛**

- 完成账号入赛、API 认证、SDK 下载和官方基线复现。

## 2026-07-23：建立本地机制验证管线

**事实**

- 保存官方 starter baseline。
- 实现 E001 自适应预算、E002 新颖度调度和 E003 snapshot 冷重放门控。
- 建立统一假时钟、fixture 环境和机器可读消融矩阵。
- 适配 SDK 3.1.2 原生 trace 结构，过滤失败工具事件。
- 四个 `attack.py` 版本均通过 SDK validate。

**解释与限制**

- 这些结果证明预算、去重和冷重放机制在确定性 fixture 中按设计工作。
- 它们不包含目标模型、隐藏 fixture 或 guardrail，不能证明榜单提升。

**证据**

- 220 秒模拟预算下，adaptive 版本执行 12 次交互，官方基线为 4 次。
- 新颖度调度在减少重复 finding 的同时保留 4 种机制覆盖。
- snapshot 门控在故意制造的冷重放失败场景中将不可重放 finding 从 2–3 条降至 0。
- 当前测试总数为 42。
- [`../experiments/offline_ablation_v1.md`](../experiments/offline_ablation_v1.md)
- [`../experiments/offline_ablation_v1.json`](../experiments/offline_ablation_v1.json)
- [`../baselines`](../baselines)
- [`../tests`](../tests)
- [`../evidence/2026-07-23_b000_v3.md`](../evidence/2026-07-23_b000_v3.md)

**决策**

- 保留 E001–E003 作为待单变量提交的候选；E004 作为跨版本契约修复，不单独计为算法版本。

**下一门槛**

- 完成官方基线的 Kaggle competition rerun。

## 2026-07-23：打通 Kaggle Notebook 与正式提交

**事实**

- 完成 Kaggle 入赛和新版 API Token 配置；Token 未写入仓库。
- 建立绑定实验 ID、Git commit 和源码 SHA-256 的私有 Notebook 构建器。
- 私有 Notebook `heralces/ai-agent-security-b000-official-baseline` version 3 云端运行完成。
- 云端 `attack.py` SHA-256 与本地官方基线完全一致：
  `c4ee5499ff43137c5128caf3e2645fb8f3448ec711c895d5ef1229562028e73d`。
- 补齐 Code Competition 要求的普通 commit 占位 `submission.csv`。
- 创建正式 competition submission `54925726`。

**解释与限制**

- Notebook v3 `COMPLETE` 只证明普通 commit 成功；submission `PENDING` 是独立状态。
- 占位 `submission.csv` 的 `0.0` 不是模型评测或榜单分数。
- 尚无 public score；private score 的可见时间取决于 Kaggle 最终评测流程。

**证据**

- `78ebc6e`：可复现 Kaggle Notebook 构建。
- `7cf2455`：普通 commit 生成 Code Competition 占位输出。
- [`../evidence/2026-07-23_b000_v3.md`](../evidence/2026-07-23_b000_v3.md)

**决策**

- 只监控 submission `54925726`；等待期间不重复提交。

**下一门槛**

- 获得 B000 的真实分数，或取得足以定位问题的失败日志。

## 2026-07-23：建立长期材料记录与 GitHub 同步

**事实**

- 新增竞赛、技术路线和进展总览。
- 新增追加式阶段日志与统一更新规则。
- 将 README、实验账本和 baseline 状态与 Notebook v3 / submission `54925726` 对齐。
- GitHub 采用私有仓库，比赛结束或确认规则允许后再评估公开化。

**解释与限制**

- 当前文档包含私有资源标识和活跃竞赛技术细节，只适合 private 仓库。
- 本阶段是材料治理与发布工作，不对应新的算法实验，实验账本记为 N/A。

**证据**

- [`project_overview.md`](project_overview.md)
- 本文件
- [`../evidence/2026-07-23_b000_v3.md`](../evidence/2026-07-23_b000_v3.md)

**决策**

- 使用私有 GitHub 仓库；公开前另做脱敏副本和规则复核。

**下一门槛**

- 完成首次 GitHub 推送。
- B000 状态变化后同步更新材料、测试并推送。

## 2026-07-23：迁入多项目 Kaggle 工作区

**事实**

- 将当前项目整体迁入 `D:\kaggle\ai-agent-security`。
- `.git`、虚拟环境、本地竞赛数据、Kaggle 产物和全部源码随项目一起迁移。
- `D:\kaggle` 改为 Kaggle 活动总目录，可容纳多个相互独立的平行项目。
- GitHub remote、`master` 历史和 B000 submission 标识保持不变。

**解释与限制**

- 这次变更只调整本地工作区边界，不改变算法、Notebook 或 Kaggle submission。
- 总目录的 `README.md` 是本地项目索引，不属于任一竞赛 Git 仓库。

**证据**

- 项目 Git 顶层：`D:/kaggle/ai-agent-security`
- GitHub remote：`https://github.com/xzzzzc217/kaggle-ai-agent-security.git`
- 最新项目提交和远端 `master` 在迁移后重新核对。

**决策**

- 后续 Kaggle 竞赛均建立为 `D:\kaggle` 下的独立平行子文件夹。
- 文档命令优先使用项目相对路径；必须使用绝对路径时写明当前项目子目录。

**下一门槛**

- 在新路径完成完整测试、SDK 验证和 GitHub 推送。
- 将 B000 监控任务的工作目录更新为新路径。

## 2026-07-23：B000 首次 competition rerun 完成

**事实**

- Submission `54925726` 从 `PENDING` 变为 `COMPLETE`。
- 提交创建时间为 2026-07-23 10:35:13 UTC；首次观测到完成的时间为
  2026-07-23 12:40:51 UTC。
- Public score 为 `0.075`。
- Kaggle CLI 当前没有返回 private score，也没有提供精确完成时间或实际运行时长。

**解释与限制**

- `0.075` 是官方 starter 在隐藏 competition rerun 上得到的真实 public score，可作为
  后续 E001–E003 单变量提交的比较锚点。
- 该结果只验证 B000 攻击算法和提交管线能够完成评分，不证明当前方案达到奖牌水平。
- 从提交创建到首次观测完成约 2 小时 6 分钟，但这包含队列等待，不能当作算法运行时。
- Private score 为空；其可见时间以 Kaggle 最终评测流程为准。

**证据**

- [`../evidence/2026-07-23_b000_v3.md`](../evidence/2026-07-23_b000_v3.md)
- Notebook：`heralces/ai-agent-security-b000-official-baseline` version 3
- Submission ref：`54925726`
- 攻击源码 SHA-256：
  `c4ee5499ff43137c5128caf3e2645fb8f3448ec711c895d5ef1229562028e73d`

**决策**

- 保留 B000 作为真实排行榜基线，不重复提交。
- 暂停 B000 状态心跳；后续提交必须使用新的实验 ID 和单变量假设。

**下一门槛**

- 写明 E001 相对 B000 的唯一变更、预算配置和判定门槛。
- 通过 preflight 与 SDK validate 后，再由用户确认是否创建下一次正式 submission。

## 2026-07-24：预注册 E001 自适应预算实验

**事实**

- 用户确认继续推进下一阶段。
- E001 只把官方 starter 的固定 180/360 秒余量替换为自适应预算控制器。
- 攻击源码 SHA-256 为
  `ec9744b77197f4a1a1838c587d4ecf5aeb680b6e45aaa5a4d422b35f96613ef6`。
- Submission preflight、42 项测试、Ruff 和 SDK 3.1.2 validate 全部通过。

**解释与限制**

- 本地 fixture 只说明预算控制按设计工作，不能预测隐藏模型上的真实分数。
- B000 的 `0.075` 是唯一真实对照；private score 当前不可见。

**证据**

- [`../evidence/2026-07-24_e001_preflight.md`](../evidence/2026-07-24_e001_preflight.md)
- [`../baselines/adaptive_budget_v1/attack.py`](../baselines/adaptive_budget_v1/attack.py)
- Source commit：`d184f45`

**决策**

- 只有 E001 rerun 完成且 public score 严格高于 `0.075` 才支持假设。
- 相等视为未证实；更低或运行失败则拒绝该变更。
- 不根据出分结果修改门槛，不自动重试失败提交。

**下一门槛**

- 构建并验证私有 E001 Notebook。
- 只创建一次 E001 competition submission，并监控至终态。

## 2026-07-24：创建 E001 正式 submission

**事实**

- 私有 Notebook `heralces/ai-agent-security-e001-adaptive-budget` version 1 云端状态为
  `COMPLETE`。
- 云端 `attack.py` SHA-256 与预注册源码一致：
  `ec9744b77197f4a1a1838c587d4ecf5aeb680b6e45aaa5a4d422b35f96613ef6`。
- 普通 commit 输出 `attack.py` 和占位 `submission.csv`；日志没有 exception 或
  traceback。
- 2026-07-24 13:50:27 UTC 创建 competition submission `54952586`，当前为 `PENDING`。
- B000 submission `54925726` 保持 `COMPLETE / 0.075`。

**解释与限制**

- Notebook v1 `COMPLETE` 只验证打包和普通 commit；E001 假设必须等待 competition
  rerun 的真实 public score。
- 占位 CSV 的四个 `0.0` 不是模型评分。
- Kaggle 环境日志中的 debugger、`mistune` 和 `nbconvert` warning 不影响普通 commit。

**证据**

- [`../evidence/2026-07-24_e001_preflight.md`](../evidence/2026-07-24_e001_preflight.md)
- Notebook version：1
- Submission ref：`54952586`
- Notebook build commit：`c221fb6`

**决策**

- 只监控 submission `54952586`，不创建第二条 E001 submission。
- 保持预注册门槛：`>0.075` 支持，`=0.075` 未证实，更低或失败则拒绝。

**下一门槛**

- E001 submission 进入 `COMPLETE` 或 `ERROR/FAILED` 终态。
- 按预注册规则更新实验结论、证据与 GitHub。

## 2026-07-24：E001 完成但未证明评分提升

**事实**

- Submission `54952586` 从 `PENDING` 变为 `COMPLETE`。
- 提交创建时间为 2026-07-24 13:50:27 UTC；首次观测完成时间为
  2026-07-24 15:31:22 UTC。
- E001 public score 为 `0.075`，与 B000 的 `0.075` 完全相同。
- Kaggle CLI 没有返回 private score 或精确算法运行时。

**解释与限制**

- 按出分前预注册规则，`=0.075` 表示“未证明真实评分改善”，不能把本地预算利用提升
  宣称为榜单提升。
- 从提交到首次观测完成约 1 小时 41 分钟，包含队列等待，不是算法运行时。
- 单次相同分数不能证明两个算法内部行为完全相同，只能说明当前 public metric 没有
  观察到增益。

**证据**

- [`../evidence/2026-07-24_e001_preflight.md`](../evidence/2026-07-24_e001_preflight.md)
- Submission ref：`54952586`
- Notebook：`heralces/ai-agent-security-e001-adaptive-budget` version 1
- Public score：`0.075`

**决策**

- 不接受 E001 为已经证实的评分改进。
- 保留 E001 作为 E002 的直接对照，因为 E002 只在 E001 上增加新颖度调度。
- 不重复提交 E001，并暂停其状态监控。

**下一门槛**

- 预注册 E002 相对 E001 的唯一变量、源码哈希和判定门槛。
- 明确 E002 必须严格高于 `0.075` 才支持新颖度调度改善真实评分。

## 2026-07-26：预注册 E002 新颖度调度实验

**事实**

- E002 以 E001 submission `54952586` 的真实 public score `0.075` 为直接对照。
- 唯一实验变量是新颖度调度：成功工具调用签名归一化、跨签名轮转、失败事件过滤和
  每签名保留上限；候选消息和 E001 自适应预算保持不变。
- 攻击源码 SHA-256 为
  `ae936c9cddbbe9ee3770145b75227ed37c3757be4efd3549eae2ff6af6ea3475`。
- Submission preflight、42 项测试、Ruff lint/format 和 SDK 3.1.2 validate 全部通过。
- 此时尚未创建 E002 Notebook 或 competition submission。

**解释与限制**

- 本地 fixture 证明调度、失败过滤和去重机制按设计工作，不包含目标模型、隐藏 fixture
  或 guardrail，不能预测真实榜单分数。
- 普通 Notebook 占位 CSV 的 `0.0` 不是模型评分。
- Kaggle 普通 GPU Notebook 使用每周配额，因此先完成本地预检，云端只运行必要的
  短时 commit；competition rerun 的排队时间不解释为算法运行时或 GPU 消耗。

**证据**

- [`../evidence/2026-07-26_e002_preflight.md`](../evidence/2026-07-26_e002_preflight.md)
- [`../baselines/novelty_scheduler_v1/attack.py`](../baselines/novelty_scheduler_v1/attack.py)
- Source commit：`748d9a4`
- SDK compatibility commit：`a0360da`

**决策**

- E002 rerun `COMPLETE` 且 public score `>0.075` 才支持新颖度调度假设。
- `=0.075` 视为未证实；更低、无分或运行失败则拒绝，不自动重试。
- 正式提交前查询历史，确保 E002 只创建一次。

**下一门槛**

- 提交并推送本预注册，使 Notebook 构建绑定一个出分前固定的 Git commit。
- 构建、云端验证私有 E002 Notebook，并核对云端 `attack.py` 哈希。

## 2026-07-26：创建 E002 正式 submission

**事实**

- 私有 Notebook `heralces/ai-agent-security-e002-novelty-scheduler` version 1 在云端
  进入 `COMPLETE`。
- Notebook 绑定预注册后的 build commit `b947bf1`；云端 `attack.py` SHA-256 与本地
  `ae936c9cddbbe9ee3770145b75227ed37c3757be4efd3549eae2ff6af6ea3475`
  完全一致。
- 普通 commit 产出 `attack.py` 和占位 `submission.csv`；日志无 exception、traceback
  或执行错误。
- 正式提交前再次查询历史，确认不存在 E002；2026-07-26 07:44:30 UTC 只创建
  submission `54995012`，当前为 `PENDING`。

**解释与限制**

- Notebook v1 `COMPLETE` 只验证打包、普通 commit 和源码一致性；E002 假设仍须等待
  competition rerun 的真实 public score。
- 占位 CSV 的四个 `0.0` 不是模型评分。
- Notebook 普通 commit 约 20 秒完成；competition submission 的排队时长不能解释为
  算法运行时，也不能据此推断每周 GPU 配额消耗。

**证据**

- [`../evidence/2026-07-26_e002_preflight.md`](../evidence/2026-07-26_e002_preflight.md)
- Notebook version：1
- Submission ref：`54995012`
- Notebook build commit：`b947bf1`

**决策**

- 只监控 submission `54995012`，不创建第二条 E002 submission。
- 保持预注册门槛：`>0.075` 支持，`=0.075` 未证实，更低或失败则拒绝。

**下一门槛**

- E002 submission 进入 `COMPLETE` 或 `ERROR/FAILED` 终态。
- 按预注册规则更新实验结论、证据和 GitHub。

## 2026-07-26：E002 完成且评分下降

**事实**

- Submission `54995012` 从 `PENDING` 变为 `COMPLETE`。
- 提交创建时间为 2026-07-26 07:44:30 UTC；首次观测完成时间为
  2026-07-26 12:15:22 UTC。
- E002 public score 为 `0.060`，比直接对照 E001 的 `0.075` 低 `0.015`。
- Kaggle CLI 没有返回 private score 或精确算法运行时。

**解释与限制**

- 按出分前预注册规则，`0.060 < 0.075` 表示拒绝当前新颖度调度变更。
- 从提交到首次观测完成约 4 小时 31 分钟，包含队列等待，不是算法运行时，也不能
  据此推断 GPU 配额消耗。
- 本地 harness 中的机制覆盖改善没有转化为真实 public score；这说明本地证据的
  外推边界，但单次总分不能定位轮转顺序、签名上限或隐藏评测交互中的具体原因。

**证据**

- [`../evidence/2026-07-26_e002_preflight.md`](../evidence/2026-07-26_e002_preflight.md)
- Submission ref：`54995012`
- Notebook：`heralces/ai-agent-security-e002-novelty-scheduler` version 1
- Public score：`0.060`

**决策**

- 拒绝 E002，不重复提交，不修改预注册门槛。
- 不把 E002 作为下一实验的默认基础。
- E003 当前叠加在 E002 上，不能直接形成相对有效对照的单变量结论；先做 trace
  诊断，再把冷重放门控隔离到 E001 上重新预注册。

**下一门槛**

- 整理可获得 trace 的 source、transformation、sink 和 predicate 分类。
- 明确下一候选相对 E001 的唯一变量、源码哈希和严格判定门槛后再提交。

## 2026-07-27：实现并预注册 E005 有界 Go-Explore

**事实**

- E002 已被拒绝，因此 E005 不继承其签名轮转、去重或 finding 上限。
- 下一候选改用竞赛 SDK 3.1.2 自带 Go-Explore 搜索；正式编号跳到 E005，保留
  E003/E004 早期原型身份。
- 同一 10 秒 scorer-equivalent 评测中，SDK 原生 Go-Explore 和 5% 余量版本都超过
  generation 截止时间；最多使用 80% 总预算且不超过 900 秒后能够完成。
- E001 与 E005 在公开 fixture 的确定性 agent 上都得到本地 `0.00`。
- E005 攻击源码 SHA-256 为
  `3a0c4f75bcb133c95197133b4ff1e953cb35df17ae57c4b0f36e524607b96eed`。
- Submission preflight、47 项测试、Ruff lint/format 和 SDK 3.1.2 validate 全部通过。

**解释与限制**

- 本地 `0.00` 不是占位 CSV 或 Kaggle 分数；确定性 agent 与目标 GPT-OSS/Gemma 不同，
  因此不能据此宣称 E005 与 E001 相同。
- 超时回归只证明有界包装解决了已复现的 generation 可靠性问题，不证明 Go-Explore
  能提高隐藏评测分数。
- 这次测试不需要 GPU/TPU；普通 Kaggle Notebook 仍只做短时打包。

**证据**

- [`../evidence/2026-07-27_e005_preflight.md`](../evidence/2026-07-27_e005_preflight.md)
- [`../baselines/bounded_goexplore_v1/attack.py`](../baselines/bounded_goexplore_v1/attack.py)
- Source commit：`c97de46`

**决策**

- E005 以 E001 public score `0.075` 为直接对照。
- E005 rerun `COMPLETE` 且 public score `>0.075` 才支持 Go-Explore 假设。
- `=0.075` 视为未证实；更低、无分或失败则拒绝，不自动重试。

**下一门槛**

- 提交并推送本预注册，使 Notebook 构建绑定出分前固定的 Git commit。
- 构建、云端验证私有 E005 Notebook，并核对云端 `attack.py` 哈希。

## 2026-07-27：创建 E005 正式 submission

**事实**

- 私有 Notebook `heralces/ai-agent-security-e005-bounded-goexplore` version 1 在云端
  进入 `COMPLETE`。
- Notebook 绑定预注册 build commit `d5f93d4`；云端 `attack.py` SHA-256 与本地
  `3a0c4f75bcb133c95197133b4ff1e953cb35df17ae57c4b0f36e524607b96eed`
  完全一致。
- 普通 commit 产出 `attack.py` 和占位 `submission.csv`；日志无 exception、traceback
  或执行错误。
- 正式提交前再次查询历史，确认不存在 E005；2026-07-27 01:12:06 UTC 只创建
  submission `55014937`，当前为 `PENDING`。

**解释与限制**

- Notebook v1 `COMPLETE` 只验证打包、普通 commit、SDK import 和源码一致性；E005
  假设仍须等待 competition rerun 的真实 public score。
- 占位 CSV 的四个 `0.0` 不是模型评分。
- 普通 Notebook 使用 T4 但只执行短时打包；真正 Go-Explore 搜索由 competition
  rerun 执行，队列等待不解释为算法运行时或 GPU 配额消耗。

**证据**

- [`../evidence/2026-07-27_e005_preflight.md`](../evidence/2026-07-27_e005_preflight.md)
- Notebook version：1
- Submission ref：`55014937`
- Notebook build commit：`d5f93d4`

**决策**

- 只监控 submission `55014937`，不创建第二条 E005 submission。
- 保持预注册门槛：`>0.075` 支持，`=0.075` 未证实，更低或失败则拒绝。

**下一门槛**

- E005 submission 进入 `COMPLETE` 或 `ERROR/FAILED` 终态。
- 按预注册规则更新实验结论、证据和 GitHub。

## 2026-07-27：E005 完成但真实分数为零

**事实**

- Submission `55014937` 从 `PENDING` 变为 `COMPLETE`。
- 提交创建时间为 2026-07-27 01:12:06 UTC；首次观测完成时间为
  2026-07-27 02:14:25 UTC。
- E005 public score 为 `0.000`，比直接对照 E001 的 `0.075` 低 `0.075`。
- Kaggle CLI 没有返回 private score、候选数量、重放日志或精确算法运行时。

**解释与限制**

- 按出分前预注册规则，`0.000 < 0.075` 表示拒绝当前有界 Go-Explore 候选。
- 从提交到首次观测完成约 1 小时 2 分钟，包含队列等待，不是算法运行时，也不能据此
  推断 GPU 配额消耗。
- 本地确定性 agent `0.00` 与真实榜单 `0.000` 来源不同；数值相同不意味着本地 agent
  可以预测隐藏评测。
- CLI 只证明最终没有可计分贡献，不能区分无候选、重放无 predicate、无可计分 cell
  或目标模型/guardrail/资源边界导致的失效。

**证据**

- [`../evidence/2026-07-27_e005_preflight.md`](../evidence/2026-07-27_e005_preflight.md)
- Submission ref：`55014937`
- Notebook：`heralces/ai-agent-security-e005-bounded-goexplore` version 1
- Public score：`0.000`

**决策**

- 拒绝 E005，不重复提交，不修改预注册门槛。
- 没有生成/重放诊断证据前，不继续 Go-Explore 参数消融。
- 回到 E001 手写候选路线，下一实验只隔离新增攻击模板覆盖。

**下一门槛**

- 从公开 predicate 和 fixture 中选择一个 E001 未覆盖、能形成独立 score cell 的模板族。
- 固定候选消息、源码哈希和严格高于 `0.075` 的判定门槛后再提交。

## 2026-07-27：建立并预注册 B001 公开 two-probe 参考基线

**事实**

- 当前公开榜首可见分数已超过 `110`，而本项目最佳仍为 B000/E001 的 `0.075`；继续在
  九条 starter 候选上做小幅调度调整的信息增益过低。
- 下载并审查公开 Notebook
  `tetsutani/ai-agent-sec-adaptive-uniform-two-probe-recovery`；其说明记录 three-probe
  前身曾获得 Hosted `88.515` 和 `89.055`。
- 建立 B001 可追溯副本，保留 two-probe、full-hop 成功验证和 replay-cost ledger，
  只把任意 `.co` 目标改为唯一的 `*.example.com` 保留域。
- 上游 Notebook SHA-256 为
  `54b7d943dc717ea9c357d954dd3ac3f1f4d6bf3eae9d43b65092f25913666bb1`。
- B001 源码 SHA-256 为
  `daf204fb5f824a90f812d23e006d390d8bb8219ef86ce7b6a7f6ecc9e8ed8431`，
  source commit 为 `0fe6d3c`。
- 54 项测试、preflight、Ruff 和 SDK 3.1.2 validate 通过。
- 120 秒确定性 agent 评测约 63 秒完成，本地 `0.00`、0 finding、0 unique cell。
- 截至 2026-07-27 13:33 UTC 尚未创建 B001 Notebook 或 competition submission。

**解释与限制**

- B001 是公开参考复现，不是原创算法实验；第三方分数不能写成我们的榜单成绩。
- 本地确定性 agent 会把请求载荷替换为 `demo`，其 `0.00` 只验证算法按预算返回，不能
  预测 GPT-OSS/Gemma。
- `*.example.com` 适配保持 score cell 的唯一 host 维度，但更长的 token 序列可能影响
  模型延迟或工具遵循率，必须由真实 rerun 验证。
- 普通 Notebook 占位 CSV 的 `0.0` 仍不是评测结果。

**证据**

- [`../evidence/2026-07-27_b001_preflight.md`](../evidence/2026-07-27_b001_preflight.md)
- [`../baselines/public_two_probe_v1/attack.py`](../baselines/public_two_probe_v1/attack.py)
- [`../baselines/public_two_probe_v1/README.md`](../baselines/public_two_probe_v1/README.md)

**决策**

- 允许 B001 进入一次正式复现。
- Public Score `>0.075` 才保留为后续基线；`>=60.000` 额外记为强复现。
- `<=0.075`、空分或失败则拒绝当前适配；不自动重试，不修改门槛。

**下一门槛**

- 提交并推送本预注册，使 B001 Notebook 绑定出分前固定 commit。
- 构建并云端验证唯一 B001 私有 Notebook，核对云端源码哈希。
- 正式提交前查询历史，确保 B001 submission 只创建一次。

## 2026-07-27：创建 B001 正式 submission

**事实**

- 私有 Notebook `heralces/ai-agent-security-b001-public-two-probe` version 1 进入
  `COMPLETE`。
- Notebook 绑定预注册 commit `3332d8c`；云端 `attack.py` SHA-256 与本地
  `daf204fb5f824a90f812d23e006d390d8bb8219ef86ce7b6a7f6ecc9e8ed8431`
  完全一致。
- 普通 commit 日志无 exception、traceback 或执行错误；生成 `attack.py` 和占位
  `submission.csv`。
- Notebook 使用 CPU；短时打包不需要消耗 Kaggle GPU/TPU 周配额。
- 正式提交前再次查询历史，确认不存在 B001；2026-07-27 13:39:35 UTC 只创建
  submission `55030205`，当前为 `PENDING`。

**解释与限制**

- Notebook v1 `COMPLETE` 只验证私有打包、SDK import 和源码一致性，不验证目标模型分数。
- 占位 CSV 的四个 `0.0` 不是 B001 Public/Private Score。
- competition rerun 的排队时间、GPU/TPU 使用和算法精确运行时在当前 CLI 中不可见，
  不从等待时长臆测。

**证据**

- [`../evidence/2026-07-27_b001_preflight.md`](../evidence/2026-07-27_b001_preflight.md)
- Notebook version：1
- Submission ref：`55030205`
- Notebook build commit：`3332d8c`

**决策**

- 只监控 submission `55030205`，不创建第二条 B001 submission。
- 保持预注册门槛：`>0.075` 保留，`>=60.000` 强复现，`<=0.075` 或失败则拒绝。

**下一门槛**

- B001 submission 进入 `COMPLETE` 或 `ERROR/FAILED` 终态。
- 按预注册规则更新实验结论、证据、项目索引和 GitHub。

## 2026-07-28：B001 完成并达到强复现门槛

**事实**

- Submission `55030205` 已进入 `COMPLETE`。
- B001 Public Score 为 `65.340`；Private Score 当前未返回。
- 相对 B000/E001 的 `0.075`，绝对提升 `65.265`。
- 结果同时满足预注册的 `>0.075` 保留门槛和 `>=60.000` 强复现门槛。

**解释与限制**

- B001 证明公开 replay-dense two-probe 路线已在本账号复现，并应取代旧 starter 路线
  成为真实对照。
- 该分数在 2026-07-30 复核时仍低于榜单快照第 200 名的 `89.390`，尚未进入当前前 200。
- B001 是公开参考复现，不构成原创算法贡献。

**决策**

- 保留 B001 作为新的真实参考基线。
- 下一参考候选优先提高单位 replay 时间内的有效候选吞吐，不回到旧的九模板搜索。

## 2026-07-30：实现并预注册 B002 公开 fill-stack 参考候选

**事实**

- 下载并固定公开 Notebook
  `pilkwang/ai-agent-v3-1-2-single-post-exfiltration` 的来源快照。
- B002 采用一次冷启动、八模板五次 1-hop 探测、raw/秒选择、仅选中模板回放和
  `1.43` replay 成本校准。
- 安全适配使用唯一 `*.invalid` 保留域，SDK 工具不发生真实网络请求。
- B002 源码 commit 为 `79df05c`，SHA-256 为
  `feb2fa2c85146afddf59186d5c12dfd05749c992b5c762ab7d99cabd21a2616f`。
- 61 项测试、preflight、Ruff 与 SDK 3.1.2 validate 全部通过。

**解释与限制**

- 本地确定性 agent 不能估计目标模型的 fire rate 或 1-hop/full-hop 延迟比。
- `1.43` 是公开经验校准；低估 replay 成本会造成整条 submission 超时，是主要风险。
- 这是公共参考栈的整体复现，不作为项目原创实验。

**决策**

- 允许 B002 在预注册提交并完成云端哈希核对后创建唯一 competition rerun。
- Public Score `>65.340` 才替换 B001；`>=89.390` 记为达到当前前 200 分数带；
  `>=100.000` 记为强竞争复现。
- `<=65.340`、空分或超时则拒绝，不自动重试。

## 2026-07-30：创建 B002 正式 submission

**事实**

- 私有 Notebook `heralces/ai-agent-security-b002-public-fillstack` version 1 进入
  `COMPLETE`。
- Notebook 绑定预注册 commit `1d7613f`；scriptVersionId 为 `339078295`。
- 云端 `attack.py` SHA-256 与本地
  `feb2fa2c85146afddf59186d5c12dfd05749c992b5c762ab7d99cabd21a2616f`
  完全一致。
- 普通 commit 日志无 exception、traceback 或执行错误；生成 `attack.py` 和占位
  `submission.csv`。
- 仅上传本地 CSV 的首次尝试返回 Kaggle API `400`，未创建 submission；正确的
  Code Competition 提交绑定 Notebook v1。
- 正式提交前再次查询历史，确认不存在 B002；2026-07-30 13:57:21 UTC 只创建
  submission `55110969`，当前为 `PENDING`。

**解释与限制**

- Notebook v1 `COMPLETE` 只验证私有打包、SDK import 和源码一致性，不验证目标模型分数。
- 占位 CSV 的四个 `0.0` 不是 B002 Public/Private Score。
- competition rerun 的排队时间、GPU/TPU 使用和算法精确运行时在当前 CLI 中不可见，
  不从等待时长臆测。

**证据**

- [`../evidence/2026-07-30_b002_preflight.md`](../evidence/2026-07-30_b002_preflight.md)
- Notebook version：1
- Submission ref：`55110969`
- Notebook build commit：`1d7613f`

**决策**

- 只监控 submission `55110969`，不创建第二条 B002 submission。
- 保持预注册门槛：`>65.340` 保留，`>=89.390` 达到 2026-07-30 前 200 分数带，
  `>=100.000` 强竞争复现，`<=65.340` 或失败则拒绝。

## 2026-07-30：准备 B003 公开 replay-safe split 后备候选

**事实**

- 拉取公开 Notebook `nctuan/jed-v25`，上游 SHA-256 为
  `2005325799dfed256e063428212d1259fdadaa6c3816ffac3ca5e400bbd8b5db`。
- B003 采用一次冷启动、live validation-fill、前 8 个候选延迟分类、慢行 frame template
  和 `0.98` replay-safe sizing。
- 安全适配使用唯一 `*.invalid` 保留域；SDK 工具不发生真实网络请求。
- B003 源码 SHA-256 为
  `f9e19bec312a3fd4410506af1418463bd30254c5d4c024c3343007566e46d0b6`。
- 68 项测试、preflight、Ruff 与 SDK 3.1.2 validate 全部通过。

**解释与限制**

- B003 与 B002 的机制差异较大，不能在 B002 出分前定义清晰的直接对照门槛。
- 默认 `PROBE_HOPS=0`，即使用 grader 配置的 hop cap；这比 B002 的 1-hop 探测更保守，
  也可能牺牲候选吞吐。
- 这是公共参考栈的整体复现，不作为项目原创实验。

**决策**

- 暂不创建 B003 Notebook 或 competition submission。
- 等 B002 `55110969` 进入终态后，再按真实分数重新预注册 B003 或转向原创单变量改进。

## 2026-07-31：B002 以 `COMPLETE` 空分结束

**事实**

- 2026-07-31 01:30 UTC 首次观测到 submission `55110969` 为 `COMPLETE`。
- Kaggle CLI 的表格与 CSV 输出均未返回 Public Score 或 Private Score。
- B001 submission `55030205` 仍为当前唯一高分可比较对照，Public Score `65.340`。

**解释与限制**

- `COMPLETE` 只说明 rerun 流程进入终态；空分不能解释为 `0.000`，也不能与 B001 比较。
- 普通 Notebook 的占位 `submission.csv` 不代表 competition rerun 分数。
- 当前 CLI 未返回可比较运行时或额外错误说明，不臆测空分的内部原因。

**证据**

- [`../evidence/2026-07-30_b002_preflight.md`](../evidence/2026-07-30_b002_preflight.md)
- Submission ref：`55110969`

**决策**

- 按出分前规则把空分视为可靠性失败，拒绝 B002，不替换 B001。
- 不重试 B002，不创建重复 submission。

**下一门槛**

- 以 B001 `65.340` 为直接对照预注册 B003，完成提交前证据链后只创建一次 rerun。

## 2026-07-31：预注册 B003 replay-safe split 参考候选

**事实**

- B003 源码保持 commit `86057bc` 与 SHA-256
  `f9e19bec312a3fd4410506af1418463bd30254c5d4c024c3343007566e46d0b6`。
- 直接对照固定为 B001 submission `55030205` 的 Public Score `65.340`。
- 主要机制固定为 live validation-fill、前 8 候选延迟分类、慢行 Harmony frame
  template、`0.98` replay-safe sizing、grader hop cap 和单 post。
- 68 项测试、preflight、Ruff 与 SDK 3.1.2 validate 的本地证据保持有效。

**解释与限制**

- B002 空分不能提供数值对照；B003 与 B001 是不同的公共参考栈整体比较，不作为原创消融。
- 本地确定性 agent 只能验证接口、预算和安全边界，不能预测目标模型 fire rate。

**决策**

- `>65.340` 才保留 B003；`>=89.390` 记为达到固定的 2026-07-30 前 200 分数带；
  `>=100.000` 记为强竞争复现。
- `<=65.340`、空分、失败或超时均拒绝，且不自动重试。
- 预注册文档提交并推送后，允许构建私有 Notebook；云端哈希与历史去重通过后，
  只创建一次 competition submission。

## 2026-07-31：创建 B003 正式 submission

**事实**

- B002 终态与 B003 预注册文档已提交并推送，commit 为 `0747344`。
- 私有 Notebook `heralces/ai-agent-security-b003-replaysafe-split` version 1
  进入 `COMPLETE`。
- 构建 manifest 绑定完整 commit
  `0747344125732bc2a5d7eb337fa1e36c78159b69`。
- 云端 `attack.py` SHA-256 与本地
  `f9e19bec312a3fd4410506af1418463bd30254c5d4c024c3343007566e46d0b6`
  完全一致；日志无 error/exception 匹配，产物凭据扫描为 0。
- 正式提交前再次查询历史，确认不存在 B003；2026-07-31 01:34:44 UTC 只创建
  submission `55123773`，当前为 `PENDING`。

**解释与限制**

- Notebook v1 `COMPLETE` 只验证私有打包、SDK import 和源码一致性，不验证目标模型分数。
- 四行 `0.0` 是 Code Competition 普通 commit 占位值，不是 Public/Private Score。
- rerun 排队与算法精确运行时在当前 CLI 中不可见。

**证据**

- [`../evidence/2026-07-30_b003_local_candidate.md`](../evidence/2026-07-30_b003_local_candidate.md)
- Notebook version：1
- Submission ref：`55123773`
- Pre-registration commit：`0747344`

**决策**

- 只监控 submission `55123773`，不创建第二条 B003 submission。
- 保持预注册门槛：`>65.340` 保留，`>=89.390` 达到固定前 200 分数带，
  `>=100.000` 强竞争复现；`<=65.340`、空分或失败则拒绝。

## 2026-07-31：B003 完成并替换 B001 为真实参考基线

**事实**

- 2026-07-31 15:42:51 UTC 首次在本任务中观测到 submission `55123773` 进入
  `COMPLETE`。
- Kaggle CLI CSV 输出显示 B003 Public Score 为 `81.585`，Private Score 为空。
- Kaggle Python API 对同一 ref 返回 `status=SubmissionStatus.COMPLETE`、
  `publicScore=None`、`privateScore=None`、`errorDescription=None`；因此实际可比较
  Public Score 以 CLI submissions 表格为准。
- 同一轮公开榜下载快照显示 `81.585` 对应 rank `830`；2026-07-31 15:45 UTC 的
  第 200 名为 `89.595`。这是当前榜单快照，不改变预注册时固定的 `89.390` 参考线。

**解释与限制**

- `81.585 > 65.340`，B003 明确超过 B001，支持 replay-safe split 参考栈优于此前
  two-probe 参考栈的预注册假设。
- `81.585 < 89.390`，未达到固定的 2026-07-30 前 200 分数带；也低于 `100.000`
  强竞争复现线。
- B003 仍是有出处的公开参考复现，不作为原创算法贡献；Private Score 当前不可见。

**证据**

- [`../evidence/2026-07-30_b003_local_candidate.md`](../evidence/2026-07-30_b003_local_candidate.md)
- Submission ref：`55123773`
- Public Score：`81.585`
- Private Score：空
- First observed terminal：`2026-07-31 15:42:51 UTC`

**决策**

- 保留 B003，替换 B001 作为新的真实参考基线。
- 不重试 B003，不重复创建相同 candidate 的 competition submission。
- 下一候选必须以 B003 `81.585` 为直接对照；优先设计结构上不同、可证伪的原创单变量
  改进，并在任何 Notebook/competition submission 前先完成预注册、提交和推送。

**下一门槛**

- 新候选 Public Score 必须严格高于 `81.585` 才能替换 B003。
- `>=89.390` 仍记录为达到固定前 200 分数带，`>=100.000` 记录为强竞争复现。

## 2026-08-01：实现并预注册 B004 slow-row multi-post 候选

**事实**

- B004 以 B003 submission `55123773` 的真实 Public Score `81.585` 为直接对照。
- B004 源码位于 `baselines/replaysafe_multipost_v1/attack.py`，source commit 为
  `af266f4`，SHA-256 为
  `7e101927bc3f96f59d91d0b04aa5e17fb18de89e0667890c95b75dac26ba7db5`。
- 唯一行为变量是将 B003 的 `SLOW_MULTIPOST_N` 默认值从 `1` 改为 `4`；其余 B003
  默认值保持不变。
- B003/B004 目标测试 7 项通过；全量测试 72 项通过；preflight、Ruff、SDK validate、
  `git diff --check` 和秘密扫描均通过。
- SDK scoring audit 显示单个成功 `http.post` finding 的 raw score 为 `18.0`，同一
  finding 内四个成功 `http.post` 的 raw score 为 `66.0`。
- 截至本记录，尚未创建 B004 Kaggle Notebook 或 competition submission。

**解释与限制**

- 本地证据只证明接口、安全 URL、动态样本形状和 SDK 打分上界；不能预测隐藏模型是否
  会稳定执行四个连续 post。
- B004 的风险是更长的 prompt 与更多工具调用可能降低遵循率或增加 replay 时间；本次
  不同时调整 replay 成本系数，以保持单变量纪律。
- B004 是 B003 后的原创单变量改动，不是新的公开参考整体复现。

**证据**

- [`../evidence/2026-08-01_b004_preflight.md`](../evidence/2026-08-01_b004_preflight.md)
- [`../baselines/replaysafe_multipost_v1/attack.py`](../baselines/replaysafe_multipost_v1/attack.py)
- [`../tests/test_replaysafe_multipost.py`](../tests/test_replaysafe_multipost.py)

**决策**

- 预注册 B004，允许在本预注册文档提交并推送后进入一次私有 Notebook 构建与云端哈希
  核验。
- B004 rerun `COMPLETE` 且 Public Score `>81.585` 才替换 B003。
- Public Score `>=89.390` 记为达到固定前 200 分数带，`>=100.000` 记为强竞争复现。
- `<=81.585`、空分、失败或超时均拒绝，且不自动重试。

**下一门槛**

- 提交并推送本预注册文档。
- 构建唯一 B004 私有 Notebook，核验 manifest、云端 `attack.py` 哈希、安全 URL、
  运行日志和产物秘密扫描。
- 正式提交前再次查询 Kaggle 历史，确认不存在相同 B004 候选。

## 2026-08-01：创建 B004 唯一 Kaggle submission，等待真实评分

**事实**

- B004 预注册文档先于正式提交在 commit `22ca5a9` 提交并推送。
- 使用 `scripts.build_kaggle_notebook` 构建私有 Notebook
  `heralces/ai-agent-security-b004-slow-multipost` version 1，manifest 绑定的
  Git commit 为 `22ca5a96a657addb37432b8aa14f1ffc3c8b27c6`。
- Kaggle Notebook v1 运行状态为 `COMPLETE`；下载的云端 `attack.py` SHA-256 与本地
  候选哈希一致：
  `7e101927bc3f96f59d91d0b04aa5e17fb18de89e0667890c95b75dac26ba7db5`。
- 云端运行日志错误扫描为 `0`，下载产物秘密扫描为 `0`。
- 正式提交前重新查询 Kaggle 历史，未发现 B004 相同候选；随后创建唯一 competition
  submission `55168834`。
- submission `55168834` 的创建时间为 2026-08-01 18:22:47.167 UTC；截至
  2026-08-02 05:52 UTC 最新 CLI 观测仍为 `SubmissionStatus.PENDING`，Public/Private
  Score 均为空。

**解释与限制**

- Notebook `COMPLETE`、云端哈希一致和日志/秘密扫描通过只证明正式提交前的产物可追溯；
  不代表 Kaggle 已完成隐藏 rerun。
- `submission.csv` 内的 `0.0` 占位值不是 leaderboard score。
- B004 出分前不能判断 slow-row multi-post 是否优于 B003，也不能把它当作新基线。

**证据**

- [`../evidence/2026-08-01_b004_preflight.md`](../evidence/2026-08-01_b004_preflight.md)
- [`../submissions/B004/submission-manifest.json`](../submissions/B004/submission-manifest.json)
- [`../artifacts/kaggle/B004_v1/attack.py`](../artifacts/kaggle/B004_v1/attack.py)

**决策**

- 只监控 B004 submission `55168834`；不重复提交、不重推相同 Notebook。
- B003 submission `55123773` 的 Public Score `81.585` 仍是当前真实最佳。
- B004 未知期间不创建 B005；等待期间只做本地候选研究、公开参考审计和轨迹分析。

**下一门槛**

- 若 `55168834` 变为 `COMPLETE`，记录真实 Public Score、Private Score 的可见状态和首次
  观测终态时间。
- 按预注册：`>81.585` 才替换 B003；`>=89.390` 记为达到固定前 200 分数带；`>=100.000`
  记为强竞争复现；空分、失败、超时或 `<=81.585` 则拒绝且不重试。

## 2026-08-02：B004 rerun 完成并刷新真实最佳分数

**事实**

- submission `55168834` 从 `PENDING` 变为 `SubmissionStatus.COMPLETE`。
- 2026-08-02 07:53 UTC 首次观测到 B004 终态。
- Public Score 为 `88.650`；Kaggle CLI 仍未返回 Private Score。
- 相对 B003 `81.585` 提升 `+7.065`；相对历史 B001 `65.340` 提升 `+23.310`。
- B004 仍低于固定的 2026-07-30 top-200 参考线 `89.390`，差 `0.740`；也低于强竞争参考
  `100.000`。

**解释与限制**

- 该结果支持 B003 slow-row 分支的 multi-post 单变量放大假设，足以按预注册替换当前最佳。
- 分数未达到固定前 200 分数带，也不能证明已经接近奖牌区。
- Private Score 为空；最终私榜表现仍不可见。

**证据**

- [`../evidence/2026-08-01_b004_preflight.md`](../evidence/2026-08-01_b004_preflight.md)
- Kaggle submissions CLI：`55168834` `COMPLETE`，Public Score `88.650`

**决策**

- 保留 B004 为新的真实参考基线；不重试 B004。
- B003 `81.585` 降为历史基线。
- 下一正式候选必须以 B004 `88.650` 为直接对照。

**下一门槛**

- 设计并预注册 B005：结构上不同、可证伪、单变量；优先选择与 slow-row multi-post 低相关的
  原创机制或尚未复现的公开高分路线。
- B005 的接受门槛必须严格高于 `88.650`；`>=89.390` 记为达到固定前 200 分数带，
  `>=100.000` 记为强竞争复现；空分、失败、超时或 `<=88.650` 拒绝且不重试。

## 2026-08-02：实现并预注册 B005 replay-safe tail-extension 候选

**事实**

- B005 以 B004 submission `55168834` 的真实 Public Score `88.650` 为直接对照。
- B005 源码位于 `baselines/replaysafe_tail99_v1/attack.py`，source commit 为
  `a4a70ac`，SHA-256 为
  `9d86d633b50a72f7499f7ad6c4f81c03fb61887e12351da977f7cb64e413c67f`。
- 唯一行为变量是将 B004 的 `REPLAY_SAFE_FRAC` 默认值从 `0.98` 改为 `0.99`；B004 的
  prompt、`SLOW_MULTIPOST_N=4`、latency split、probe hops、保留域和 replay-cost 系数保持
  不变。
- 与 B004 源码 diff 只包含 docstring 标识和 `REPLAY_SAFE_FRAC` 常量变化。
- B004/B005/B003 目标测试 9 项通过；全量测试 76 项通过；preflight、Ruff、SDK validate、
  `git diff --check` 和秘密扫描均通过。
- 9000 秒假环境样本显示 B005 相对 B004 返回约 1.0% 更多候选：13s 慢行样本为 `675→682`，
  20s 慢行为 `439→443`，30s 慢行为 `292→295`。
- 截至本记录，尚未创建 B005 Kaggle Notebook 或 competition submission。

**解释与限制**

- B005 不改变攻击 wording，也不继续调整 multi-post 数；它只测试 B004 成功后是否仍有安全
  replay tail 可用于补足 `88.650` 到固定前 200 参考线 `89.390` 的 `0.740` 缺口。
- 本地假环境只能验证候选数量、预算边界和动态样本形状；不能预测隐藏 replay 是否在 `0.99`
  下仍稳定完成。
- `0.99` 比 B004 更接近 replay budget 边界，主要风险是隐藏重放耗时增加导致失败、空分或
  score 下降。

**证据**

- [`../evidence/2026-08-02_b005_preflight.md`](../evidence/2026-08-02_b005_preflight.md)
- [`../baselines/replaysafe_tail99_v1/attack.py`](../baselines/replaysafe_tail99_v1/attack.py)
- [`../tests/test_replaysafe_tail99.py`](../tests/test_replaysafe_tail99.py)

**决策**

- 预注册 B005，允许在本预注册文档提交并推送后进入一次私有 Notebook 构建与云端哈希核验。
- B005 rerun `COMPLETE` 且 Public Score `>88.650` 才替换 B004。
- Public Score `>=89.390` 记为达到固定前 200 分数带，`>=100.000` 记为强竞争复现。
- `<=88.650`、空分、失败或超时均拒绝，且不自动重试。

**下一门槛**

- 提交并推送本预注册文档。
- 构建唯一 B005 私有 Notebook，核验 manifest、云端 `attack.py` 哈希、安全 URL、运行日志和
  产物秘密扫描。
- 正式提交前再次查询 Kaggle 历史，确认不存在相同 B005 候选。

## 2026-08-02：创建 B005 唯一 Kaggle submission，等待真实评分

**事实**

- B005 预注册文档先于正式提交在 commit `3e5f741` 提交并推送。
- 使用 `scripts.build_kaggle_notebook` 构建私有 Notebook
  `heralces/ai-agent-security-b005-tail99` version 1，manifest 绑定的 Git commit 为
  `3e5f741f8829990f5a7f9a387f81e7266b9a3d59`。
- Kaggle Notebook v1 运行状态为 `COMPLETE`；下载的云端 `attack.py` SHA-256 与本地候选哈希
  一致：
  `9d86d633b50a72f7499f7ad6c4f81c03fb61887e12351da977f7cb64e413c67f`。
- 云端运行日志错误扫描为 `0`，下载产物秘密扫描为 `0`。
- 正式提交前重新查询 Kaggle 历史，未发现 B005 相同候选；随后创建唯一 competition
  submission `55185029`。
- submission `55185029` 的创建时间为 2026-08-02 11:54:44.773 UTC；截至本记录最新 CLI 观测为
  `SubmissionStatus.PENDING`，Public/Private Score 均为空。

**解释与限制**

- Notebook `COMPLETE`、云端哈希一致和日志/秘密扫描通过只证明正式提交前的产物可追溯；
  不代表 Kaggle 已完成隐藏 rerun。
- `submission.csv` 内的 `0.0` 占位值不是 leaderboard score。
- B005 出分前不能判断 replay-safe tail extension 是否优于 B004，也不能把它当作新基线。

**证据**

- [`../evidence/2026-08-02_b005_preflight.md`](../evidence/2026-08-02_b005_preflight.md)
- [`../submissions/B005/submission-manifest.json`](../submissions/B005/submission-manifest.json)
- [`../artifacts/kaggle/B005_v1/attack.py`](../artifacts/kaggle/B005_v1/attack.py)

**决策**

- 只监控 B005 submission `55185029`；不重复提交、不重推相同 Notebook。
- B004 submission `55168834` 的 Public Score `88.650` 仍是当前真实最佳。
- B005 未知期间不创建 B006；等待期间只做本地候选研究、公开参考审计和轨迹分析。

**下一门槛**

- 若 `55185029` 变为 `COMPLETE`，记录真实 Public Score、Private Score 的可见状态和首次观测
  终态时间。
- 按预注册：`>88.650` 才替换 B004；`>=89.390` 记为达到固定前 200 分数带；`>=100.000`
  记为强竞争复现；空分、失败、超时或 `<=88.650` 则拒绝且不重试。

## 2026-08-03：B005 rerun 完成并越过固定前 200 参考线

**事实**

- submission `55185029` 从 `SubmissionStatus.PENDING` 变为 `SubmissionStatus.COMPLETE`。
- 2026-08-03 03:24 UTC 首次观测到 B005 终态。
- Kaggle CLI 显示 Public Score `91.930`；Private Score 仍为空。
- 相对直接对照 B004 `88.650` 提升 `+3.280`。
- 相对固定的 2026-07-30 top-200 参考线 `89.390` 高 `+2.540`；相对强竞争参考线
  `100.000` 仍低 `8.070`。

**解释与限制**

- 结果支持 B004 之后的 replay-safe tail-extension 单变量假设，说明 `REPLAY_SAFE_FRAC`
  从 `0.98` 延长到 `0.99` 在本账号隐藏 rerun 中没有破坏可靠性，并带来可比较的真实分数提升。
- `91.930 >= 89.390` 只表示达到出分前固定的 2026-07-30 前 200 分数带；实时榜线、奖牌区和私榜表现
  可能随队伍与提交变化而漂移。
- Private Score 当前不可见，最终候选选择仍需保留机制低相关版本。

**证据**

- [`../evidence/2026-08-02_b005_preflight.md`](../evidence/2026-08-02_b005_preflight.md)
- Kaggle submissions CLI：`55185029` `SubmissionStatus.COMPLETE`，Public Score `91.930`。

**决策**

- 按预注册保留 B005 为新的真实参考基线，不重试 B005。
- B004 `88.650` 降为历史基线。
- 下一正式候选必须以 B005 `91.930` 为直接对照，并在任何 Kaggle Notebook 或 competition
  submission 前先完成预注册、提交和推送。

**下一门槛**

- 设计并预注册 B006：结构上不同、可证伪、单变量，优先选择与 replay-safe tail-extension 和
  slow-row multi-post 低相关的机制。
- B006 的接受门槛必须严格高于 `91.930`；`>=100.000` 记为强竞争复现；空分、失败、超时或
  `<=91.930` 拒绝且不重试。

## 2026-08-03：实现并预注册 B006 replay-safe threshold8 候选

**事实**

- B006 以 B005 submission `55185029` 的真实 Public Score `91.930` 为直接对照。
- B006 源码位于 `baselines/replaysafe_threshold8_v1/attack.py`，source commit 为
  `59df333`，SHA-256 为
  `7c9c7e41c019d030c034192926c9c916c7651fed913b83a3ed499801b9144128`。
- 唯一行为变量是将 B005 的 `SPLIT_THRESHOLD_S` 默认值从 `12.0` 改为 `8.0`；B005 的
  prompt、`REPLAY_SAFE_FRAC=0.99`、`SLOW_MULTIPOST_N=4`、probe hops、保留域和
  replay-cost 系数保持不变。
- 与 B005 源码 diff 只包含 docstring 标识和 `SPLIT_THRESHOLD_S` 常量变化。
- B006 目标测试 2 项通过；全量测试 80 项通过；preflight、Ruff、SDK validate、
  `git diff --check` 和秘密扫描均通过。
- 9000 秒假环境样本显示 B006 相对 B005 不改变候选数，但把 9-12 秒中速样本从 plain
  单 post 路由到 frame / four-endpoint 分支。
- 截至本记录，尚未创建 B006 Kaggle Notebook 或 competition submission。

**解释与限制**

- B006 测试的是 latency routing 边界，而不是继续调 `REPLAY_SAFE_FRAC` 或
  `SLOW_MULTIPOST_N`。
- 本地假环境只能验证路由形状、候选数量、保留域 URL 和接口契约；不能预测隐藏模型在中速行
  是否更愿意执行 frame / four-endpoint 指令。
- 因样本候选数不变，B006 的上涨空间来自机制质量替换；若中速行原本更适合 plain 模板或
  frame 模板更触发隐藏 guardrail，B006 可能低于 B005。

**证据**

- [`../evidence/2026-08-03_b006_preflight.md`](../evidence/2026-08-03_b006_preflight.md)
- [`../baselines/replaysafe_threshold8_v1/attack.py`](../baselines/replaysafe_threshold8_v1/attack.py)
- [`../tests/test_replaysafe_threshold8.py`](../tests/test_replaysafe_threshold8.py)

**决策**

- 预注册 B006，允许在本预注册文档提交并推送后进入一次私有 Notebook 构建与云端哈希核验。
- B006 rerun `COMPLETE` 且 Public Score `>91.930` 才替换 B005。
- Public Score `>=100.000` 记为强竞争复现。
- `<=91.930`、空分、失败或超时均拒绝，且不自动重试。

**下一门槛**

- 提交并推送本预注册文档。
- 构建唯一 B006 私有 Notebook，核验 manifest、云端 `attack.py` 哈希、安全 URL、运行日志和
  产物秘密扫描。
- 正式提交前再次查询 Kaggle 历史，确认不存在相同 B006 候选。

## 2026-08-03：创建 B006 唯一 Kaggle submission，等待真实评分

**事实**

- B006 预注册文档先于正式提交在 commit `b896105` 提交并推送。
- 使用 `scripts.build_kaggle_notebook` 构建私有 Notebook
  `heralces/ai-agent-security-b006-threshold8` version 1，manifest 绑定的 Git commit 为
  `b89610512eb08a3afbd14412e26b47a46b04508f`。
- Kaggle Notebook v1 运行状态为 `COMPLETE`；下载的云端 `attack.py` SHA-256 与本地候选哈希
  一致：
  `7c9c7e41c019d030c034192926c9c916c7651fed913b83a3ed499801b9144128`。
- 云端运行日志错误扫描为 `0`，下载产物秘密扫描为 `0`。
- 正式提交前重新查询 Kaggle 历史，未发现 B006 相同候选；随后创建唯一 competition
  submission `55203390`。
- submission `55203390` 的创建时间为 2026-08-03 05:36:55.310 UTC；截至本记录最新 CLI 观测为
  `SubmissionStatus.PENDING`，Public/Private Score 均为空。
- 一次错误的本地 CSV 上传形式曾返回 HTTP 400；查询 submissions 确认它没有创建 B006
  competition submission。唯一实际 B006 submission 是 `55203390`。

**解释与限制**

- Notebook `COMPLETE`、云端哈希一致和日志/秘密扫描通过只证明正式提交前的产物可追溯；
  不代表 Kaggle 已完成隐藏 rerun。
- `submission.csv` 内的 `0.0` 占位值不是 leaderboard score。
- B006 出分前不能判断 threshold8 routing 是否优于 B005，也不能把它当作新基线。

**证据**

- [`../evidence/2026-08-03_b006_preflight.md`](../evidence/2026-08-03_b006_preflight.md)
- [`../submissions/B006/submission-manifest.json`](../submissions/B006/submission-manifest.json)
- [`../artifacts/kaggle/B006_v1/attack.py`](../artifacts/kaggle/B006_v1/attack.py)

**决策**

- 只监控 B006 submission `55203390`；不重复提交、不重推相同 Notebook。
- B005 submission `55185029` 的 Public Score `91.930` 仍是当前真实最佳。
- B006 未知期间不创建 B007；等待期间只做本地候选研究、公开参考审计和轨迹分析。

**下一门槛**

- 若 `55203390` 变为 `COMPLETE`，记录真实 Public Score、Private Score 的可见状态和首次观测
  终态时间。
- 按预注册：`>91.930` 才替换 B005；`>=100.000` 记为强竞争复现；空分、失败、超时或
  `<=91.930` 则拒绝且不重试。

## 2026-08-04：B006 rerun 完成但低于 B005，按预注册拒绝

**事实**

- submission `55203390` 从 `SubmissionStatus.PENDING` 变为 `SubmissionStatus.COMPLETE`。
- 2026-08-04 00:45 UTC 首次在本任务中观测到 B006 终态。
- Kaggle CLI 显示 Public Score `80.535`；Private Score 仍为空。
- 相对直接对照 B005 `91.930` 下降 `-11.395`。
- 该分数也低于历史 B003 `81.585`，说明 threshold8 routing 不只是未提升，而是明显伤害了真实 rerun 表现。

**解释与限制**

- 结果证伪 B006 的单变量假设：把 9-12 秒中速行从 plain 单 post 路由到 frame / four-endpoint
  分支，在本账号隐藏 rerun 中降低了有效得分。
- 本地 fake-clock 审计只验证了路由形状和候选数不变，不能代表隐藏模型 compliance 或 guardrail
  行为；本次真实分数说明中速行更可能应保留 plain 模板，或 frame 模板在该延迟段触发率更差。
- Private Score 当前不可见；最终候选选择仍以可见 Public rerun 和机制低相关性作为阶段依据。

**证据**

- [`../evidence/2026-08-03_b006_preflight.md`](../evidence/2026-08-03_b006_preflight.md)
- Kaggle submissions CLI：`55203390` `SubmissionStatus.COMPLETE`，Public Score `80.535`。

**决策**

- 按预注册拒绝 B006，不重试 B006，不重推相同 Notebook。
- B005 submission `55185029` 的 Public Score `91.930` 继续保持当前真实最佳。
- 下一候选 B007 必须以 B005 `91.930` 为直接对照，优先选择与 latency-threshold、tail-extension
  和 slow-row multi-post 低相关的机制；任何正式 submission 前必须先完成预注册、提交和推送。

**下一门槛**

- 审计尚未可靠复现的公开高分路线与本地原创机制，固定 B007 的来源哈希、唯一行为变量、
  接受/拒绝门槛和失败退出条件。
- B007 的接受门槛必须严格高于 `91.930`；`>=100.000` 记为强竞争复现；空分、失败、超时或
  `<=91.930` 拒绝且不重试。

## 2026-08-04：实现并预注册 B007 fast-row direct-burst 候选

**事实**

- 当前真实直接对照仍为 B005 submission `55185029`，Public Score `91.930`，Private Score 为空。
- B006 submission `55203390` 已按预注册拒绝，Public Score `80.535`，不得重试。
- 公开路线审计查询了当前公开 notebooks，并拉取 `dimong4/ai-agent-security`；该公开 notebook 的
  SHA-256 固定为
  `009c481f5dfa50bca2aa2255cc727b41269b39733dbc3efdccb5789a873e50c3`。
- B007 源码位于 `baselines/replaysafe_fastburst_v1/attack.py`，source commit `22a5bad`，
  SHA-256 为
  `269c8d2fcd2d431dc213309ef4c3c8e859fab1dc6ceb7811f9fd74ec002e0c5f`。
- 唯一行为变量是 post-classification fast/plain branch 的 `FAST_BURST_K` 从 `1` 改为 `2`。
  B005 的 `SPLIT_THRESHOLD_S=12.0`、`REPLAY_SAFE_FRAC=0.99`、`SLOW_MULTIPOST_N=4`、
  probe hops、保留域和 replay-cost 系数保持不变。
- B007 目标测试 3 项通过；全量测试 85 项通过；preflight、SDK 3.1.2 validate、Ruff、
  `git diff --check` 和新文件秘密扫描均通过。

**解释与限制**

- B007 是 fast/plain 行机制测试，不继续调整 B006 失败的 latency threshold，也不继续盲调 tail 或
  slow-row post count。
- 本地 9000 秒 fake-clock 审计只能证明路由形状：5-12 秒 fast/plain 行在首 8 个分类候选后使用
  二连 direct `http.post`；13 秒及以上 slow/frame 行保持 B005 的四端点 forge 形状。
- 公开 `dimong4/ai-agent-security` 仅作为 direct-burst 机制线索；B007 没有照搬其 `.co` URL 或全局
  `BURST_K=2` 配置，而是保留项目安全边界的唯一 `*.invalid` 目标域。
- 本地 fixture 不能预测隐藏模型是否会稳定执行两个 direct posts，也不能预测真实 Public Score。

**证据**

- [`../evidence/2026-08-04_b007_preflight.md`](../evidence/2026-08-04_b007_preflight.md)
- [`../baselines/replaysafe_fastburst_v1/attack.py`](../baselines/replaysafe_fastburst_v1/attack.py)
- [`../tests/test_replaysafe_fastburst.py`](../tests/test_replaysafe_fastburst.py)

**决策**

- 预注册 B007；必须先提交并推送本预注册文档，再允许构建唯一 B007 私有 Notebook。
- B007 的直接判定门槛固定为：Public Score `>91.930` 才替换 B005；`>=100.000` 记为强竞争复现；
  `<=91.930`、空分、失败或超时均拒绝且不重试。

**下一门槛**

- 构建 B007 私有 Notebook 前再次检查历史去重、候选哈希、manifest、动态样本契约、安全 URL、
  SDK validate、本地测试和秘密扫描。
- 云端 Notebook `COMPLETE` 后必须核验云端 `attack.py` SHA 与本地一致、日志错误扫描 0、
  产物秘密扫描 0；随后最多创建一次 B007 competition submission。

## 2026-08-04：创建 B007 唯一 Kaggle submission，等待真实评分

**事实**

- B007 预注册文档已在 commit `eaed697` 提交并推送。
- 使用 `scripts.build_kaggle_notebook` 构建私有 Notebook
  `heralces/ai-agent-security-b007-fastburst` version 1；manifest 绑定的 Git commit 为
  `eaed697f4554a36462ec75da5d91f79edbc1338b`。
- Kaggle Notebook v1 状态为 `COMPLETE`；下载的云端 `attack.py` SHA-256 与本地候选一致：
  `269c8d2fcd2d431dc213309ef4c3c8e859fab1dc6ceb7811f9fd74ec002e0c5f`。
- 云端运行日志错误扫描为 `0`；下载产物秘密扫描为 `0`。
- 正式提交前再次查询 Kaggle 历史，未发现 B007 或 attack hash prefix `269c8d2f` 的既有
  competition submission。
- 随后使用 Notebook output binding 创建唯一 B007 competition submission `55229800`。
- submission `55229800` 创建时间为 2026-08-04 04:58:47.290 UTC；截至本记录最新 CLI/API 观测为
  `SubmissionStatus.PENDING`，Public/Private Score 均为空。

**解释与限制**

- Notebook `COMPLETE`、manifest 绑定、云端哈希一致和日志/秘密扫描通过只证明 B007 正式提交前的
  产物可追溯；不代表隐藏 rerun 已完成评分。
- `submission.csv` 中的 `0.0` 仍只是 Code Competition 普通运行占位值，不是 leaderboard score。
- B007 出分前不能判断 fast-row direct-burst 是否优于 B005，也不能把 B007 当作新基线。

**证据**

- [`../evidence/2026-08-04_b007_preflight.md`](../evidence/2026-08-04_b007_preflight.md)
- [`../submissions/B007/submission-manifest.json`](../submissions/B007/submission-manifest.json)
- [`../artifacts/kaggle/B007_v1/attack.py`](../artifacts/kaggle/B007_v1/attack.py)

**决策**

- 只监控 B007 submission `55229800`；不重复提交、不重推相同 Notebook。
- B005 submission `55185029` 的 Public Score `91.930` 仍是当前真实最佳。
- B007 未知期间不创建 B008；等待期间只做本地候选研究、公开参考审计和轨迹分析。

**下一门槛**

- 若 `55229800` 变为 `COMPLETE`，记录真实 Public Score、Private Score 的可见状态和首次观测
  终态时间。
- 按预注册：`>91.930` 才替换 B005；`>=100.000` 记为强竞争复现；空分、失败、超时或
  `<=91.930` 则拒绝且不重试。

## 2026-08-05：B007 rerun 完成但低于 B005，按预注册拒绝

**事实**

- submission `55229800` 从 `SubmissionStatus.PENDING` 变为 `SubmissionStatus.COMPLETE`。
- 2026-08-05 07:48 UTC 首次在本任务中观测到 B007 终态。
- Kaggle CLI 显示 Public Score `76.905`；Private Score 仍为空。
- 相对直接对照 B005 `91.930` 下降 `-15.025`。
- 该分数低于 B006 `80.535` 和 B003 `81.585`，说明 fast/plain direct-burst 在本账号隐藏
  rerun 中明显伤害真实表现。

**解释与限制**

- B007 证伪了本次单变量假设：把 post-classification fast/plain branch 从单次 direct post
  改为二连 direct post 没有提升 Public Score，反而显著降低。
- 本地 fake-clock 审计只验证了 fast/plain burst2 与 slow/frame forge4 的路由形状；真实分数
  表明二连 direct prompt 可能降低执行合规率、有效 sink 命中率，或该 fast/plain 分支并非当前瓶颈。
- Private Score 当前不可见；阶段决策仍按预注册只使用可见 Public rerun 与可靠性状态。

**证据**

- [`../evidence/2026-08-04_b007_preflight.md`](../evidence/2026-08-04_b007_preflight.md)
- Kaggle submissions CLI：`55229800` `SubmissionStatus.COMPLETE`，Public Score `76.905`。

**决策**

- 按预注册拒绝 B007，不重试 B007，不重推相同 Notebook。
- B005 submission `55185029` 的 Public Score `91.930` 继续保持当前真实最佳。
- 下一正式候选 B008 必须以 B005 `91.930` 为直接对照，并优先选择与 fastburst、threshold、
  tail-extension 和 slow-row multipost 低相关的机制。

**下一门槛**

- 审计尚未可靠复现的公开高分路线与本地原创机制，固定 B008 的来源哈希、唯一行为变量、
  接受/拒绝门槛和失败退出条件。
- B008 的接受门槛必须严格高于 `91.930`；`>=100.000` 记为强竞争复现；空分、失败、超时或
  `<=91.930` 拒绝且不重试。

## 2026-08-05：实现并预注册 B008 replay-safe classify5 候选

**事实**

- 当前真实直接对照仍为 B005 submission `55185029`，Public Score `91.930`，Private Score 为空。
- B006 submission `55203390` 与 B007 submission `55229800` 均已按预注册拒绝且不得重试。
- 公开路线审计拉取了当前高票/高分公开 notebooks；B008 采用的机制线索来自
  `kaiwalyaatulraut/ai-agent-security-competition-solution`，Notebook SHA-256 为
  `0bf4faaf5b72b4ca58e8661909bbb4fb99005604701340154667fa78ec821ce9`。
- B008 源码位于 `baselines/replaysafe_classify5_v1/attack.py`，source commit `4b1ce2b`，
  SHA-256 为
  `4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1`。
- 唯一行为变量是 `SPLIT_CLASSIFY_N` 从 `8` 改为 `5`。B005 的 `SPLIT_THRESHOLD_S=12.0`、
  `REPLAY_SAFE_FRAC=0.99`、`SLOW_MULTIPOST_N=4`、`BURST_K=1`、probe hops、保留域和
  replay-cost 系数保持不变。
- B008 目标测试 3 项通过；全量测试 90 项通过；preflight、SDK 3.1.2 validate、Ruff、
  `git diff --check` 和新文件秘密扫描均通过。

**解释与限制**

- B008 不重复 B006 的 threshold routing，也不重复 B007 的 fast/plain direct-burst；它只减少
  慢行进入 B005 four-endpoint frame plan 之前的 plain classification 开销。
- 本地 9000 秒 fake-clock 审计显示 5/8/9/12 秒 fast/plain 行完全不变；13 秒和 20 秒 slow/frame
  行候选总数不变，但各多 3 个 four-endpoint forge 候选。
- 该改动的预期收益较窄；真实分数可能被隐藏 fixture mix、模型合规率或 leaderboard 方差淹没。

**证据**

- [`../evidence/2026-08-05_b008_preflight.md`](../evidence/2026-08-05_b008_preflight.md)
- [`../baselines/replaysafe_classify5_v1/attack.py`](../baselines/replaysafe_classify5_v1/attack.py)
- [`../tests/test_replaysafe_classify5.py`](../tests/test_replaysafe_classify5.py)

**决策**

- 预注册 B008；必须先提交并推送本预注册文档，再允许构建唯一 B008 私有 Notebook。
- B008 的直接判定门槛固定为：Public Score `>91.930` 才替换 B005；`>=100.000` 记为强竞争复现；
  `<=91.930`、空分、失败或超时均拒绝且不重试。

**下一门槛**

- 构建 B008 私有 Notebook 前再次检查历史去重、候选哈希、manifest、动态样本契约、安全 URL、
  SDK validate、本地测试和秘密扫描。
- 云端 Notebook `COMPLETE` 后必须核验云端 `attack.py` SHA 与本地一致、日志错误扫描 0、
  产物秘密扫描 0；随后最多创建一次 B008 competition submission。

## 2026-08-05：创建 B008 唯一 Kaggle submission，等待真实评分

**事实**

- B008 预注册文档已在 commit `34aaa89` 提交并推送。
- 使用 `scripts.build_kaggle_notebook` 构建私有 Notebook
  `heralces/ai-agent-security-b008-classify5` version 1；manifest 绑定的 Git commit 为
  `34aaa89d93d1b608862f4d3773f4ae98a0455e00`。
- Kaggle Notebook v1 状态为 `COMPLETE`；下载的云端 `attack.py` SHA-256 与本地候选一致：
  `4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1`。
- 云端运行日志错误扫描为 `0`；下载产物秘密扫描为 `0`。
- 正式提交前再次查询 Kaggle 历史，未发现 B008 或 attack hash prefix `4d433a77` 的既有
  competition submission。
- 随后使用 Notebook output binding 创建唯一 B008 competition submission `55266445`。
- submission `55266445` 创建时间为 2026-08-05 09:59:15.037 UTC；截至本记录最新 CLI/API 观测为
  `SubmissionStatus.PENDING`，Public/Private Score 均为空。

**解释与限制**

- Notebook `COMPLETE`、manifest 绑定、云端哈希一致和日志/秘密扫描通过只证明 B008 正式提交前的
  产物可追溯；不代表隐藏 rerun 已完成评分。
- `submission.csv` 中的 `0.0` 仍只是 Code Competition 普通运行占位值，不是 leaderboard score。
- B008 出分前不能判断 classify5 是否优于 B005，也不能把 B008 当作新基线。

**证据**

- [`../evidence/2026-08-05_b008_preflight.md`](../evidence/2026-08-05_b008_preflight.md)
- [`../submissions/B008/submission-manifest.json`](../submissions/B008/submission-manifest.json)
- [`../artifacts/kaggle/B008_v1/attack.py`](../artifacts/kaggle/B008_v1/attack.py)

**决策**

- 只监控 B008 submission `55266445`；不重复提交、不重推相同 Notebook。
- B005 submission `55185029` 的 Public Score `91.930` 仍是当前真实最佳。
- B008 未知期间不创建 B009；等待期间只做本地候选研究、公开参考审计和轨迹分析。

**下一门槛**

- 若 `55266445` 变为 `COMPLETE`，记录真实 Public Score、Private Score 的可见状态和首次观测
  终态时间。
- 按预注册：`>91.930` 才替换 B005；`>=100.000` 记为强竞争复现；空分、失败、超时或
  `<=91.930` 则拒绝且不重试。

## 2026-08-06：B008 rerun 完成并小幅刷新当前真实最佳

**事实**

- submission `55266445` 从 `SubmissionStatus.PENDING` 变为 `SubmissionStatus.COMPLETE`。
- 2026-08-06 11:27 UTC 首次在本任务中观测到 B008 终态。
- Kaggle CLI 显示 Public Score `92.165`；Private Score 仍为空。
- Kaggle API 对同一 ref 的 Public/Private 字段仍为空，`errorDescription` 为空；以 CLI 可见 Public Score
  作为本次真实 public 记录。
- 相对直接对照 B005 `91.930` 提升 `+0.235`。

**解释与限制**

- 结果支持 B008 的单变量假设：对已超过 12 秒阈值的慢行，把 `SPLIT_CLASSIFY_N` 从 `8` 降到
  `5`，在本账号隐藏 rerun 中略微提高了 Public Score。
- 提升幅度较小，说明 classify5 只是局部改善，并未突破强竞争参考线。
- B008 继续高于固定的 2026-07-30 top-200 参考线 `89.390`，但实时排名和奖牌边界会漂移；
  未重新核验实时 leaderboard 前不能声称进入奖牌区。

**证据**

- [`../evidence/2026-08-05_b008_preflight.md`](../evidence/2026-08-05_b008_preflight.md)
- [`../submissions/B008/submission-manifest.json`](../submissions/B008/submission-manifest.json)
- [`../artifacts/kaggle/B008_v1/attack.py`](../artifacts/kaggle/B008_v1/attack.py)

**决策**

- 按预注册接受 B008，替换 B005 成为新的真实参考基线。
- 当前真实最佳为 B008 submission `55266445`，Public Score `92.165`，Private Score 为空。
- 不重试 B008，不重推相同 Notebook。

**下一门槛**

- B009 必须以 B008 `92.165` 为直接对照。
- B009 需要机制低相关、可证伪、单变量；避免重复 B006 threshold8、B007 fastburst 或只盲调
  `SPLIT_CLASSIFY_N`。
- 接受门槛固定为 Public Score `>92.165`；`>=100.000` 记为强竞争复现；空分、失败、超时或
  `<=92.165` 拒绝且不重试。

## 2026-08-06：实现并预注册 B009 replay-safe probe4 候选

**事实**

- 当前真实直接对照为 B008 submission `55266445`，Public Score `92.165`，Private Score 为空。
- B009 源码位于 `baselines/replaysafe_probe4_v1/attack.py`，source commit `727ad45`，SHA-256 为
  `5fec8ee21232e8448d7cb17822b6e393ce33891ad20326c3eeb00b26581e63ff`。
- 唯一行为变量是 live validation 的 `PROBE_HOPS` 从 `0` 改为 `4`。B008 的
  `SPLIT_CLASSIFY_N=5`、`SPLIT_THRESHOLD_S=12.0`、`REPLAY_SAFE_FRAC=0.99`、
  `SLOW_MULTIPOST_N=4`、`BURST_K=1`、保留域和 replay-cost 系数保持不变。
- 公开路线审计拉取了 Foysal V15、Nikita 0011、tetsutani uniform recovery、haodou conservative
  replay-safe sizing 和 nctuan slow-multipost；B009 只采用 probe-hop 线索，不照搬 unsafe `.co`
  或多模板路线。
- B009 目标测试 3 项通过；全量测试 95 项通过；preflight、SDK 3.1.2 validate、Ruff、
  `git diff --check` 和秘密扫描均通过。

**解释与限制**

- B009 不改变候选消息、URL、安全域、slow-row four-endpoint frame plan 或 replay-safe tail；
  它只把 live fill 的 validation hop cap 降到 4。
- 本地常量时延 fake-clock 审计显示 B009 与 B008 返回候选数和候选消息形状完全一致，仅
  `max_tool_hops` 从 8 变为 4。
- 该本地审计不能证明隐藏 rerun 会变快；如果隐藏 env 在 4 次 tool call 后没有额外 wrap-up 成本，
  B009 可能中性。

**证据**

- [`../evidence/2026-08-06_b009_preflight.md`](../evidence/2026-08-06_b009_preflight.md)
- [`../baselines/replaysafe_probe4_v1/attack.py`](../baselines/replaysafe_probe4_v1/attack.py)
- [`../tests/test_replaysafe_probe4.py`](../tests/test_replaysafe_probe4.py)

**决策**

- 预注册 B009；必须先提交并推送本预注册文档，再允许构建唯一 B009 私有 Notebook。
- B009 的直接判定门槛固定为：Public Score `>92.165` 才替换 B008；`>=100.000` 记为强竞争复现；
  `<=92.165`、空分、失败或超时均拒绝且不重试。

**下一门槛**

- 构建 B009 私有 Notebook 前再次检查历史去重、候选哈希、manifest、动态样本契约、安全 URL、
  SDK validate、本地测试和秘密扫描。
- 云端 Notebook `COMPLETE` 后必须核验云端 `attack.py` SHA 与本地一致、日志错误扫描 0、
  产物秘密扫描 0；随后最多创建一次 B009 competition submission。

## 2026-08-06：创建 B009 唯一 Kaggle submission，等待真实评分

**事实**

- B009 预注册文档已在 commit `b84827b` 提交并推送。
- 使用 `scripts.build_kaggle_notebook` 构建私有 Notebook
  `heralces/ai-agent-security-b009-probe4` version 1；manifest 绑定的 Git commit 为
  `b84827b6e4cfc13553be933ee48706cbee619130`。
- Kaggle Notebook v1 状态为 `COMPLETE`；下载的云端 `attack.py` SHA-256 与本地候选一致：
  `5fec8ee21232e8448d7cb17822b6e393ce33891ad20326c3eeb00b26581e63ff`。
- 云端运行日志错误扫描为 `0`；下载产物与 Notebook bundle 的秘密扫描为 `0`。
- 正式提交前再次查询 Kaggle 历史，未发现 B009 或 attack hash prefix `5fec8ee2` 的既有
  competition submission。
- 随后使用 Notebook output binding 创建唯一 B009 competition submission `55299759`。
- submission `55299759` 创建时间为 2026-08-06 13:42:57.073 UTC；截至本记录最新 CLI/API 观测为
  `SubmissionStatus.PENDING`，Public/Private Score 均为空。

**解释与限制**

- Notebook `COMPLETE`、manifest 绑定、云端哈希一致和日志/秘密扫描通过只证明 B009 正式提交前的
  产物可追溯；不代表隐藏 rerun 已完成评分。
- `submission.csv` 中的 `0.0` 仍只是 Code Competition 普通运行占位值，不是 leaderboard score。
- B009 出分前不能判断 probe4 是否优于 B008，也不能把 B009 当作新基线。

**证据**

- [`../evidence/2026-08-06_b009_preflight.md`](../evidence/2026-08-06_b009_preflight.md)
- [`../submissions/B009/submission-manifest.json`](../submissions/B009/submission-manifest.json)
- [`../artifacts/kaggle/B009_v1/attack.py`](../artifacts/kaggle/B009_v1/attack.py)

**决策**

- 只监控 B009 submission `55299759`；不重复提交、不重推相同 Notebook。
- B008 submission `55266445` 的 Public Score `92.165` 仍是当前真实最佳。
- B009 未知期间不创建 B010；等待期间只做本地候选研究、公开参考审计和轨迹分析。

**下一门槛**

- 若 `55299759` 变为 `COMPLETE`，记录真实 Public Score、Private Score 的可见状态和首次观测
  终态时间。
- 按预注册：`>92.165` 才替换 B008；`>=100.000` 记为强竞争复现；空分、失败、超时或
  `<=92.165` 则拒绝且不重试。

## 2026-08-07：B009 rerun 以系统错误终态结束，按预注册拒绝

**事实**

- submission `55299759` 从 `SubmissionStatus.PENDING` 变为 `SubmissionStatus.ERROR`。
- 2026-08-07 07:30 UTC 首次在本任务中观测到 B009 终态。
- Kaggle CLI 的 Public/Private Score 均为空。
- Kaggle API 对同一 ref 的 `_public_score` / `_private_score` 均为 `None`，错误描述为：
  `A system error. Please try resubmitting to resolve the error and contact Kaggle Support if it persists.`
- 当前真实最佳仍为 B008 submission `55266445`，Public Score `92.165`，Private Score 为空。

**解释与限制**

- 该结果不能判定 probe4 的算法分数，只能判定 B009 本次正式 rerun 未产生可比较 Public Score。
- 虽然 Kaggle 错误信息建议 resubmitting，但本项目对每个候选最多正式提交一次；B009 的
  `ERROR` 终态按预注册作为可靠性失败处理。
- B009 不作为新基线，且不得重试或重推相同 Notebook。

**证据**

- [`../evidence/2026-08-06_b009_preflight.md`](../evidence/2026-08-06_b009_preflight.md)
- [`../submissions/B009/submission-manifest.json`](../submissions/B009/submission-manifest.json)
- [`../artifacts/kaggle/B009_v1/attack.py`](../artifacts/kaggle/B009_v1/attack.py)

**决策**

- 按预注册拒绝 B009，不重试 B009，不重推相同 Notebook。
- B008 submission `55266445` 的 Public Score `92.165` 继续保持当前真实最佳。
- 下一正式候选 B010 必须以 B008 `92.165` 为直接对照，并与 probe4、classify5、fastburst、
  threshold8、tail-extension 和 slow-row multipost 保持机制低相关。

**下一门槛**

- 审计尚未可靠复现的公开高分路线与本地原创机制，固定 B010 的来源哈希、唯一行为变量、
  接受/拒绝门槛和失败退出条件。
- B010 的接受门槛固定为 Public Score `>92.165`；`>=100.000` 记为强竞争复现；空分、失败、
  超时或 `<=92.165` 拒绝且不重试。

## 2026-08-07：实现并预注册 B010 slow-commentary 候选

**事实**

- 当前真实直接对照为 B008 submission `55266445`，Public Score `92.165`，Private Score 为空。
- B009 submission `55299759` 已按预注册作为可靠性失败拒绝，不重试、不重推。
- B010 源码位于 `baselines/replaysafe_slowcommentary_v1/attack.py`，source commit `236cf40`，
  SHA-256 为 `04eead5643b0240d69903cdb4ba3649a6f4ab7a6e496ad9b9b74b704eacfd8da`。
- B010 的父版本为 B008 `baselines/replaysafe_classify5_v1/attack.py`，SHA-256
  `4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1`。
- 唯一行为变量是 slow-row frame plan 的 injected channel 从 `analysis` 改为 `commentary`；
  B008 的 `SPLIT_CLASSIFY_N=5`、`SPLIT_THRESHOLD_S=12.0`、`REPLAY_SAFE_FRAC=0.99`、
  `SLOW_MULTIPOST_N=4`、`BURST_K=1`、`PROBE_HOPS=0`、保留域和 replay-cost 系数保持不变。
- 公开路线审计拉取了 `dimong4/ai-agent-security`、`assiaben/jed-attack-5-templates-aggressive-replay-0-99`、
  `anasriaz/ai-agent-security` 和 `nctuan/jed-slow-multipost`；B010 只采用 Assiaben
  notebook 中 commentary-channel injection 的窄线索，不复制五模板路线，不采用 unsafe `.co` URL。
- B010 目标测试 4 项通过；全量测试 101 项通过；preflight 通过；SDK 3.1.2 validate 通过。
- 9000 秒常量时延 fake-clock 审计显示 B010 与 B008 的返回候选数、URL 数和 `max_tool_hops`
  完全一致；仅 13s/20s slow-frame 行把 `<|channel|>analysis<|message|>` 换为
  `<|channel|>commentary<|message|>`。

**解释与限制**

- B010 不继续盲调 B006/B007/B008/B009 已测试过的 threshold、fastburst、classify batch、
  probe hops、tail fraction 或 slow-row endpoint count。
- 本地 fixture 只能证明单变量边界和候选形状，不包含 hidden model 的 channel 语义、guardrail
  和真实 rerun 合规漂移。
- 如果 hidden agent 更依赖 `analysis` channel 的规划语义，B010 可能低于 B008；这正是该候选的可证伪点。

**证据**

- [`../evidence/2026-08-07_b010_preflight.md`](../evidence/2026-08-07_b010_preflight.md)
- [`../baselines/replaysafe_slowcommentary_v1/attack.py`](../baselines/replaysafe_slowcommentary_v1/attack.py)
- [`../tests/test_replaysafe_slowcommentary.py`](../tests/test_replaysafe_slowcommentary.py)

**决策**

- 预注册 B010；必须先提交并推送本预注册文档，再允许构建唯一 B010 私有 Notebook。
- B010 的直接判定门槛固定为：Public Score `>92.165` 才替换 B008；`>=100.000` 记为强竞争复现；
  `<=92.165`、空分、失败或超时均拒绝且不重试。

**下一门槛**

- 构建 B010 私有 Notebook 前再次检查历史去重、候选哈希、manifest、动态样本契约、安全 URL、
  SDK validate、本地测试和秘密扫描。
- 云端 Notebook `COMPLETE` 后必须核验云端 `attack.py` SHA 与本地一致、日志错误扫描 0、
  产物秘密扫描 0；随后最多创建一次 B010 competition submission。

## 2026-08-07：创建 B010 唯一 Kaggle submission，等待真实评分

**事实**

- B010 预注册文档已在 commit `e91bf35` 提交并推送。
- 使用 `scripts.build_kaggle_notebook` 构建私有 Notebook
  `heralces/ai-agent-security-b010-slow-commentary` version 1；manifest 绑定的 Git commit 为
  `e91bf3583adebb7c24b4d1698336f456f0b477fa`。
- Kaggle Notebook v1 状态为 `COMPLETE`；下载的云端 `attack.py` SHA-256 与本地候选一致：
  `04eead5643b0240d69903cdb4ba3649a6f4ab7a6e496ad9b9b74b704eacfd8da`。
- 云端运行日志错误扫描为 `0`；下载产物秘密扫描为 `0`。
- 正式提交前再次查询 Kaggle 历史，未发现 B010 或 attack hash prefix `04eead56` 的既有
  competition submission。
- 随后使用 Notebook output binding 创建唯一 B010 competition submission `55327331`。
- submission `55327331` 创建时间为 2026-08-07 14:48:07.930 UTC；截至本记录最新 CLI/API 观测为
  `SubmissionStatus.PENDING`，Public/Private Score 均为空。

**解释与限制**

- Notebook `COMPLETE`、manifest 绑定、云端哈希一致和日志/秘密扫描通过只证明 B010 正式提交前的
  工程可靠性，不代表真实评分已提升。
- B010 出分前不能判断 slow-commentary 是否优于 B008，也不能把 B010 当作新基线。
- B010 是本候选的唯一正式 competition submission；不得重复提交或重推相同 Notebook。

**证据**

- [`../evidence/2026-08-07_b010_preflight.md`](../evidence/2026-08-07_b010_preflight.md)
- [`../submissions/B010/submission-manifest.json`](../submissions/B010/submission-manifest.json)
- [`../artifacts/kaggle/B010_v1/attack.py`](../artifacts/kaggle/B010_v1/attack.py)

**决策**

- 只监控 B010 submission `55327331`；不重复提交、不重推相同 Notebook。
- B008 submission `55266445` 的 Public Score `92.165` 仍是当前真实最佳。
- B010 未知期间不创建 B011；等待期间只做本地候选研究、公开参考审计和轨迹分析。

**下一门槛**

- 若 `55327331` 变为 `COMPLETE`，记录真实 Public Score、Private Score 的可见状态和首次观测
  终态时间。
- 按预注册：`>92.165` 才替换 B008；`>=100.000` 记为强竞争复现；空分、失败、超时或
  `<=92.165` 则拒绝且不重试。

## 2026-08-09：B010 rerun 完成但明显低于 B008，按预注册拒绝

**事实**

- submission `55327331` 从 `SubmissionStatus.PENDING` 变为 `SubmissionStatus.COMPLETE`。
- 2026-08-09 05:10 UTC 首次在本任务中观测到 B010 终态。
- Kaggle CLI 显示 Public Score `52.330`；Private Score 仍为空。
- Kaggle API 对同一 ref 返回 `status=SubmissionStatus.COMPLETE`、`_public_score='52.330'`、
  `_private_score=None`、`errorDescription=None`。
- 当前真实最佳仍为 B008 submission `55266445`，Public Score `92.165`，Private Score 为空。
- 同一次最新 submissions/API 查询中，若干历史有分 submission 的 status 字段显示为
  `SubmissionStatus.ERROR`，但仍保留 `_public_score` 且无 `errorDescription`；这被视为 Kaggle/API
  表示漂移，不改变先前已记录的 score-bearing 结果与当前最佳判断。

**解释与限制**

- `52.330` 直接证伪 B010 的 slow-commentary 假设：把 slow-row frame channel 从 `analysis`
  改为 `commentary` 在本账号真实 rerun 上明显伤害得分。
- 该结果支持保留 B008 的 `analysis` slow-frame 形状，不继续沿同一 channel-token 方向盲调。
- Private Score 当前不可见；阶段决策仍按预注册只使用可见 Public rerun 与可靠性状态。

**证据**

- [`../evidence/2026-08-07_b010_preflight.md`](../evidence/2026-08-07_b010_preflight.md)
- [`../submissions/B010/submission-manifest.json`](../submissions/B010/submission-manifest.json)
- [`../artifacts/kaggle/B010_v1/attack.py`](../artifacts/kaggle/B010_v1/attack.py)

**决策**

- 按预注册拒绝 B010，不重试 B010，不重推相同 Notebook。
- B008 submission `55266445` 的 Public Score `92.165` 继续保持当前真实最佳。
- 下一正式候选 B011 必须以 B008 `92.165` 为直接对照，并与 probe4、slow-commentary、
  classify5、fastburst、threshold8、tail-extension 和 slow-row multipost 保持机制低相关。

**下一门槛**

- 审计尚未可靠复现的公开高分路线与本地原创机制，固定 B011 的来源哈希、唯一行为变量、
  接受/拒绝门槛和失败退出条件。
- B011 的接受门槛固定为 Public Score `>92.165`；`>=100.000` 记为强竞争复现；空分、失败、
  超时或 `<=92.165` 拒绝且不重试。

## 2026-08-09：B011 首轮公开路线与本地机制筛查，暂不预注册

**事实**

- 当前真实最佳仍为 B008 submission `55266445`，Public Score `92.165`，Private Score 为空。
- 最新 Kaggle submissions 查询仍显示 B010 submission `55327331` 是最近一次正式提交，Public Score
  `52.330`，低于 B008；未发现 B011 competition submission。
- 只读拉取并审计了 Foysal V15、Anvith Pilk、tetsutani adaptive uniform、Canqiang、Nikita
  0011 和 PengWang fill-v26 等公开 Notebook，固定了 notebook/code SHA。
- 本地筛查了 replay 预算倍率和 slowest-row 预测余量两条小机制：`REPLAY_BUDGET_MULT` 提升在样本中
  不增加候选数；`SLOWEST_MULT` 从 `1.35` 收紧到 `1.15`/`1.05` 只在多数常量时延样本中增加约一个候选。

**解释与限制**

- 公开 adaptive template-bank 路线机制上与 B008 不同，但若直接采用会替换整套 prompt-selection
  机制，不满足当前 B011 的单变量边界。
- Foysal 的 frame-template override 与 B010 刚被证伪的 channel/prompt-token 方向相关，缺少足够证据继续消耗
  正式提交额度。
- `SLOWEST_MULT` 收紧是可审计的单变量想法，但本地增量过小，暂不值得用一次正式 Kaggle rerun 验证。

**证据**

- [`../evidence/2026-08-09_b011_public_audit.md`](../evidence/2026-08-09_b011_public_audit.md)

**决策**

- 本轮不预注册 B011，不构建 Notebook，不创建 competition submission。
- B008 submission `55266445` 的 Public Score `92.165` 继续保持当前真实最佳。

**下一门槛**

- 继续寻找机制低相关且单变量边界更强的 B011 候选。
- B011 预注册仍必须先固定来源/父版本哈希、候选源码 SHA、直接比较 B008 `92.165`、单一假设、
  接受/拒绝门槛和失败退出条件。

## 2026-08-09：当前 public leaderboard 使用 B010 分数，触发选择风险

**事实**

- 使用 Kaggle CLI 下载当前 public leaderboard，共 `816` 个 team rows。
- 账号/team `heralces` 当前 leaderboard 行显示 rank `637`、score `52.330`、last submission date
  `2026-08-07 14:48:07`，即 B010 的低分结果。
- 同一 leaderboard 快照中，如果按已记录的 B008 Public Score `92.165` 计算，约为 rank `59`；
  score_at_50 为 `92.655`，score_at_100 为 `90.055`，score_at_200 为 `88.065`。
- 最新 submissions 列表仍显示 B008 `92.165` 是本账号已观测的最高真实 rerun 分数，但 leaderboard
  当前没有使用该分数作为 team row。

**解释与限制**

- 这说明“当前真实最佳分数记录”和“当前 public leaderboard 可见排名”已经分离：B008 仍是历史最佳
  实验结果，但可见榜单行被 B010 `52.330` 拉低。
- 该现象需要尽快通过 Kaggle UI 的提交选择功能或明确授权的恢复策略处理；否则继续探索性提交可能继续
  牺牲可见 Public 排名。
- 本次审计没有自动重提 B008，因为这会违反既有“不重试/不重复提交相同候选”的纪律；当前 Kaggle CLI
  也没有暴露明确的 prior-submission selection 命令。

**证据**

- [`../evidence/2026-08-09_current_leaderboard_audit.md`](../evidence/2026-08-09_current_leaderboard_audit.md)

**决策**

- 暂停创建新的正式 competition submission，直到解决当前 leaderboard/提交选择风险。
- 继续保留 B008 `92.165` 为当前已观测最高真实分数，但不得把当前 public rank 写成 rank `59`；
  当前 leaderboard 下载中的账号可见 rank 是 `637`。

**下一门槛**

- 用户确认是否手动在 Kaggle UI 选择 B008 submission `55266445`，或授权一次狭义的 best-score
  restoration 例外。
- 在该选择风险解决前，只做本地研究、文档、公开路线审计和轨迹分析，不创建新的正式 competition
  submission。

## 2026-08-10：leaderboard 选择风险仍未解决，当前 rank 继续下滑

**事实**

- 再次使用 Kaggle CLI 查询 latest submissions，最新正式提交仍是 B010 submission `55327331`，
  Public Score `52.330`；未出现 B011 或新的 competition submission。
- 再次下载当前 public leaderboard，共 `910` 个 team rows。
- 账号/team `heralces` 当前 leaderboard 行显示 rank `711`、score `52.330`、last submission date
  `2026-08-07 14:48:07`。
- 同一 leaderboard 快照中，如果按已记录的 B008 Public Score `92.165` 计算，约为 rank `70`；
  score_at_50 为 `94.160`，score_at_100 为 `90.540`，score_at_200 为 `88.560`。

**解释与限制**

- 该结果确认 leaderboard/提交选择风险仍然存在，且随着参赛队伍和高分提交增加，B008 `92.165`
  对应的估算可见 rank 已从 `59` 漂移到约 `70`。
- 当前可见 public rank 是 B010 `52.330` 对应的 `711`，不能把 B008 的估算 rank 写成当前排名。
- 在用户没有确认选择/恢复策略前，继续创建正式提交会加重选择纪律和当前榜单排名之间的冲突。

**证据**

- [`../evidence/2026-08-09_current_leaderboard_audit.md`](../evidence/2026-08-09_current_leaderboard_audit.md)

**决策**

- 继续暂停新的正式 competition submission。
- 不重提 B008；等待用户手动选择 B008 或明确授权 best-score restoration 例外。

**下一门槛**

- 用户完成 Kaggle UI 选择或给出明确授权后，重新下载 leaderboard 核验 team row 是否恢复到 B008
  `92.165`。
- 若选择风险解决，再恢复 B011 预注册/提交流程；否则仅做本地研究和文档。

## 2026-08-10：B008 是 score-bearing ERROR，不能当作当前可选提交

**事实**

- 用户提供的 Kaggle submissions 截图显示 B008 行有警告/错误图标，但 Public Score 仍为 `92.165`。
- Kaggle API 对 B008 submission `55266445` 返回：
  `status=SubmissionStatus.ERROR`、`_public_score='92.165'`、`_private_score=None`、
  `error_description=''`。
- Kaggle Notebook worker 对 `heralces/ai-agent-security-b008-classify5` 返回
  `KernelWorkerStatus.COMPLETE`。
- B010 submission `55327331` 则返回 `SubmissionStatus.COMPLETE`、Public Score `52.330`，
  Notebook worker 同样为 `COMPLETE`。

**解释与限制**

- B008 的 Notebook 运行本身不是失败点；失败/警告状态来自 competition submission 层。
- B008 当前是“有分但 ERROR”的不一致状态，不应继续写成当前可选择或当前 leaderboard-effective
  submission。
- 当前可见 leaderboard row 仍使用 B010 `52.330`，所以不能把 B008 的估算 rank 写成当前排名。

**证据**

- [`../evidence/2026-08-10_b008_status_audit.md`](../evidence/2026-08-10_b008_status_audit.md)
- [`../evidence/2026-08-09_current_leaderboard_audit.md`](../evidence/2026-08-09_current_leaderboard_audit.md)

**决策**

- 暂停新的正式 competition submission。
- 不再建议“直接手动选择 B008”作为确定可行路径；当前应先处理 B008 score-bearing ERROR 状态。
- 不重提 B008，除非用户明确授权一次狭义 best-score restoration 例外。

**下一门槛**

- 若用户能在 Kaggle UI 或 Kaggle Support 层恢复/选择 B008，重新下载 leaderboard 核验 team row。
- 若无法恢复且用户授权 rerun，再按例外流程重新固定恢复目标、风险和退出条件。
- 否则仅继续本地研究、公开审计和 B011 设计，不创建新正式提交。

## 2026-08-10：用户授权 B008R 最佳分数恢复例外，先预注册再恢复

**事实**

- 用户明确授权“恢复最佳分数，授权所有操作”。
- 2026-08-10 01:42 UTC 重新核验 Kaggle API：B008 submission `55266445`
  当前为 `SubmissionStatus.ERROR`，但保留 Public Score `92.165`，Private Score 为空；
  B010 submission `55327331` 为 `SubmissionStatus.COMPLETE`，Public Score `52.330`。
- 重新下载 public leaderboard，共 `911` 个 team rows；账号/team `heralces` 当前行显示
  rank `712`、score `52.330`、last submission date `2026-08-07 14:48:07`。
- 同一 leaderboard 快照中，如果按 B008 `92.165` 计算，约为 rank `71`；
  score_at_50 为 `94.160`，score_at_100 为 `90.585`，score_at_200 为 `88.560`。
- B008R 恢复源固定为 B008 `baselines/replaysafe_classify5_v1/attack.py` 原样源码，
  SHA-256 `4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1`，
  size `10799` bytes；不改变任何算法行为变量。
- 恢复前本地检查通过：preflight PASS、SDK validate PASS、101 项测试通过、Ruff check 通过、
  Ruff format check 通过、`git diff --check` 通过、凭据值扫描 0。

**解释与限制**

- B008R 是用户授权下的狭义 best-score restoration 例外，不是 B011，不是新算法候选，也不改变
  B008 的 `SPLIT_CLASSIFY_N`、prompt、URL、tail fraction、slow multipost 或 replay-cost 系数。
- 这次恢复会消耗一次正式 competition submission，并有 hidden rerun 方差或再次被 Kaggle 标记为
  `ERROR` 的风险；因此必须先预注册并推送，再构建和提交。
- 当前可见 leaderboard rank 仍是 B010 `52.330` 对应的 `712`；B008 `92.165` 对应的 rank `71`
  只是同一快照下的估算，不是当前 rank。

**证据**

- [`../evidence/2026-08-10_b008_restore_exception.md`](../evidence/2026-08-10_b008_restore_exception.md)
- [`../evidence/2026-08-10_b008_status_audit.md`](../evidence/2026-08-10_b008_status_audit.md)
- [`../evidence/2026-08-09_current_leaderboard_audit.md`](../evidence/2026-08-09_current_leaderboard_audit.md)

**决策**

- 预注册 B008R 恢复例外；预注册文档提交并推送后，允许构建一个新的私有 Notebook
  `heralces/ai-agent-security-b008r-restore-classify5`。
- 云端 Notebook 必须 `COMPLETE`，云端 `attack.py` SHA 必须等于
  `4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1`，日志错误扫描和产物凭据值
  扫描必须通过。
- 最多创建一次 B008R competition submission；若 `COMPLETE` 且 Public Score `>=92.165`，记为历史最佳恢复；
  若 `52.330 < score < 92.165`，记为部分恢复；若 `<=52.330`、空分、失败或超时，记为恢复失败。

**下一门槛**

- 提交并推送本恢复预注册文档。
- 构建、推送并云端核验 B008R Notebook。
- 创建唯一 B008R competition submission 后记录 submission ref，并只监控该恢复提交直到终态。

## 2026-08-10：B008R 恢复提交已创建，等待 Kaggle 终态

**事实**

- B008R 恢复预注册文档已在 commit `2e45dd7` 提交并推送。
- 构建私有 Notebook `heralces/ai-agent-security-b008r-restore-classify5` v1，绑定
  `git_commit=2e45dd7945aa46d5cbfb7b9663bf514307a28eb5`。
- Kaggle Notebook v1 已完成，状态为 `KernelWorkerStatus.COMPLETE`。
- 下载云端产物到 `artifacts/kaggle/B008R_v1`；云端 `attack.py` SHA-256 为
  `4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1`，与 B008 本地源完全一致。
- `submission.csv` 已生成，大小 `88` bytes。
- 云端日志可操作错误扫描为 0；产物凭据值扫描为 0。
- 创建唯一 B008R competition submission `55393959`，创建时间为
  `2026-08-10 01:53:43.003 UTC`，初始状态为 `SubmissionStatus.PENDING`，Public/Private Score 均为空。

**解释与限制**

- 这是用户授权的最佳分数恢复例外，不是新的算法候选，不改变 B008 的任何行为变量。
- 当前只能说明恢复 submission 已进入 Kaggle 队列；尚不能说明 leaderboard 已恢复。
- 在 `55393959` 出终态前，不创建 B011 或其他正式 competition submission。

**证据**

- [`../evidence/2026-08-10_b008_restore_exception.md`](../evidence/2026-08-10_b008_restore_exception.md)
- `kaggle kernels status heralces/ai-agent-security-b008r-restore-classify5`
- `kaggle kernels output heralces/ai-agent-security-b008r-restore-classify5 -p artifacts/kaggle/B008R_v1 --force`
- `kaggle competitions submissions ai-agent-security-multi-step-tool-attacks -v`

**决策**

- 保留 B008R `55393959` 为唯一恢复提交；严禁重复创建相同恢复 submission。
- 按恢复预注册规则监控终态：`COMPLETE` 且 Public Score `>=92.165` 记为历史最佳恢复；
  `52.330 < score < 92.165` 记为部分恢复；`<=52.330`、空分、失败或超时记为恢复失败。

**下一门槛**

- 下一次只查询并监控 B008R submission `55393959`。
- 若 B008R 终态恢复成功，再重新下载 leaderboard 验证 team row；若失败，先评估 Kaggle Support
  或新候选策略，再决定是否恢复 B011。

## 2026-08-10：B008R 终态为 88.760，部分恢复榜单但未恢复历史高点

**事实**

- 2026-08-10 15:36 UTC 首次在本任务中观测到 B008R submission `55393959` 进入
  `SubmissionStatus.COMPLETE`。
- Kaggle CLI Public Score 为 `88.760`，Private Score 为空；Kaggle API model 的 raw
  `_public_score='88.760'`、`_private_score=None`、`errorDescription=None`。
- SDK 的 `publicScore` convenience accessor 返回 `None`，但 CLI、API raw score 与 leaderboard
  三者均一致为 `88.760`。
- 重新下载的 public leaderboard 共 `993` 个 team rows；team `heralces` 当前为 rank `205`、
  score `88.760`、last submission date `2026-08-10 01:53:43`、submission count `2`。
- 同一快照中，score_at_50=`94.645`、score_at_100=`90.810`、score_at_200=`88.830`；
  历史 B008 `92.165` 若有效计入约为 rank `79`。

**解释与限制**

- `52.330 < 88.760 < 92.165`，因此严格按预注册把 B008R 判为部分恢复：当前可见分数已从
  B010 `52.330` 恢复到 `88.760`，但没有恢复历史 B008 高点 `92.165`。
- 当前 rank `205` 是 leaderboard 的真实可见行；B008 `92.165` 对应的 rank `79` 只是同一快照
  下的估算，不能写成当前排名。
- 当前分数仅比 top-200 边界 `88.830` 低 `0.070`，但这不是奖牌边界；实时榜线仍会漂移。
- byte-identical B008R 与原 B008 相差 `3.405`，说明真实 rerun 存在显著波动；后续候选必须区分
  “改善当前 leaderboard-effective 分数”和“超过历史已观测高点”两种结论。

**证据**

- [`../evidence/2026-08-10_b008_restore_exception.md`](../evidence/2026-08-10_b008_restore_exception.md)
- `artifacts/kaggle/leaderboards/2026-08-10_1536_b008r_monitor/ai-agent-security-multi-step-tool-attacks.zip`
- `kaggle competitions submissions ai-agent-security-multi-step-tool-attacks -v`

**决策**

- 不重复提交 B008R，不重推相同 Notebook；恢复例外到此结束。
- 当前 leaderboard-effective 直接对照固定为 B008R `88.760`；B008 `92.165` 保留为历史已观测
  高点，只有候选 `>92.165` 才称为新的历史最佳。
- 恢复 B011 本地机制筛查；在形成更强的低相关单变量证据前，不创建新的正式 submission。

**下一门槛**

- B011 必须先固定父版本/来源哈希、候选源码 SHA、唯一行为变量和去重记录。
- B011 预注册至少同时报告：`>88.760` 为改善当前 effective 分数、`>92.165` 为刷新历史高点、
  `>=100.000` 为强竞争复现；空分、失败、ERROR、超时或 `<=88.760` 均拒绝且不重试。
- 继续避开已证伪或低证据方向：threshold8、fastburst、probe4、slow-commentary、重复 classify5
  恢复以及小幅预算余量盲调。

## 2026-08-11：预注册 B011 replay-safe fast-fill 单变量候选

**事实**

- 2026-08-11 13:06 UTC 重新下载 public leaderboard：team `heralces` 当前为 B008R `88.760`
  / rank `225`，top-200 边界 `89.100`；历史 B008 `92.165` 若计入约为 rank `85`。
- 审计 4 个最新公开 Notebook：`dimong4/ai-agent-security`、
  `kaiwalyaatulraut/ai-agent-security-competition-solution`、
  `koushikkumardinda/ai-agent-security-replay-safe-exfiltration` 和
  `verityix/ai-agent-security-attack-algorithm-hitherto`。
- 选择 B011 fast-fill 作为正式候选：父版本为 B008/B008R
  `baselines/replaysafe_classify5_v1/attack.py`，SHA-256
  `4d433a7736f9f9d90a03b96c40652236e5088f4fea4eeef2e5133216fa7490f1`。
- B011 源码为 `baselines/replaysafe_fastfill_v1/attack.py`，source commit `8b8c2b9`，
  SHA-256 `ff5b5fac23bdcea595e68abb201a1c8475df3c6e2cd36b1c805506292b2811c3`。
- 唯一行为变量：post-classification fast/plain branch 从 B008/B008R 的 single-post
  `TEMPLATE` 改为 reserved-domain `FILL_TEMPLATE`；前五条分类消息和 slow-row
  frame/multipost 分支保持不变。
- 本地检查通过：目标测试 19 项、全量测试 106 项、preflight、SDK validate、Ruff check、
  Ruff format check、`git diff --check` 和凭据值扫描。

**解释与限制**

- `dimong4` 只作为 fast-fill 机制线索；B011 不复制其 `.co` 目标或完整参数栈，并把邮箱目标安全适配为
  `admin@example.invalid`。
- B011 改变的是快行分类后的工具覆盖提示，不是 B006/B007/B008/B009/B010 的已证伪变量，也不是
  B008R 的重复恢复。
- 本地假环境只能证明候选数、URL 数、hops 与分支边界；不能证明 hidden scorer 会给 fast-fill 加分。

**证据**

- [`../evidence/2026-08-11_b011_fastfill_preflight.md`](../evidence/2026-08-11_b011_fastfill_preflight.md)
- `artifacts/kaggle/leaderboards/2026-08-11_1306_b011_resume/ai-agent-security-multi-step-tool-attacks.zip`
- `pytest -q`
- `python -m aicomp_sdk.cli.main validate redteam .\baselines\replaysafe_fastfill_v1\attack.py`

**决策**

- 预注册 B011；预注册文档提交并推送后，允许构建一个私有 Notebook
  `heralces/ai-agent-security-b011-fastfill` v1。
- B011 判定门槛固定为：Public Score `>88.760` 改善当前 leaderboard-effective 分数；
  `>92.165` 刷新历史高点；`>=100.000` 记为强竞争复现。
- Public Score `<=88.760`、空分、失败、`ERROR`、超时或重复路线均拒绝且不重试。

**下一门槛**

- 提交并推送本预注册文档。
- 构建并推送 B011 私有 Notebook v1，下载云端产物并核验 `attack.py` SHA、日志和秘密扫描。
- 确认历史 submission 列表不存在 B011 fast-fill 后，最多创建一次 competition submission，并只监控该
  submission 到终态。
