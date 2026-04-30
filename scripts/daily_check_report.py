#!/usr/bin/env python3
"""
每日维护检查报告
运行所有检查项并生成报告，发送到指定渠道
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path


def run_cmd(cmd: list, timeout: int = 10) -> tuple:
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def check_gateway() -> dict:
    """检查 Gateway 状态"""
    ok, stdout, stderr = run_cmd(["openclaw", "gateway", "status"])
    return {
        "name": "1. Gateway 状态",
        "status": "✅ 正常" if ok and "running" in stdout else "❌ 异常",
        "detail": stdout[:100] if stdout else stderr[:100]
    }


def check_board() -> dict:
    """检查 Board 状态"""
    board_dir = Path.home() / ".openclaw" / "shared" / "board"
    try:
        files = list(board_dir.glob("*.md"))
        index_file = board_dir / "index.md"
        return {
            "name": "2. Board 状态",
            "status": "✅ 正常",
            "detail": f"{len(files)} 个项目文件，index: {'✅' if index_file.exists() else '❌'}"
        }
    except Exception as e:
        return {"name": "2. Board 状态", "status": "❌ 异常", "detail": str(e)}


def check_mail() -> dict:
    """检查邮件系统（阿里云企业邮箱）"""
    try:
        import smtplib, ssl
        SMTP_HOST = "smtp.mxhichina.com"
        SMTP_PORT = 465
        EMAIL = "matuoer@ezcan.cn"
        PASSWORD = "szl284624"
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=5) as server:
            server.login(EMAIL, PASSWORD)
        
        return {
            "name": "3. 邮件系统",
            "status": "✅ 正常",
            "detail": f"阿里云企业邮箱: {EMAIL}"
        }
    except Exception as e:
        return {"name": "3. 邮件系统", "status": "❌ 异常", "detail": str(e)}


def check_heartbeat() -> dict:
    """检查 HEARTBEAT.md 可执行"""
    hb_file = Path.home() / ".openclaw" / "workspaces" / "Mautoer" / "workspace" / "HEARTBEAT.md"
    try:
        content = hb_file.read_text(encoding="utf-8")
        # 检查是否有可执行命令
        commands = [line for line in content.split("\n") if line.startswith("python3") or line.startswith("cd ")]
        return {
            "name": "4. Heartbeat 配置",
            "status": "✅ 正常",
            "detail": f"{len(commands)} 个检查命令"
        }
    except Exception as e:
        return {"name": "4. Heartbeat 配置", "status": "❌ 异常", "detail": str(e)}


def check_memory_auto() -> dict:
    """检查 memory-automation 状态"""
    try:
        sessions_dir = Path.home() / ".openclaw" / "agents" / "mautoer" / "sessions"
        files = list(sessions_dir.glob("*.jsonl"))
        
        memory_dir = Path.home() / ".openclaw" / "workspaces" / "Mautoer" / "workspace" / "memory"
        today = datetime.now().strftime("%Y-%m-%d")
        today_file = memory_dir / f"{today}.md"
        
        # 同时检查 clean_session
        clean_dir = Path.home() / ".openclaw" / "agents" / "mautoer" / "clean_session"
        clean_files = list(clean_dir.glob(f"{today}*.json"))
        
        status = "✅ 正常"
        detail = f"sessions: {len(files)} 个, 今日clean: {'✅' if clean_files else '❌'}"
        if not today_file.exists():
            status = "⚠️ L1未生成"
            detail += f", L1: ❌"
        else:
            detail += f", L1: ✅"
        
        return {
            "name": "5. Memory Automation",
            "status": status,
            "detail": detail
        }
    except Exception as e:
        return {"name": "5. Memory Automation", "status": "❌ 异常", "detail": str(e)}


def check_skills() -> dict:
    """检查 Skill 状态"""
    skills_dir = Path.home() / ".openclaw" / "skills"
    try:
        skills = [d.name for d in skills_dir.iterdir() if d.is_dir()]
        
        # 检查关键 skill
        key_skills = ["agent-board", "obsidian-wiki-init", "memory-automation"]
        missing = [s for s in key_skills if s not in skills]
        
        status = "✅ 正常" if not missing else "⚠️ 部分缺失"
        detail = f"{len(skills)} 个 skill"
        if missing:
            detail += f", 缺失: {', '.join(missing)}"
        
        return {
            "name": "6. Skill 状态",
            "status": status,
            "detail": detail
        }
    except Exception as e:
        return {"name": "6. Skill 状态", "status": "❌ 异常", "detail": str(e)}


def check_obsidian_wiki() -> dict:
    """检查 obsidian-wiki-init"""
    try:
        ob_dir = Path.home() / ".openclaw" / "skills" / "obsidian-wiki-init"
        scripts = list((ob_dir / "scripts").glob("*.py")) if (ob_dir / "scripts").exists() else []
        
        # 检查 obheartbeat
        obheartbeat_ok = (ob_dir / "obheartbeat" / "__init__.py").exists()
        
        return {
            "name": "7. obsidian-wiki-init",
            "status": "✅ 正常",
            "detail": f"scripts: {len(scripts)} 个, obheartbeat: {'✅' if obheartbeat_ok else '❌'}"
        }
    except Exception as e:
        return {"name": "7. obsidian-wiki-init", "status": "❌ 异常", "detail": str(e)}


def check_disk_space() -> dict:
    """检查磁盘空间"""
    ok, stdout, stderr = run_cmd(["df", "-h"], timeout=5)
    if ok:
        # 解析根目录使用率
        lines = stdout.split("\n")
        for line in lines:
            if line.endswith("/") or "/System/Volumes/Data" in line:
                parts = line.split()
                if len(parts) >= 5:
                    usage = parts[4].replace("%", "")
                    try:
                        usage_int = int(usage)
                        status = "✅ 正常" if usage_int < 80 else "⚠️ 空间不足" if usage_int < 90 else "❌ 空间严重不足"
                        return {
                            "name": "8. 磁盘空间",
                            "status": status,
                            "detail": f"使用率: {usage}"
                        }
                    except:
                        pass
    
    return {"name": "8. 磁盘空间", "status": "⚠️ 无法获取", "detail": stderr[:100]}


def check_config() -> dict:
    """检查 OpenClaw 配置"""
    config_file = Path.home() / ".openclaw" / "openclaw.json"
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        
        # 检查关键配置
        has_broadcast = "broadcast" in config
        has_bindings = "bindings" in config
        
        return {
            "name": "9. OpenClaw 配置",
            "status": "✅ 正常",
            "detail": f"broadcast: {'✅' if has_broadcast else '❌'}, bindings: {'✅' if has_bindings else '❌'}"
        }
    except Exception as e:
        return {"name": "9. OpenClaw 配置", "status": "❌ 异常", "detail": str(e)}


def check_git_status() -> dict:
    """检查 Git 状态"""
    workspace = Path.home() / ".openclaw" / "workspaces" / "Mautoer" / "workspace"
    try:
        ok, stdout, stderr = run_cmd(["git", "-C", str(workspace), "status", "--short"], timeout=5)
        if ok:
            changes = stdout.strip()
            if changes:
                lines = changes.split("\n")
                return {
                    "name": "10. Git 状态",
                    "status": "⚠️ 有未提交变更",
                    "detail": f"{len(lines)} 个文件未提交"
                }
            else:
                return {
                    "name": "10. Git 状态",
                    "status": "✅ 正常",
                    "detail": "工作区干净"
                }
        else:
            return {"name": "10. Git 状态", "status": "⚠️ 无法检查", "detail": stderr[:100]}
    except Exception as e:
        return {"name": "10. Git 状态", "status": "❌ 异常", "detail": str(e)}


def generate_report() -> str:
    """生成检查报告"""
    checks = [
        check_gateway(),
        check_board(),
        check_mail(),
        check_heartbeat(),
        check_memory_auto(),
        check_skills(),
        check_obsidian_wiki(),
        check_disk_space(),
        check_config(),
        check_git_status(),
    ]
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    weekday = datetime.now().strftime("%A")
    
    lines = [
        f"# Mautoer 每日维护检查报告",
        f"",
        f"**检查时间**: {now} ({weekday})",
        f"",
        f"## 检查结果",
        f"",
    ]
    
    for check in checks:
        lines.append(f"### {check['name']}")
        lines.append(f"- **状态**: {check['status']}")
        lines.append(f"- **详情**: {check['detail']}")
        lines.append(f"")
    
    # 统计
    ok_count = sum(1 for c in checks if "✅" in c['status'])
    warning_count = sum(1 for c in checks if "⚠️" in c['status'])
    error_count = sum(1 for c in checks if "❌" in c['status'])
    
    lines.extend([
        f"---",
        f"",
        f"**统计**: ✅ {ok_count} 项正常，⚠️ {warning_count} 项警告，❌ {error_count} 项异常",
        f"",
        f"_自动生成的每日检查报告_",
    ])
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 生成报告
    report = generate_report()
    
    # 运行各项检查（用于判断异常和发送告警）
    checks = [
        check_gateway(),
        check_board(),
        check_mail(),
        check_heartbeat(),
        check_memory_auto(),
        check_skills(),
        check_obsidian_wiki(),
        check_disk_space(),
        check_config(),
        check_git_status(),
    ]
    
    # 保存到本地（独立目录，不在 board 里）
    report_dir = Path.home() / ".openclaw" / "shared" / "reports" / "daily-check"
    report_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = report_dir / f"daily-check-{today}.md"
    report_file.write_text(report, encoding="utf-8")
    
    # 发送飞书消息（每天）- 使用 HTTP API
    feishu_result = {"sent": False, "error": ""}
    try:
        import requests
        
        # 获取 tenant_access_token
        token_resp = requests.post(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={"app_id": "cli_a92ab2c398625bdb", "app_secret": "c2RvCUnFlTzg7b2sgd6RKfPlRQSGg0AI"},
            timeout=10
        )
        token_data = token_resp.json()
        token = token_data.get("tenant_access_token", "")
        
        if token:
            # 截断消息避免过长（飞书单条消息限制）
            msg_short = report[:2800] if len(report) > 2800 else report
            
            resp = requests.post(
                "https://open.feishu.cn/open-apis/im/v1/messages",
                headers={"Authorization": f"Bearer {token}"},
                params={"receive_id_type": "open_id"},
                json={
                    "receive_id": "ou_83d6abde1b37e26ebac7059a9bc12da3",
                    "msg_type": "text",
                    "content": json.dumps({"text": msg_short})
                },
                timeout=15
            )
            feishu_result = {
                "sent": resp.status_code == 200 and resp.json().get("code") == 0,
                "status_code": resp.status_code,
                "response": resp.text[:300]
            }
        else:
            feishu_result = {"sent": False, "error": "无法获取 token"}
    except Exception as e:
        feishu_result = {"sent": False, "error": str(e)}
    
    # 检查是否有异常/警告，有则 iMessage 通知
    abnormal_checks = [c for c in checks if "❌" in c['status'] or "⚠️" in c['status']]
    imsg_result = {"sent": False, "error": ""}
    
    if abnormal_checks:
        # 构建异常摘要
        alert_lines = ["⚠️ Mautoer 维护异常告警", ""]
        for c in abnormal_checks:
            emoji = "❌" if "❌" in c['status'] else "⚠️"
            alert_lines.append(f"{emoji} {c['name']}: {c['detail']}")
        alert_lines.append("")
        alert_lines.append(f"完整报告: {report_file}")
        alert_msg = "\n".join(alert_lines)
        
        try:
            result = subprocess.run(
                ["imsg", "send", "--to", "tontonbin@msn.com", "--text", alert_msg, "--service", "imessage"],
                capture_output=True, text=True, timeout=30
            )
            imsg_result = {
                "sent": result.returncode == 0,
                "stdout": result.stdout[:200],
                "stderr": result.stderr[:200] if result.stderr else ""
            }
        except Exception as e:
            imsg_result = {"sent": False, "error": str(e)}
    
    # 输出结果
    has_alert = len(abnormal_checks) > 0
    print(json.dumps({
        "success": feishu_result.get("sent"),
        "report_file": str(report_file),
        "feishu_result": feishu_result,
        "abnormal_count": len(abnormal_checks),
        "imessage_alert": has_alert,
        "imsg_result": imsg_result
    }, ensure_ascii=False, indent=2))
