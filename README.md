# Kaggle LLM Medal Project

本仓库服务于一个明确目标：在与 LLM/Agent 高度相关的 Kaggle 竞赛中获得奖牌或官方奖项，并把全过程沉淀为可核验的求职与深造材料。

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
- [x] 保存官方 starter baseline（待 SDK 到位后运行）
- [x] 建立离线测试骨架并完成自适应预算调度实验
- [ ] 登录 Kaggle、接受比赛规则并配置 API Token
- [ ] 下载竞赛 SDK/数据并完成官方 baseline 首次提交
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

## 立即行动

唯一需要账号所有者完成的动作记录在 [`docs/onboarding.md`](docs/onboarding.md)。完成后运行：

```powershell
uv sync
.\.venv\Scripts\kaggle.exe competitions files ai-agent-security-multi-step-tool-attacks
```

任何 API Token 都不得提交到本仓库。
