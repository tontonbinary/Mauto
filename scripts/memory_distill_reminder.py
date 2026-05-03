#!/usr/bin/env python3
"""
Memory Distill Reminder - 心跳时输出 L1 蒸馏规范
基于入口机制：SelfEvolve → RuleDecision/SocialEcology 分流
"""

print("""
📋 L1 蒸馏规范（心跳提醒）

【入口机制】
所有纠正和知识 → 先进入 SelfEvolve → 再按规则分流

【纠正分流规则（7天计数制）】
纠正1次 → SelfEvolve 完整记录
纠正2次 → SelfEvolve 改摘要+次数，内容提升到 RuleDecision
纠正3次+ → SelfEvolve 更新次数标记

【知识分流规则】
跟系统/工具/组织有关 → SocialEcology
跟个人技能/通用知识有关 → SelfEvolve 保留

【6分类速查】
RuleDecision  = 硬性规则（2次纠正升级）
SelfEvolve    = 入口：纠正/知识/偏好/教训
SocialEcology = 环境认知：角色/渠道/协作/系统
To-do         = 待办/搁置/承诺
Output        = 已完成/交付物
Event         = 兜底：其他客观事实

【只记一次】
完整内容只在一个分类出现
纠正升级后，SelfEvolve 只留摘要标记

【自检清单】
□ SelfEvolve入口：纠正/知识正确分流了吗？
□ 纠正次数：近7天这个主题被纠正几次？够2次要升RuleDecision吗？
□ RuleDecision漏了吗？SocialEcology漏了吗？
□ To-do/Output漏了吗？
□ 近3天L1有重复吗？（有则引用不写全文）
□ 内容一句话精华？（超100字要压缩）
""")
