---
title: "TOOLS.md Template"
summary: "Workspace template for TOOLS.md"
read_when:
  - Bootstrapping a workspace manually
---

# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## OpenClaw 配置

- **Workspace**: `/Users/binary/.openclaw/workspaces/Mautoer/workspace`
- **Account**: `Mautoer` (feishu channels)

## 飞书应用

- **名称**: `Mautoer`
- **App ID**: `cli_a92ab2c398625bdb`
- **App Secret**: `c2RvCUnFlTzg7b2sgd6RKfPlRQSGg0AI`

## Memory-Automation TODO 多维表

- **URL**: https://ijspedabjh.feishu.cn/base/EIKObhnhLa1KQIsle6wcAd6hnMb
- **App Token**: `EIKObhnhLa1KQIsle6wcAd6hnMb`
- **Table ID**: `tbltsQVg8sDlztYo`
- **名称**: Openclaw Todo
- **用途**: TODO 管理（项目 | 任务 | 任务描述 | 进展 | 重要紧急程度 等）
- **权限**: 用户 ou_83d6abde1b37e26ebac7059a9bc12da3 已授权 full_access

## 飞书 Bitable API

### 获取 Token
```bash
curl -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id": "cli_a92ab2c398625bdb", "app_secret": "c2RvCUnFlTzg7b2sgd6RKfPlRQSGg0AI"}'
```

### 创建多维表
```bash
curl -X POST "https://open.feishu.cn/open-apis/bitable/v1/apps" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"name": "表格名称"}'
```

### 创建字段
```bash
# 文本字段
curl -X POST "https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields" \
  -H "Authorization: Bearer {token}" \
  -d '{"field_name": "字段名", "type": 1}'

# 单选字段（options 为选项数组）
curl -X POST ".../fields" \
  -H "Authorization: Bearer {token}" \
  -d '{"field_name": "进展", "type": 3, "property": {"options": [{"name": "待开始"}, {"name": "进行中"}]}}'

# 日期字段
curl -X POST ".../fields" \
  -H "Authorization: Bearer {token}" \
  -d '{"field_name": "日期", "type": 5, "property": {"auto_fill": false, "date_formatter": "yyyy/MM/dd"}}'
```

### 创建记录
```bash
curl -X POST "https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "文本": "项目名",
      "任务": "任务名",
      "进展": "待开始",
      "重要紧急程度": "重要紧急"
    }
  }'
```

### 删除字段
```bash
curl -X DELETE "https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields/{field_id}" \
  -H "Authorization: Bearer {token}"
```

### 授予权限
```bash
curl -X POST "https://open.feishu.cn/open-apis/drive/v1/permissions/{app_token}/members?type=bitable" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "member_type": "openid",
    "member_id": "ou_用户openid",
    "perm": "full_access"
  }'
```

### 字段类型
| type | 说明 |
|------|------|
| 1 | 文本 |
| 2 | 数字 |
| 3 | 单选 |
| 4 | 多选 |
| 5 | 日期 |
| 17 | 附件 |

---

## Git 操作

### GitHub CLI
```bash
gh auth status          # 检查认证状态
gh auth refresh -h github.com  # 重新认证
gh auth git-credential  # push 认证（不是浏览器）
```

### Gitee
- **仓库**: https://gitee.com/tontonbinary/memory-automation
- **推送**: `git push gitee <branch>`

### GitCode
- **仓库**: https://gitcode.com/Binary_Wu/Mauto
- **Token**: `KsHU9_kAz5m5BK54xc2G-n-E`
- **API 认证**: `Authorization: Bearer <token>`
- **推送**: `git remote set-url gitcode https://oauth2:<token>@gitcode.com/Binary_Wu/Mauto.git`

### 常用操作
```bash
git push gitee main     # 推送到 Gitee
git push github main    # 推送到 GitHub
git push gitcode main   # 推送到 GitCode
gh repo sync            # 同步 GitHub 仓库
```

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Mautoer 飞书 TODO 多维表
- **URL**: https://ijspedabjh.feishu.cn/base/EIKObhnhLa1KQIsle6wcAd6hnMb
- **App Token**: `EIKObhnhLa1KQIsle6wcAd6hnMb`
- **Table ID**: `tbltsQVg8sDlztYo`
- **App ID**: `cli_a92ab2c398625bdb`（Mautoer 飞书应用）
- **App Secret**: `c2RvCUnFlTzg7b2sgd6RKfPlRQSGg0AI`
- ⚠️ feishu plugin 的 `feishu_bitable_*` 工具报错 "credentials not configured for account default"，需配置账号或改用 curl 直接调 API

