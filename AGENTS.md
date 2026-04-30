---
title: "AGENTS.md Template"
summary: "Workspace template for AGENTS.md"
read_when:
  - Bootstrapping a workspace manually
---

# AGENTS.md - Your Workspace

This folder is home. Treat it that way.

## Session Startup

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. **标签懒加载模式**（替代全文读取）：
   - 读取当日 `memory/YYYY-MM-DD.md` 的**第一段：标签索引**
   - 直接加载 `memory/Patterns.md`（L2 成长记忆）
   - 直接加载 `MEMORY.md`（L3 长期记忆）
   - **不读取 L1 完整日志**，除非被标签索引触发召回
   - 回忆中触发标签 → 调取 L1 对应的完整内容
4. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`
5. **If in GROUP CHAT** (群聊场景): Also read `collaboration.md` — 这是群聊热规则

---

## 记忆管理

- **每日记录**：`memory/YYYY-MM-DD.md` — 原始日志
- **长期记忆**：`MEMORY.md` — 仅主会话加载

**铁律：写下来 > 记脑子里**

### ✅ 任务收尾检查（强制）

完成任何**非平凡**任务后，立即问自己：

1. **学到了什么新规则/坑？** → `~/.openclaw/workspaces/{agent_id}/workspace/memory/L2/patterns.md` 
2. **用户纠正了什么？** → `~/.openclaw/workspaces/{agent_id}/workspace/memory/L2/corrections.md`
3. **用户偏好有变化吗？** → `USER.md`
4. **工具有新问题/经验吗？** → `TOOLS.md`
5. **项目状态变了吗？** → `MEMORY.md` 或项目日志

**非平凡 = 多步操作/有决策/有反馈/耗时>5分钟**

### Wiki Vault

**Vault 路径**: `/Volumes/Binary HD/obsidian/Mautoer`
- 外部知识库，存储稳定信息（世界知识/周期性规律/环境认知）
- 高频使用和瞬时状态放 MEMORY.md

---

## 红线

- 绝不泄露隐私数据
- 破坏性操作必须确认

---

## External vs Internal

自由操作：读文件、搜索、整理
需请示：发邮件、公开发帖、出机器操作

---

## 💓 Heartbeats 

读  HEARTBEAT.md （如有）并执行，或回  HEARTBEAT_OK 
定期检查：项目状态
后台可做：整理记忆、提交代码


---

## 🧑‍💻 编码分级规则

| 级别 | 行数 | 执行方式 | 触发条件 |
|------|------|----------|----------|
| **1级** | ≤20 | 直接写 | 单文件、原子操作 |
| **2级** | 21~100 | 子代理 sessions_spawn | Skill/业务逻辑/多文件 |
| **3级** | >100 | OpenCode 或 claude code(acp) | 重构/调试/复杂 API |

**边界模糊时向上取整。Skill 开发和密钥配置强制 2 级。**

### 调用示例

```javascript
// 2级：子代理
sessions_spawn({ task: "...", model: "kimi-coding/k2.6", mode: "run" })

// 3级：OpenCode
sessions_spawn({ task: "...", runtime: "acp", agentId: "opencode", mode: "run" })
```


