import sys
import json
import re

def main():
    input_data = json.loads(sys.stdin.buffer.read().decode("utf-8", errors="replace"))
    output_content = str(input_data.get("output", ""))
    lower = output_content.lower()

    junk_keywords = ["reflected xss without version", "clickjacking (low impact)"]
    is_junk = any(kw in lower for kw in junk_keywords)
    may_contain_secret = bool(re.search(
        r"(?i)(authorization:\s*(?:bearer|basic)\s+\S+|set-cookie:\s*\S+|"
        r"eyJ[A-Za-z0-9_-]{4,}\.[A-Za-z0-9_-]{4,}\.[A-Za-z0-9_-]{4,})",
        output_content))

    feedback = []
    if is_junk:
        feedback.append("⚠️ [质量警告] 内容疑似低危垃圾洞，请重新评估影响等级。")
    if may_contain_secret:
        feedback.append("⚠️ [数据保护] 工具输出疑似包含认证信息；后续引用或落盘前必须脱敏。")
    
    if feedback:
        # 将验证结果反馈给 AI，让它自我修正或确认
        print(json.dumps({
            "message": "\n".join(feedback)
        }))

if __name__ == "__main__":
    main()
