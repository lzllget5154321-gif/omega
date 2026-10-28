#!/bin/bash
# Omega Sandbox Network Filter
# ============================
# 在 omega-sandbox-net 容器启动时设置 iptables 规则。
# 仅允许访问：PyPI、npm registry、GitHub、docs.python.org、readthedocs.io
# 阻止所有其他网络访问。
#
# 此脚本以 root 运行，需要 NET_ADMIN capability。

set -e

ALLOWED_DOMAINS="${ALLOWED_DOMAINS:-pypi.org files.pythonhosted.org registry.npmjs.org github.com raw.githubusercontent.com docs.python.org readthedocs.io}"

echo "[sandbox-net-filter] Setting up limited network access..."

# 清空已有规则
iptables -F OUTPUT 2>/dev/null || true

# 允许本地回环（容器内通信）
iptables -A OUTPUT -o lo -j ACCEPT

# 允许 DNS 查询
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

# 允许已建立和相关的连接
iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 逐个域名 DNS 解析并添加规则
for domain in $ALLOWED_DOMAINS; do
    # 尝试解析域名
    ips=$(dig +short "$domain" 2>/dev/null || echo "")
    if [ -n "$ips" ]; then
        for ip in $ips; do
            iptables -A OUTPUT -p tcp -d "$ip" --dport 443 -j ACCEPT
            iptables -A OUTPUT -p tcp -d "$ip" --dport 80 -j ACCEPT
        done
        echo "  [ALLOW] $domain"
    else
        echo "  [WARN] Cannot resolve $domain — skipping iptables rule"
    fi
done

# 默认拒绝所有其他出站流量
iptables -A OUTPUT -j REJECT --reject-with icmp-admin-prohibited

echo "[sandbox-net-filter] Network filtering active. Allowed domains: $ALLOWED_DOMAINS"
