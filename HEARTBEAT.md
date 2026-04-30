## memory-automation
cd ~/.openclaw/skills/memory-automation && python3 -m memory.automation heartbeat --agent mautoer

## 每日维护检查报告
python3 ~/.openclaw/workspaces/Mautoer/workspace/scripts/daily_check_report.py

## OBHeartbeat (obsidian-wiki-init)
# 扫描知识库：检查 raw/ 待编译文件、wiki/ 健康状态
PYTHONPATH=~/.openclaw/skills/obsidian-wiki-init python3 -m obheartbeat scan "/Volumes/Binary HD/obsidian/Mautoer" --json
