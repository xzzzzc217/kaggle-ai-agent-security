# Kaggle onboarding（账号所有者动作）

状态：**已于 2026-07-23 完成**。账号已加入比赛，新版 API Token 已配置，
Kaggle CLI 可以列出竞赛文件。下面保留凭证轮换和故障恢复步骤。

## 1. 加入比赛

1. 打开：https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks
2. 登录 Kaggle。
3. 点击 **Join Competition**，阅读并接受规则。
4. 确认 Kaggle 个人资料已完成比赛所需的手机号/身份验证（若页面要求）。

最晚不能超过 **2026-08-25 23:59 UTC**，但为了保留完整冲榜周期，应立即完成。

## 2. 创建 API Token

在 Kaggle Settings 的 **API Tokens (Recommended)** 区域创建具名 Token。项目使用的
Kaggle CLI 1.8.4 支持新版 Token。将 Token 原文单独保存到：

```text
C:\Users\21398\.kaggle\access_token
```

文件中只放 Token 原文，不加引号，也不包装成 JSON。`kaggle.json` 仅用于
**Legacy API Credentials**，不要把新版 Token 写入该文件。

不要把 Token 粘贴到聊天、Notebook、Git、命令输出或实验日志中。若 Token
曾被回显，应立即在 Kaggle Settings 中撤销并重新生成。

## 3. 本地验证

在当前项目根目录运行（当前本地路径为
`D:\kaggle\ai-agent-security`）：

```powershell
uv sync
.\.venv\Scripts\kaggle.exe competitions files ai-agent-security-multi-step-tool-attacks
```

若能列出比赛文件，即账号、规则与认证三项均已打通。

## 4. 完成信号

轮换完成后只需告知：“已重新配置”。不要发送 Token 内容。验证过程只检查
文件是否存在并调用 Kaggle CLI，不读取或打印 Token。
