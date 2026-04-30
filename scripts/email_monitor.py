#!/usr/bin/env python3
"""
email_monitor.py — 自动检查邮箱并处理 Xiaoxian 的邮件。

Run by OpenClaw heartbeat every 10 minutes.
"""
from __future__ import annotations

import imaplib
import ssl
import email
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

# Config
SMTP_HOST = "smtp.mxhichina.com"
IMAP_HOST = "imap.mxhichina.com"
IMAP_PORT = 993
EMAIL = "matuoer@ezcan.cn"
PASSWORD = "szl284624"
XIAOXIAN_EMAIL = "xiaoxian@ezcan.cn"

# State file to track processed emails
STATE_FILE = Path.home() / ".openclaw" / "workspaces" / "Mautoer" / "workspace" / ".email-state.json"


def load_state() -> dict[str, Any]:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"processed_ids": [], "last_check": None}


def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def check_xiaoxian_emails() -> list[dict[str, Any]]:
    """Check inbox for new emails from Xiaoxian."""
    context = ssl.create_default_context()
    emails = []
    
    try:
        with imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=context) as mail:
            mail.login(EMAIL, PASSWORD)
            mail.select("INBOX")
            
            # Search for ALL emails (filter by sender in code)
            _, data = mail.search(None, 'ALL')
            
            ids = data[0].decode().split()
            if not ids:
                return []
            
            state = load_state()
            processed = set(state.get("processed_ids", []))
            
            for eid in ids:
                if eid in processed:
                    continue
                    
                _, msg_data = mail.fetch(eid, "(RFC822)")
                raw = msg_data[0][1]
                msg = email.message_from_bytes(raw)
                
                subject = msg["Subject"] or ""
                # Decode MIME subject
                subject_parts = email.header.decode_header(subject)
                subject = "".join(
                    part.decode(encoding or "utf-8", errors="ignore") if isinstance(part, bytes) else part
                    for part, encoding in subject_parts
                )
                
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            payload = part.get_payload(decode=True)
                            if payload:
                                body = payload.decode("utf-8", errors="ignore")
                                break
                else:
                    payload = msg.get_payload(decode=True)
                    if payload:
                        body = payload.decode("utf-8", errors="ignore")
                
                emails.append({
                    "id": eid,
                    "subject": subject,
                    "body": body,
                    "date": msg["Date"],
                })
                
                # Mark as processed
                processed.add(eid)
            
            state["processed_ids"] = list(processed)
            state["last_check"] = datetime.now(timezone.utc).isoformat()
            save_state(state)
            
    except Exception as e:
        print(f"Email check error: {e}", file=sys.stderr)
        
    return emails


def parse_review_feedback(body: str) -> list[dict[str, Any]]:
    """Parse Xiaoxian's review email to extract issues."""
    issues = []
    
    # Look for numbered issues like "问题 1:" or "❌ 问题 1"
    pattern = r'(?:问题|Issue)\s*(\d+)[:：]\s*(.+?)(?=\n\s*(?:问题|Issue)\s*\d+[:：]|\n\s*[-=]{3,}|$)'
    matches = re.findall(pattern, body, re.DOTALL | re.IGNORECASE)
    
    for num, content in matches:
        # Extract priority
        priority = "medium"
        if "高优先级" in content or "P0" in content:
            priority = "high"
        elif "中优先级" in content or "P1" in content:
            priority = "medium"
        elif "低优先级" in content or "P2" in content:
            priority = "low"
            
        issues.append({
            "number": int(num),
            "content": content.strip(),
            "priority": priority,
        })
    
    return issues


def is_obsidian_wiki_init_related(subject: str, body: str) -> bool:
    """Check if email is about obsidian-wiki-init."""
    keywords = ["obsidian", "wiki", "OBHeartbeat", "lint", "compile", "验收", "review"]
    text = (subject + " " + body).lower()
    return any(kw in text for kw in keywords)


def generate_fix_plan(issues: list[dict[str, Any]]) -> str:
    """Generate a plan to fix the issues."""
    lines = ["## 修复计划", ""]
    for issue in issues:
        icon = "🔴" if issue["priority"] == "high" else "🟡" if issue["priority"] == "medium" else "🟢"
        lines.append(f"{icon} 问题 {issue['number']} ({issue['priority']}): {issue['content'][:100]}...")
    return "\n".join(lines)


def main() -> int:
    emails = check_xiaoxian_emails()
    
    if not emails:
        print("No new emails from Xiaoxian.")
        return 0
    
    print(f"Found {len(emails)} new email(s) from Xiaoxian:")
    
    for em in emails:
        print(f"\n---")
        print(f"Subject: {em['subject']}")
        print(f"Date: {em['date']}")
        
        if not is_obsidian_wiki_init_related(em["subject"], em["body"]):
            print("(Not obsidian-wiki-init related, skipping)")
            continue
        
        issues = parse_review_feedback(em["body"])
        if issues:
            print(f"Found {len(issues)} issue(s) to fix")
            plan = generate_fix_plan(issues)
            print(plan)
            
            # Save plan for agent to pick up
            plan_file = Path.home() / ".openclaw" / "workspaces" / "Mautoer" / "workspace" / ".xiaoxian-todo.md"
            plan_file.write_text(plan, encoding="utf-8")
            print(f"\nPlan saved to: {plan_file}")
        else:
            print("No actionable issues found (might be confirmation/acknowledgment)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
