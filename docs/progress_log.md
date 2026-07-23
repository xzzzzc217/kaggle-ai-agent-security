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
