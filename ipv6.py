import subprocess
import re
import random

def get_interfaces_with_ipv6():
    """ 获取所有有 IPv6 地址的网卡，排除 ::1/128 和 fe80::，并去掉 @ifX 形式 """
    result = subprocess.run(["ip", "-6", "addr", "show"], capture_output=True, text=True)
    interface_pattern = re.compile(r"\d+: (\S+):")  # 匹配网卡名
    ipv6_pattern = re.compile(r"inet6 ([\da-fA-F:]+)/(\d+)")

    interfaces = {}
    current_interface = None

    for line in result.stdout.splitlines():
        match_iface = interface_pattern.match(line)
        if match_iface:
            current_interface = match_iface.group(1).split("@")[0]  # 去掉 @ifX
        match_ipv6 = ipv6_pattern.search(line)
        if match_ipv6 and current_interface:
            ipv6_address, prefix = match_ipv6.groups()
            if ipv6_address != "::1" and not ipv6_address.startswith("fe80"):  # 排除 ::1 和 fe80::
                interfaces[current_interface] = (ipv6_address, int(prefix))

    return interfaces

def generate_new_ipv6(same_prefix_ipv6):
    """ 生成新的同网段 IPv6 地址 """
    parts = same_prefix_ipv6.split(":")
    # 仅修改最后 4 组，保持前缀不变
    for i in range(4, 8):
        parts[i] = format(random.randint(0, 0xFFFF), "x")
    return ":".join(parts)

def add_ipv6_address(interface, new_ipv6, prefix_len):
    """ 添加新的 IPv6 地址到网卡 """
    cmd = ["sudo", "ip", "-6", "addr", "add", f"{new_ipv6}/{prefix_len}", "dev", interface]
    subprocess.run(cmd, check=True)
    print(f"✅ 已添加 IPv6 地址: {new_ipv6}/{prefix_len} 到网卡 {interface}")

if __name__ == "__main__":
    interfaces = get_interfaces_with_ipv6()

    if not interfaces:
        print("❌ 没有找到可用的 IPv6 地址")
    else:
        num_addresses = int(input("请输入要生成的 IPv6 地址数量: "))
        for interface, (ipv6, prefix) in interfaces.items():
            print(f"🌐 检测到网卡: {interface}，IPv6: {ipv6}/{prefix}")
            for _ in range(num_addresses):
                new_ipv6 = generate_new_ipv6(ipv6)
                add_ipv6_address(interface, new_ipv6, prefix)
