#!/usr/bin/env python3

from pathlib import Path
import re
from collections import Counter

REPORTS_DIR = Path("reports")

def newest_auth_failure_file():
    files = sorted(REPORTS_DIR.glob("auth_failures_raw_*.txt"))
    if not files:
        raise SystemExit("No auth_failures_raw_*.txt files found in reports/")
    return files[-1]

def main():
    raw_file = newest_auth_failure_file()
    lines = raw_file.read_text(errors="ignore").splitlines()

    failure_lines = [
        ln for ln in lines
        if ln.strip()
        and not ln.startswith("AUTHENTICATION")
        and not ln.startswith("Timestamp")
        and not ln.startswith("Source log")
        and not ln.startswith("Failed authentication")
    ]

    total_failures = len(failure_lines)

    # Simple risk rules based on total failures
    if total_failures == 0:
        risk = "low"
    elif total_failures <= 5:
        risk = "low"
    elif total_failures <= 25:
        risk = "medium"
    else:
        risk = "high"

    ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

    user_counter = Counter()
    ip_counter = Counter()

    for ln in failure_lines:
        ip_match = ip_pattern.search(ln)
        if ip_match:
            ip_counter[ip_match.group()] += 1

        if "Invalid user" in ln:
            parts = ln.split("Invalid user", 1)[1].strip().split()
            if parts:
                user_counter[parts[0]] += 1

        elif "Failed password for" in ln:
            parts = ln.split("Failed password for", 1)[1].strip().split()
            if parts:
                if parts[0] == "invalid" and len(parts) >= 3 and parts[1] == "user":
                    user_counter[parts[2]] += 1
                else:
                    user_counter[parts[0]] += 1

        elif "authentication failure" in ln and "user=" in ln:
            after = ln.split("user=", 1)[1]
            uname = after.split()[0].strip()
            if uname:
                user_counter[uname] += 1

    print(f"Analyzing file: {raw_file.name}")
    print(f"Total failed authentication events: {total_failures}")
    print(f"Risk level: {risk}")

    print("Top usernames (failures):")
    for user, count in user_counter.most_common(5):
        print(f"  {user}: {count}")

    print("Top source IPs (failures):")
    for ip, count in ip_counter.most_common(5):
        print(f"  {ip}: {count}")

if __name__ == "__main__":
    main()

