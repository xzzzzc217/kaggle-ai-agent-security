# Competition selection memo — 2026-07-22

## Decision

将 **AI Agent Security - Multi-Step Tool Attacks** 设为当前主赛。

这不是一般的 prompt engineering 活动，而是要求提交 `AttackAlgorithm` 的算法型红队竞赛。算法需要在确定性、离线、沙盒化的工具环境中搜索多步失败路径，并返回可重放的攻击候选。该问题直接覆盖 Agent、工具调用、间接 prompt injection、安全评测、搜索与推理，和 LLM 求职/研究申请的相关性极高。

## 加权标准

| 维度 | 权重 | 主赛判断 |
|---|---:|---|
| LLM/Agent 技术相关性 | 25% | 极高：真实工具型 Agent 与多步安全评测 |
| 主办方与研究认可度 | 20% | 极高：OpenAI、Google、IEEE |
| Kaggle 奖牌有效性 | 20% | Featured，明确显示 Points & Medals |
| 获奖可行性 | 15% | 中等：竞争强，但 SDK 离线、无需自训大模型 |
| 算力匹配 | 10% | 高：核心是搜索、轨迹和预算效率；本地 8GB GPU 可做原型 |
| 可公开展示性 | 10% | 极高：可形成算法、基准、消融和安全研究报告 |

## 主要候选比较

| 候选 | 优势 | 核心风险 | 定位 |
|---|---|---|---|
| AI Agent Security | 最贴近 LLM Agent；Featured 奖牌赛；强主办方；约六周可冲刺 | 已有大量队伍；私有 guardrail；code rerun 成本高 | **主赛** |
| ARC Prize 2026 ARC-AGI-2/3 | 顶级推理研究价值；奖金高；奖牌有效 | 赛场成熟、竞争极强、通常需要大量研究和计算资源 | 只跟踪，不分散主赛时间 |
| BenchFlow - Agent Skill Lift | Agent 技能与安全高度相关；参赛队少；适合作品集 | Hackathon 的评审与 Kaggle 竞赛奖牌不是同一目标 | 主赛结束后的备选项目 |
| Autonomous Agent Prediction (Beta) | Agent 自动建模概念新；参与人数少 | 当前奖励主要为 Swag，职业信号弱于 Featured medal | 不作为主赛 |
| CUHK-X Large/Small Model Track | 参赛人数少、奖金存在 | Community 赛认可度和奖牌状态不如 Featured 明确 | 备用，不抢主赛时间 |

## 决策门槛

主赛保持不变，除非出现以下任一事实：

1. 无法在 2026-07-25 前加入比赛或运行官方 SDK；
2. 规则限制与用户身份/地区/时间冲突；
3. 经过至少三次有效提交仍无法建立可解释的分数反馈；
4. 新开放的 Featured LLM 竞赛在认可度、剩余赛期和算力匹配上显著更优。

不能仅因为早期分数低或实现困难而换赛。
