# B005 replay-safe tail-extension variant

B005 is a single-variable child of B004. It keeps the B004 slow-row multi-post
prompting behavior unchanged and only moves the replay-safe sizing fraction from
`0.98` to `0.99`.

The hypothesis is narrow: B004 finished successfully at `0.98` and reached
Public Score `88.650`, only `0.740` below the fixed 2026-07-30 top-200
reference line `89.390`. A one-point tail extension may return a few more
validated candidates without changing the attack wording.

This is not a retry of B004 and does not change `SLOW_MULTIPOST_N`.
