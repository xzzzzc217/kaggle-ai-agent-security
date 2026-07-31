# B003 公开 replay-safe split 候选：本地准备记录

> 记录日期：2026-07-30
>
> 当前状态：B002 已以 `COMPLETE` 空分被拒绝；B003 已相对 B001 `65.340` 预注册，尚未提交

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
rate、frame template 合规率或榜单成绩。B002 的真实 rerun 为空分，不能作为数值对照；
因此 B003 的直接对照固定为仍有可比较分数的 B001。

## 5. 2026-07-31 正式预注册

**直接对照**：B001，submission `55030205`，Public Score `65.340`。

**假设**：相对 B001 的 two-probe 参考栈，B003 的 live validation-fill、延迟分流、
Harmony frame template 和 `0.98` replay-safe sizing 能在保持 rerun 可靠性的同时，
使 Public Score 严格高于 `65.340`。

固定判定如下：

| 真实结果 | 固定判定 |
|---|---|
| `COMPLETE` 且 Public Score `>65.340` | 保留 B003，作为新的真实参考基线 |
| Public Score `>=89.390` | 达到 2026-07-30 榜单快照的前 200 分数带 |
| Public Score `>=100.000` | 记为强竞争复现，优先在该栈上做原创单变量改进 |
| Public Score `<=65.340` | 未证明提升，拒绝且不替换 B001 |
| `ERROR`、`FAILED`、空分或 replay timeout | 因可靠性失败拒绝，不自动重试 |

只有在预注册文档提交并推送、源码哈希复核、preflight、SDK validate、测试、Kaggle
历史去重和云端 `attack.py` 哈希核对全部通过后，才允许创建一次 B003 competition
submission。每个候选最多提交一次；不得因 B002 空分而重试 B002。
