# IAM Security Automation Lab

## Overview
This project demonstrates a realistic Identity and Access Management (IAM) and authentication security automation using Bash and Python on Red Hat Enterprise Linux.

The automation collects identity, access, and authentication evidence from a Linux system, analyzes authentication failures, and produces a single consolidated security report suitable for audit, review, or incident triage.

This mirrors the type of work performed by Security Consultants and Security Analysts in enterprise environments.

---

## What This Automation Does

The project performs the following security checks:

- Collects host identity information (hostname, OS, IP addresses)
- Verifies identity-critical services (SSHD and firewall status)
- Audits privileged access (UID 0 accounts and sudo configuration)
- Extracts failed authentication events from system logs
- Analyzes authentication failures using Python
- Assigns a simple risk level (low / medium / high)
- Produces a single, readable security report

---

## Tools Used

- Red Hat Enterprise Linux 10
- Bash (automation and evidence collection)
- Python 3 (log analysis and summarization)
- Git and GitHub (version control and documentation)

---

## Project Structure

iam-automation-lab/
├── scripts/
│ ├── iam_security_collector.sh
│ └── auth_log_analyzer.py
├── reports/
│ └── final_report.txt
└── README.md

---

## How to Run the Automation

1. Run the IAM security collector script:
./scripts/iam_security_collector.sh


2. Analyze authentication failures:
python3 scripts/auth_log_analyzer.py


3. Review the final report:
less reports/final_report.txt

---

## Why This Matters

Security teams must continuously validate:
- Who has access
- Who has administrative privileges
- Whether authentication failures indicate risk
- Whether systems are configured securely

This automation turns those repeatable checks into reliable, documented evidence that can be reviewed by engineers, managers, or auditors.

---

## Interview Summary

This project demonstrates:
- Linux IAM and authentication auditing
- Bash automation with fail-safe design
- Python-based log analysis
- Evidence-driven security reporting
- Professional version control practices

