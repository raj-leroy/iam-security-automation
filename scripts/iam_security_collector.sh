#!/bin/bash
set -euo pipefail
OUTDIR="reports"
TS="$(date +%Y%m%d_%H%M%S)"
HOSTFILE="$OUTDIR/host_identity_$TS.txt"

mkdir -p "$OUTDIR"

{
  echo "HOST IDENTITY EVIDENCE"
  echo "Timestamp: $TS"
  echo
  echo "Hostname:"
  hostname
  echo
  echo "OS Release:"
  cat /etc/redhat-release
  echo
  echo "IP Addresses:"
  ip a
} > "$HOSTFILE"
SERVICEFILE="$OUTDIR/service_status_$TS.txt"

{
  echo "IDENTITY-CRITICAL SERVICE STATUS"
  echo "Timestamp: $TS"
  echo
  echo "SSHD Status:"
  systemctl status sshd --no-pager
  echo
  echo "Firewall Status:"
  systemctl status firewalld --no-pager
} > "$SERVICEFILE"
PRIVFILE="$OUTDIR/privileged_access_$TS.txt"

{
  echo "PRIVILEGED ACCESS AUDIT"
  echo "Timestamp: $TS"
  echo
  echo "UID 0 accounts (should normally be only root):"
  awk -F: '($3 == 0) {print $1 ":" $3 ":" $7}' /etc/passwd
  echo
  echo "Sudo configuration (who can use sudo):"
  sudo cat /etc/sudoers
  echo
  echo "Sudo drop-in files (extra sudo rules):"
  sudo ls -la /etc/sudoers.d
} > "$PRIVFILE"
AUTHFILE="$OUTDIR/auth_failures_raw_$TS.txt"

{
  echo "AUTHENTICATION FAILURE EVIDENCE (RAW)"
  echo "Timestamp: $TS"
  echo
  echo "Source log: /var/log/secure"
  echo
  echo "Failed authentication lines:"
  sudo grep -E "Failed password|authentication failure|Invalid user" /var/log/secure || true
} > "$AUTHFILE"
