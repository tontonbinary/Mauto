# MEMORY.md — Long-Term Memory

_Last updated: 2026-04-05_

---

## 🧠 Core Identity
<!-- Agent identity, name, purpose, personality -->

## 👤 User
- **Name:** Binary / Bin兄 / 哥们儿
- **性格**：不喜欢废话，注重行动力
- **工作原则**：
  1. 自信度=责任心，低责任心导致假性自信度不足
  2. 核心工作必须先讨论→决定→执行，流程高度契合
  3. 有讨论外想法需先充分说明获认可再执行
  4. 有风险/不可逆操作必须先请示，说明风险等级，不确定时先查再答
  5. 备份空间：`/Volumes/Binary HD/claw/mission/Mautoer`

## 🏗️ Projects → 详见 [[wiki/项目/Mauto.md]]

## 💰 Business
<!-- Metrics, revenue, unit economics -->

## 👥 People & Team
- **xiaoxian**: 提供了飞书账号隔离机制指导
- **agent_xiaoxian**: 提供飞书账号隔离机制指导，解决 Mautoer 账号读取飞书文档的凭证问题

## 🎯 Strategy
- **LLM vs 脚本分工原则**：
  - 语义理解/分类/内容判断类任务 → 交给 LLM 处理
  - 结构化枚举/来源/时间/路径等脚本可识别字段 → 脚本处理
  - 例：功能分类用 LLM；来源/安装日期/归属可用脚本
- **飞书API调用**: 必须指定 accountId="Mautoer"，否则默认用 default 账号导致凭证找不到
- **Git平台策略**: GitHub + GitCode 为准，Gitee暂不使用（仓库被误标为企业仓库，API有限制）
- **备份空间**: `/Volumes/Binary HD/claw/mission/Mautoer` — 有风险/需留余量的工作放这里

## 📌 Key Decisions → 详见 [[wiki/项目/Mauto.md]]

## 💡 Lessons Learned → 详见 [[wiki/项目/Mauto.md]]


## 🔧 Environment
- **测试环境**: ~/mauto-test/（隔离于production）
- **备份空间**: `/Volumes/Binary HD/claw/mission/Mautoer`
- **HEARTBEAT.md**: 必须是实际可执行命令格式（非纯#注释），否则OpenClaw心跳检查会跳过（正则跳过#开头行和空checklist项）
- **Exec**: 免审批配置（tools.exec.ask off + tools.exec.security full）
- **飞书应用**: Mautoer app (cli_a92ab2c398625bdb)，调用API需指定 accountId="Mautoer"
- **MiniMax API**: sk-cp-v2rdxRY...(MiniMax-M2.5模型)

## 🌊 Open Threads
- [[reply_to_current]] 群聊 session 不被蒸馏到 L1（Fix 4，记入飞书多维表，搁置状态）
- [[reply_to_current]] pending_queue 缓冲补救（Fix 3，TODO，可后做）
