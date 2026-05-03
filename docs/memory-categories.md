# 全局 L1 分类规范（2026-05-03 生效）

> **适用范围**：所有 Agent 全局适用
> **Per-Agent 部分**：具体写入哪条 L1（日期、内容）是 per-agent 的

---

## 分类体系（6 分类）

按优先级从高到低，一条记忆**只进一个**分类：

| 优先级 | 分类 | 含义 | 入口 |
|--------|------|------|------|
| 1 | **RuleDecision** | 硬性规则、流程约束 | SelfEvolve 升级（纠正≥2次） |
| 2 | **SelfEvolve** | 纠错教训、知识、偏好 | 入口：所有纠正和知识先进入 |
| 3 | **SocialEcology** | 环境认知：角色/渠道/协作/系统 | SelfEvolve 分流（环境类知识） |
| 4 | **To-do** | 待办、搁置、承诺 | 直接写入 |
| 5 | **Output** | 已完成、交付物 | 直接写入 |
| 6 | **Event** | 兜底：其他客观事实 | 直接写入 |

**已删除**：CoreWork、EventsOutside（合并进 Event）

---

## 核心规则

1. **SelfEvolve 是入口**：所有纠正和知识先进入 SelfEvolve，再分流
2. **纠正 7 天计数制**：近 7 天内同一主题纠正次数
   - 1次：SelfEvolve 完整记录
   - 2次：SelfEvolve 改摘要+次数，完整内容提升到 RuleDecision
   - 3次+：SelfEvolve 更新次数标记
3. **知识分流**：属于系统/工具/组织的 → SocialEcology；个人/通用的 → 保留 SelfEvolve
4. **只记一次**：完整内容只在一个分类出现
5. **多日重复**：引用格式 `[4/27-持续] 摘要 + 今日进展`

---

## 包含分类定义的文件清单（修改时必须同步）

> 下次改分类时，直接改下面列出的所有文件。

| 文件 | 路径 | 包含分类内容的位置 |
|------|------|-------------------|
| **Skill 主文档** | `~/.openclaw/skills/memory-automation/SKILL.md` | §3.3 L1 格式示例、§3.4 格式规则表、§3.5 entries 示例 |
| **L1 写入器** | `~/.openclaw/skills/memory-automation/memory/l1_writer.py` | `CATEGORIES` 常量 |
| **心跳提醒** | `~/.openclaw/workspaces/Mautoer/workspace/scripts/memory_distill_reminder.py` | 完整规范输出 |
| **蒸馏规则草案** | `~/.openclaw/workspaces/Mautoer/workspace/memory-distill-rules-draft.md` | 详细分类解释+案例 |
| **Memory Rules** | `~/.openclaw/skills/memory-automation/memory-rules.md` | L1 存储规范（7分类 → 待同步） |
| **AGENTS.md** | `~/.openclaw/workspaces/Mautoer/workspace/AGENTS.md` | 当前无旧分类内容，无需改 |

---

## 分类边界速查

### SelfEvolve vs RuleDecision
- 纠正 1 次 → SelfEvolve（完整）
- 纠正 2 次 → RuleDecision（完整），SelfEvolve（摘要+次数）
- 用户说"必须/以后都/禁止" → RuleDecision

### SelfEvolve vs SocialEcology
- 属于系统/工具/组织 → SocialEcology
- 属于个人技能/通用 → SelfEvolve
- "飞书支持撤回" → SocialEcology
- "Python 3.12 新语法" → SelfEvolve

### 所有分类 vs Event
- 有规则/纠正/环境/待办/产出属性 → 不进 Event
- 排除后剩下的 → Event

---

*版本：2026-05-03*
*状态：已生效*
