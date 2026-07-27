# Experiment ledger

每个有效实验追加一行，禁止只记录成功实验。

| ID | UTC date | Git commit | Hypothesis | Single change | Local evidence | Public score | Runtime | Decision |
|---|---|---|---|---|---|---:|---:|---|
| B000 | 2026-07-23 | 78ebc6e / 7cf2455 | 官方 starter 可以完成 competition rerun | 无，原样基线；仅补齐 Code Competition 占位输出 | SDK 3.1.2 validate 通过；deterministic fixture harness 已运行（不可与榜单比较）；私有 Notebook version 3 `COMPLETE`；云端 `attack.py` 哈希一致；submission `54925726` 完成 | 0.075 | 10:35 UTC 提交；12:40 UTC 首次观测完成（含排队，非算法运行时） | 保留为真实基线；下一步设计 E001 单变量提交 |
| B001 | 2026-07-27 | 0fe6d3c | 公开 replay-dense two-probe 路线可在本账号显著超过 0.075，并成为原创实验的新参考基线 | 有出处地复现公开 two-probe 方法；唯一安全适配是把任意 `.co` 改为唯一 `*.example.com` 保留域 | 上游 Notebook 哈希固定；54 项测试、preflight、Ruff、SDK validate 通过；120 秒确定性 agent 本地 0.00/0 finding，仅证明预算边界；[证据](../evidence/2026-07-27_b001_preflight.md) | — | 本地约 63 秒；尚无真实 rerun | 提交前；`>0.075` 保留，`>=60` 强复现，`<=0.075` 或失败则拒绝 |
| E001 | 2026-07-24 | d184f45 / c221fb6 | 自适应预算估计能在不侵占退出余量的前提下执行更多候选，并使 public score 高于 B000 的 0.075 | 用观测到的交互时延替换固定 180/360 秒门槛；prompt 与目标不变 | 220 秒控制器测试为 18 次 vs 固定门槛 5 次；统一 fixture 消融为 12 次 vs 4 次；preflight、42 项测试与 SDK 3.1.2 validate 通过；Notebook v1 `COMPLETE`、云端哈希一致；submission `54952586`；[证据](../evidence/2026-07-24_e001_preflight.md) | 0.075 | 13:50 UTC 提交；15:31 UTC 首次观测完成（含排队） | 与 B000 相同，未支持评分提升假设；保留为 E002 单变量对照，不重复提交 |
| E002 | 2026-07-26 | 748d9a4 / a0360da / b947bf1 | 优先覆盖不同成功工具调用签名能提高单位预算的新颖机制数，并使 public score 高于 E001 的 0.075 | 在 E001 上加入签名归一化、跨机制轮转、失败事件过滤与每签名保留上限；候选消息和自适应预算不变 | 首轮 4 次覆盖 4 种签名；失败调用不计入；假环境端到端回放通过；preflight、42 项测试、Ruff 与 SDK 3.1.2 validate 通过；Notebook v1 `COMPLETE`、云端哈希一致；submission `54995012`；[证据](../evidence/2026-07-26_e002_preflight.md) | 0.060 | 07:44 UTC 提交；12:15 UTC 首次观测完成（含排队，非算法运行时） | 比 E001 低 0.015，按预注册拒绝；不重复提交，不作为下一实验默认基础 |
| E003 | 2026-07-23 | 0db9fb6 | 只扩展已验证 source 状态并强制冷重放，可提高 evaluator 可复现率 | 在 E002 上加入 source-gated archive、分支去重与 fresh-reset replay gate | 失败 source 不 snapshot；仅 snapshot 成功但冷重放失败的候选被拒绝；23 项测试通过 | — | simulated | SDK replay 后决定 |
| E004 | 2026-07-23 | a0360da | 解析 SDK 3.1.2 原生 trace 后，实际工具新颖度与 source-gated snapshot 分支才会生效 | 工具事件兼容 `name/args/ok`，并排除 `ok=False` | 原生成功 `fs.read` 可建 archive，失败事件被拒绝；四版本 SDK validate 通过；38 项测试通过 | — | SDK contract | 保留；后续候选的必要兼容修复 |
| E005 | 2026-07-27 | c97de46 / d5f93d4 | 有墙钟和内存边界的 SDK Go-Explore 能比 E001 手写候选发现更多可重放高价值 cell，并使 public score 高于 0.075 | 用 SDK Go-Explore 替换固定九候选搜索；最多使用 80% 总预算且不超过 900 秒；不继承 E002 去重 | 原生和 5% 余量版本在 10 秒外层预算中超时；E005 完成但确定性 agent score 为 0.00；preflight、47 项测试、Ruff 与 SDK 3.1.2 validate 通过；Notebook v1 `COMPLETE`、云端哈希一致；submission `55014937`；[证据](../evidence/2026-07-27_e005_preflight.md) | 0.000 | 01:12 UTC 提交；02:14 UTC 首次观测完成（含排队，非算法运行时） | 比 E001 低 0.075，按预注册拒绝；本地 0.00 与真实 0.000 不得混淆；不重复提交 |

统一假时钟、假环境和独立冷重放的横向结果见
[`offline_ablation_v1.md`](offline_ablation_v1.md)，机器可读记录见
[`offline_ablation_v1.json`](offline_ablation_v1.json)。

规则：

1. 一个实验只检验一个主要假设；
2. 记录失败、空分、超时与环境异常；
3. 不用 public leaderboard 代替本地机制证据；
4. 最终提交必须能追溯到 commit、Notebook version 与完整配置；
5. 私榜候选至少保留两个机制低相关版本。