## OpenClaw Skills 管理多维表
- **URL**: https://ijspedabjh.feishu.cn/base/AtVrbgqDga69tAsz98HczuGVnqd
- **App Token**: `AtVrbgqDga69tAsz98HczuGVnqd`
- **Table ID**: `tblH4i4MLF5N65K5`
- **用途**: Skills 目录管理（名称/来源/路径/功能描述/作者/版本/安装人/依赖工具）
- **同步**: `skadmin sync` 可同步到多维表

## Agent World
- **Skill 路径**: `~/.openclaw/workspaces/Mautoer/skills/agent-world/`（per-agent 安装）
- **API Key**: `agent-world-dc03ee264b8fe330d7892e26b8eff417f65e8f7dd77615be`
- **Username**: `mautoer`
- **Agent ID**: `d32b73c9-752c-46e5-9aee-bb0250db5bc5`
- **Profile**: https://friends.coze.site/profile/mautoer
- **调用示例**:
  ```bash
  curl https://world.coze.site/api/agents/profile/mautoer \
    -H "agent-auth-api-key: agent-world-dc03ee264b8fe330d7892e26b8eff417f65e8f7dd77615be"
  ```


## AgentLink（找笔友）
- **Xiaoxian**: https://friends.coze.site/profile/xiaoxian_ai
- **TS**: https://friends.coze.site/profile/tangshou
- 双向喜欢后解锁邮箱，可发邮件联络

## 虾评Skill 平台
- **平台**: https://xiaping.coze.site
- **user_id**: 905ae8f6-80dc-495e-8215-c4719aba96d0
- **API Key**: agent-world-dc03ee264b8fe330d7892e26b8eff417f65e8f7dd77615be
- **等级**: A2-1（虾米 32）

## InStreet（instreet.coze.site）
- **账号**: mautoer
- **API Key**: sk_inst_2a95311fc8badb75174b81f54d225c41
- **agent_id**: 8c0d0c61-3624-47f4-8f6a-1d2753af5732
- **发帖**: https://instreet.coze.site/post/5544520f-e1cd-4db4-bf99-db372ebad57b（Skill 分享区，评测 Agent记忆系统搭建指南 + mauto 推广）

## 阿里云企业邮箱
- **邮箱**: matuoer@ezcan.cn
- **SMTP**: smtp.mxhichina.com:465 (SSL)
- **IMAP**: imap.mxhichina.com:993 (TLS)
- **账号**: mautoer / szl284624
- **himalaya 配置**: `~/.config/himalaya/config.toml`（目前 himalaya 连接失败，改用 Python smtplib 直连）

### Agent 联系人
- **xiaoxian**: xiaoxian@ezcan.cn
- **TS**: TS@ezcan.cn

### 发邮件方法（Python smtplib）
```python
import smtplib, ssl
from email.message import EmailMessage

SMTP_HOST = "smtp.mxhichina.com"
SMTP_PORT = 465
EMAIL = "matuoer@ezcan.cn"
PASSWORD = "szl284624"
context = ssl.create_default_context()

msg = EmailMessage()
msg["From"] = f"Mautoer <{EMAIL}>"
msg["To"] = "收件地址"
msg["Subject"] = "主题"
msg.set_content("正文")

with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)
```

## Memory-Automation TODO（Fix 1-3）

### Fix 4: 群聊 session 不被蒸馏
- **文件**: `~/.openclaw/skills/memory-automation/memory/session_manager.py`
- **问题**: `get_current_session()` 用 `openclaw sessions --agent {agent_id}` 过滤，只拿当前 agent 下的 session。群聊 session 不属于特定 agent，导致群聊内容完全不会进入 L1 蒸馏流程
- **方案**: 改扫 session 文件再按 chat_type 筛选 group chat，不走 `--agent` 过滤
- **状态**: ✅ 已记入多维表（搁置）
