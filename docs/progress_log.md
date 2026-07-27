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
