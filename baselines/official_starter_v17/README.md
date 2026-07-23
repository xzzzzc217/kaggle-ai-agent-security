# Official starter baseline (version 17 observed 2026-07-22)

来源：https://www.kaggle.com/code/martynaplomecka/getting-started-notebook

Notebook 页面标注 Apache License 2.0。这里保存 `attack.py` 的可审计副本，目的是在取得比赛 SDK 后复现官方基线，不把它当作自主方案或最终提交。

官方页面显示该版本：

- 运行约 23 秒（页面展示的普通 notebook run，不等于隐藏 competition rerun）；
- 使用 `/kaggle/input/**/kaggle_evaluation` 定位 SDK；
- 导入 `aicomp_sdk`；
- 通过 `JEDAttackInferenceServer` 交付 `attack.py`；
- 页面展示 best score 0.075（V5），不应被视为当前版本或私榜保证。

取得比赛数据后，先原样复现，再做任何优化。
