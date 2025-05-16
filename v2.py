#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import re
import random
import shutil
import os
import platform
import ipaddress
import sys

IPV6_FILE = "ipv6.txt"

def check_dependencies():
    if platform.system() != "Linux":
        print("❌ 此脚本仅支持 Linux 系统。")
        sys.exit(1)
    if not shutil.which("ip"):
        print("❌ 未找到 'ip' 命令，请先安装 iproute2。")
        sys.exit(1)
    if os.geteuid() != 0:
        print("❌ 请以 root 权限运行此脚本（使用 sudo）。")
        sys.exit(1)

def get_interfaces_with_ipv6():
    """
    获取所有有 IPv6 地址的物理/虚拟网卡，排除 lo、fe80::、::1、tun*、docker0
    返回：{ interface_name: (primary_ipv6, prefix) }
    """
    out = subprocess.run(["ip", "-6", "addr", "show"], capture_output=True, text=True).stdout
    iface_re = re.compile(r"\d+: (\S+):")
    addr_re  = re.compile(r"inet6 ([0-9a-fA-F:]+)/(\d+)\s+scope global")
    result = {}
    current = None

    for line in out.splitlines():
        m = iface_re.match(line)
        if m:
            name = m.group(1).split("@")[0]
            # 排除回环和常见虚拟接口
            if name == "lo" or name.startswith("tun") or name == "docker0":
                current = None
            else:
                current = name
        elif current:
            m2 = addr_re.search(line)
            if m2:
                ipv6, p = m2.groups()
                # 只取第一个全局地址作为主地址
                if current not in result:
                    result[current] = (ipv6, int(p))
    return result

def expand_ipv6(ipv6):
    """把任意形式的 IPv6 地址展开为 8 段列表"""
    return ipaddress.IPv6Address(ipv6).exploded.split(":")

def generate_new_ipv6(base_ipv6):
    """
    基于 base_ipv6，同段随机生成新的 IPv6。
    保持前半段（前 4 段）不变，后 4 段随机。
    """
    parts = expand_ipv6(base_ipv6)
    for i in range(4, 8):
        parts[i] = format(random.randint(0, 0xFFFF), "x").zfill(4)
    return ":".join(parts)

def is_ipv6_in_use(ipv6):
    out = subprocess.run(["ip", "-6", "addr", "show"], capture_output=True, text=True).stdout.lower()
    return ipv6.lower() in out

def add_ipv6_address(iface, ipv6, prefix):
    if is_ipv6_in_use(ipv6):
        print(f"⚠️  {ipv6}/{prefix} 已存在，跳过")
        return False
    cmd = ["ip", "-6", "addr", "add", f"{ipv6}/{prefix}", "dev", iface]
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ 添加 {ipv6}/{prefix} ➤ {iface}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 添加失败: {e}")
        return False

def delete_ipv6_address(iface, ipv6, prefix):
    cmd = ["ip", "-6", "addr", "del", f"{ipv6}/{prefix}", "dev", iface]
    try:
        subprocess.run(cmd, check=True)
        print(f"🗑️ 删除 {ipv6}/{prefix} ◁ {iface}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 删除失败: {e}")

def save_to_file(addresses):
    """将纯 IPv6 地址列表写入 ipv6.txt"""
    with open(IPV6_FILE, "w") as f:
        for ip in addresses:
            f.write(ip + "\n")
    print(f"💾 保存到 {IPV6_FILE}")

def load_from_file():
    """读取 ipv6.txt 并返回纯地址列表"""
    if not os.path.exists(IPV6_FILE):
        print(f"⚠️ {IPV6_FILE} 不存在")
        return []
    with open(IPV6_FILE) as f:
        return [line.strip() for line in f if line.strip()]

def list_interface_ipv6(iface):
    """
    列出指定接口的所有全局 IPv6 地址及前缀，返回列表 [(ipv6, prefix), ...]
    """
    out = subprocess.run(["ip", "-6", "addr", "show", "dev", iface], capture_output=True, text=True).stdout
    addr_re = re.compile(r"inet6 ([0-9a-fA-F:]+)/(\d+)\s+scope global")
    addrs = []
    for line in out.splitlines():
        m = addr_re.search(line)
        if m:
            ipv6, p = m.groups()
            # 排除回环和链路本地
            if ipv6 != "::1" and not ipv6.startswith("fe80"):
                addrs.append((ipv6, int(p)))
    return addrs

def main():
    check_dependencies()
    ifaces = get_interfaces_with_ipv6()
    if not ifaces:
        print("❌ 未检测到可用网卡与 IPv6")
        sys.exit(1)

    print("\n🚀 IPv6 自动管理脚本")
    print("📌 https://github.com/help660vip/auto-add-ipv6\n")
    print("请选择：")
    print("1. 自动生成并添加新 IPv6")
    print("2. 从 ipv6.txt 添加 IPv6")
    print("3. 删除手动添加的 IPv6")
    print("4. 清空 ipv6.txt")
    print("0. 退出")
    choice = input("输入(0-4)：").strip()

    if choice == "1":
        n = input("生成地址数量：").strip()
        if not n.isdigit():
            print("❌ 数字格式错误")
            sys.exit(1)
        n = int(n)
        added = []
        for iface,(base, pfx) in ifaces.items():
            print(f"🌐 {iface} 主地址: {base}/{pfx}")
            for _ in range(n):
                new = generate_new_ipv6(base)
                if add_ipv6_address(iface, new, pfx):
                    added.append(new)
        if added:
            save_to_file(added)
        sys.exit(0)

    elif choice == "2":
        addrs = load_from_file()
        if not addrs:
            sys.exit(1)
        for iface,(base,pfx) in ifaces.items():
            print(f"🌐 {iface} 主段: {base}/{pfx}")
            net = ipaddress.IPv6Network(f"{base}/{pfx}", strict=False)
            for ip in addrs:
                try:
                    ipaddr = ipaddress.IPv6Address(ip)
                except ipaddress.AddressValueError:
                    print(f"⚠️ 格式非法：{ip}")
                    continue
                if ipaddr not in net:
                    yn = input(f"{ip} 不在同段，继续? (yes/其他=跳过) ")
                    if yn != "yes":
                        continue
                add_ipv6_address(iface, ip, pfx)
        sys.exit(0)

    elif choice == "3":
        for iface in ifaces:
            addrs = list_interface_ipv6(iface)
            if not addrs:
                continue
            # 保留第一个，删除剩余
            primary = addrs[0]
            print(f"🌐 {iface} 保留: {primary[0]}/{primary[1]}")
            for ipv6, pfx in addrs[1:]:
                delete_ipv6_address(iface, ipv6, pfx)
        sys.exit(0)

    elif choice == "4":
        open(IPV6_FILE,"w").close()
        print(f"🗑️ 已清空 {IPV6_FILE}")
        sys.exit(0)

    elif choice == "0":
        sys.exit(0)

    else:
        print("❌ 无效选项，退出")
        sys.exit(1)

if __name__ == "__main__":
    main()
