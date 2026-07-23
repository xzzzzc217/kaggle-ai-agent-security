# Experiment ledger

每个有效实验追加一行，禁止只记录成功实验。

| ID | UTC date | Git commit | Hypothesis | Single change | Local evidence | Public score | Runtime | Decision |
|---|---|---|---|---|---|---:|---:|---|
| B000 | 2026-07-23 | 78ebc6e / 7cf2455 | 官方 starter 可以完成 competition rerun | 无，原样基线；仅补齐 Code Competition 占位输出 | SDK 3.1.2 validate 通过；deterministic fixture harness 已运行（不可与榜单比较）；私有 Notebook version 3 `COMPLETE`；云端 `attack.py` 哈希一致；submission `54925726` 完成 | 0.075 | 10:35 UTC 提交；12:40 UTC 首次观测完成（含排队，非算法运行时） | 保留为真实基线；下一步设计 E001 单变量提交 |
| E001 | 2026-07-23 | d184f45 | 自适应预算估计能在不侵占退出余量的前提下执行更多候选 | 用观测到的交互时延替换固定 180/360 秒门槛 | 220 秒模拟预算下 18 次 vs 固定门槛 5 次；8 项测试通过 | — | simulated | SDK replay 后决定 |
| E002 | 2026-07-23 | 748d9a4 | 优先覆盖不同工具调用签名能提高单位预算的新颖机制数 | 在 E001 上加入签名归一化、跨机制轮转与每签名保留上限 | 首轮 4 次覆盖 4 种签名；失败调用不计入；假环境端到端回放通过；17 项测试通过 | — | simulated | SDK replay 后决定 |
| E003 | 2026-07-23 | 0db9fb6 | 只扩展已验证 source 状态并强制冷重放，可提高 evaluator 可复现率 | 在 E002 上加入 source-gated archive、分支去重与 fresh-reset replay gate | 失败 source 不 snapshot；仅 snapshot 成功但冷重放失败的候选被拒绝；23 项测试通过 | — | simulated | SDK replay 后决定 |
| E004 | 2026-07-23 | a0360da | 解析 SDK 3.1.2 原生 trace 后，实际工具新颖度与 source-gated snapshot 分支才会生效 | 工具事件兼容 `name/args/ok`，并排除 `ok=False` | 原生成功 `fs.read` 可建 archive，失败事件被拒绝；四版本 SDK validate 通过；38 项测试通过 | — | SDK contract | 保留；后续候选的必要兼容修复 |

统一假时钟、假环境和独立冷重放的横向结果见
[`offline_ablation_v1.md`](offline_ablation_v1.md)，机器可读记录见
[`offline_ablation_v1.json`](offline_ablation_v1.json)。

规则：

1. 一个实验只检验一个主要假设；
2. 记录失败、空分、超时与环境异常；
3. 不用 public leaderboard 代替本地机制证据；
4. 最终提交必须能追溯到 commit、Notebook version 与完整配置；
5. 私榜候选至少保留两个机制低相关版本。
