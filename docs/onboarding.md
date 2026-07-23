# Kaggle onboarding（账号所有者动作）

当前浏览器会话未登录 Kaggle，本机也没有 Kaggle API 凭证。下面几步涉及账号条款和私密 Token，必须由账号所有者完成。

## 1. 加入比赛

1. 打开：https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks
2. 登录 Kaggle。
3. 点击 **Join Competition**，阅读并接受规则。
4. 确认 Kaggle 个人资料已完成比赛所需的手机号/身份验证（若页面要求）。

最晚不能超过 **2026-08-25 23:59 UTC**，但为了保留完整冲榜周期，应立即完成。

## 2. 创建 API Token

在 Kaggle Settings 的 API 区域创建 Token。优先使用 Kaggle 当前推荐的 token 方式；若下载得到 `kaggle.json`，将其放到：

```text
C:\Users\21398\.kaggle\kaggle.json
```

不要把 Token 粘贴到聊天、Notebook、Git 或实验日志中。

## 3. 本地验证

在 `D:\kaggle` 运行：

```powershell
uv sync
.\.venv\Scripts\kaggle.exe competitions files ai-agent-security-multi-step-tool-attacks
```

若能列出比赛文件，即账号、规则与认证三项均已打通。

## 4. 完成信号

只需告知：“已加入比赛并配置 Token”。不要发送 Token 内容。随后即可自动下载 SDK、复现 baseline、创建首次提交并开始实验。
