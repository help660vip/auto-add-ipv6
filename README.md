# 自动获取并添加 IPv6 地址脚本

## 介绍
这是一个 Python 脚本，它可以自动检测系统中所有具有 IPv6 地址的网卡，并根据已有的 IPv6 地址自动生成新的同网段 IPv6 地址，然后添加到网卡中。

该脚本适用于 **物理机、虚拟机、Docker 容器、LXC 容器** 等环境，并能正确处理 `eth0@if2` 这种带 `@` 的网卡名称。

## 功能特点
✅ **自动获取网卡名称**（支持 `eth0@if2` 格式）  
✅ **自动获取 IPv6 地址和子网掩码**  
✅ **排除 `::1/128`（本地回环地址）和 `fe80::`（链路本地地址）**  
✅ **支持用户输入需要生成的 IPv6 地址数量**  
✅ **自动生成多个新的同网段 IPv6 地址**  
✅ **自动添加 IPv6 地址到对应网卡**  

## 依赖环境
本脚本基于 Python 3，并依赖 `ip` 命令（通常由 `iproute2` 提供）。请确保系统已安装这些组件。

### **安装 Python 3**
如果你的系统没有 Python 3，可以使用以下命令安装（以 Debian/Ubuntu 为例）：
```sh
sudo apt update && sudo apt install -y python3
```

## 使用方法
### 1. 下载脚本
```sh
git clone https://github.com/help660vip/auto-add-ipv6.git
cd auto-add-ipv6
```

### 2. 运行脚本
```sh
sudo python3 ipv6.py
```

### 3. 输入要生成的 IPv6 地址数量
```sh
请输入要生成的 IPv6 地址数量: 5
```

### 4. 运行示例输出
```sh
🌐 检测到网卡: eth0，IPv6: 2001:db8:abcd:1234::1/64
✅ 已添加 IPv6 地址: 2001:db8:abcd:1234::a9b1/64 到网卡 eth0
✅ 已添加 IPv6 地址: 2001:db8:abcd:1234::c6d3/64 到网卡 eth0
✅ 已添加 IPv6 地址: 2001:db8:abcd:1234::d2ef/64 到网卡 eth0
✅ 已添加 IPv6 地址: 2001:db8:abcd:1234::e7f5/64 到网卡 eth0
✅ 已添加 IPv6 地址: 2001:db8:abcd:1234::f8c2/64 到网卡 eth0
```

## 结果验证
执行以下命令，查看是否成功添加了 IPv6 地址：
```sh
ip -6 addr show
```

## 适用场景
- **服务器自动批量分配 IPv6**
- **Docker / LXC 容器 IPv6 地址管理**
- **大规模 IPv6 网络测试**
- **IPv6 地址自动化运维**

## 贡献
欢迎提交 Issue 和 Pull Request 进行改进！

## 许可证
MIT License

