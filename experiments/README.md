# Experiment ledger

每个有效实验追加一行，禁止只记录成功实验。

| ID | UTC date | Git commit | Hypothesis | Single change | Local evidence | Public score | Runtime | Decision |
|---|---|---|---|---|---|---:|---:|---|
| B000 | pending | pending | 官方 starter 可以完成 competition rerun | 无，原样基线 | SDK 尚未取得 | — | — | pending |
| E001 | 2026-07-23 | d184f45 | 自适应预算估计能在不侵占退出余量的前提下执行更多候选 | 用观测到的交互时延替换固定 180/360 秒门槛 | 220 秒模拟预算下 18 次 vs 固定门槛 5 次；8 项测试通过 | — | simulated | SDK replay 后决定 |
| E002 | 2026-07-23 | 748d9a4 | 优先覆盖不同工具调用签名能提高单位预算的新颖机制数 | 在 E001 上加入签名归一化、跨机制轮转与每签名保留上限 | 首轮 4 次覆盖 4 种签名；失败调用不计入；假环境端到端回放通过；17 项测试通过 | — | simulated | SDK replay 后决定 |

规则：

1. 一个实验只检验一个主要假设；
2. 记录失败、空分、超时与环境异常；
3. 不用 public leaderboard 代替本地机制证据；
4. 最终提交必须能追溯到 commit、Notebook version 与完整配置；
5. 私榜候选至少保留两个机制低相关版本。
