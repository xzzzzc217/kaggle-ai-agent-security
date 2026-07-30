# B003 公开 replay-safe split 候选：本地准备记录

> 记录日期：2026-07-30
>
> 当前状态：本地候选已冻结；B002 submission `55110969` 仍在 `PENDING`，因此尚未预注册或提交 B003

## 1. 角色与来源

B003 不是原创算法实验，而是对公开 replay-safe split 路线的可追溯安全适配。直接来源为
公开 Kaggle Notebook [`nctuan/jed-v25`](https://www.kaggle.com/code/nctuan/jed-v25)。

本候选采用 2026-07-30 拉取的公开快照。该 Notebook 文件 SHA-256 为：

```text
2005325799dfed256e063428212d1259fdadaa6c3816ffac3ca5e400bbd8b5db
```

## 2. 固定实现与主要差异

B003 固定采用：

- 一次丢弃的冷启动；
- live validation-fill，只保留实际产生成功 marker post 的候选；
- 前 8 个候选用普通 verbose template 进行延迟分类；
- 若均值延迟高于 12 秒，则后续使用 Harmony control-token frame template；
- replay-safe sizing 使用 `0.98` replay fraction；
- 默认按 grader 配置的 `max_tool_hops` 探测，不启用 B002 的 1-hop 探测；
- `BURST_K=1` 且 `SLOW_MULTIPOST_N=1`，不启用 multi-post 放大。

本项目的安全适配是把公开实现中的任意 `.co` 改为唯一的 RFC 保留 `*.invalid` 目标。
SDK `http.post` 只写入离线 fixture 的 egress 记录，不执行真实网络请求。

## 3. 源码身份

```text
path=baselines/public_replaysafe_split_v1/attack.py
sha256=f9e19bec312a3fd4410506af1418463bd30254c5d4c024c3343007566e46d0b6
size=10721
experiment_id=B003
upstream=nctuan/jed-v25
upstream_sha256=2005325799dfed256e063428212d1259fdadaa6c3816ffac3ca5e400bbd8b5db
sdk=3.1.2
probe_hops=0
replay_safe_frac=0.98
split_by_latency=True
split_threshold_s=12.0
split_classify_n=8
url_suffix=.invalid
```

## 4. 本地证据与限制

- 全量 `pytest`：68 项通过；
- Ruff lint：通过；
- submission preflight：通过，0 error / 0 warning；
- SDK 3.1.2 `validate redteam`：syntax、imports、attack structure 全部通过；
- 假时钟回归确认：
  - 2,000 个 URL 唯一且全部属于 `*.invalid`；
  - structure-only path 只返回有界 fallback；
  - 默认探测使用 grader 配置的 hop cap；
  - 慢行延迟分类后会切换到 frame template；
  - 无成功候选时只返回有界 fallback。

本地确定性 agent 不保留请求中的 `SECRET_MARKER`，不能预测 GPT-OSS/Gemma 的 fire
rate、frame template 合规率或榜单成绩。B003 只作为 B002 出分后的后备候选；正式
预注册必须等 B002 终态后重新固定直接对照和门槛。

## 5. 当前决策

暂不创建 B003 Kaggle Notebook 或 competition submission。后续只在 B002 `55110969`
进入终态、且新预注册明确直接对照后，才允许 B003 消耗正式 rerun。
