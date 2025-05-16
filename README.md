# IPv6 地址自动管理脚本

![Linux](https://img.shields.io/badge/平台-Linux-blue)
![Python](https://img.shields.io/badge/Python-3.6%2B-green)
![License](https://img.shields.io/badge/许可证-MIT-orange)

一个用于 Linux 系统的自动化 IPv6 地址管理工具，支持批量生成、添加、删除 IPv6 地址，并提供持久化存储功能。适用于物理机、虚拟机、Docker/LXC 容器等环境。


## 功能特性

### 核心功能

-  **自动检测网卡**：支持 `eth0@if2` 格式的复杂网卡名称
-  **精准过滤**：自动排除本地回环 (`::1`)、链路本地 (`fe80::`) 地址及虚拟接口（`lo`, `tun*`, `docker0`）
-  **地址生成**：基于主地址随机生成同子网段的新 IPv6 地址
-  **批量操作**：支持从 `ipv6.txt` 文件批量添加地址
-  **智能清理**：一键删除非主地址，保留原始配置
-  **持久化存储**：自动保存生成的地址到 `ipv6.txt`

### 高级支持

- ✅ 全自动操作流程，无需手动配置
- ✅ 内置地址冲突检测机制
- ✅ 兼容 Docker/LXC 容器网络环境
- ✅ 支持大规模 IPv6 地址自动化运维

---

## 环境要求

- **操作系统**: Linux（推荐 Ubuntu/CentOS）
- **依赖工具**:
  - `iproute2` 工具包（提供 `ip` 命令）
  - Python 3.6 或更高版本
- **权限要求**: Root 权限

---

## 快速开始

### 1. 下载脚本

```bash
wget https://raw.githubusercontent.com/help660vip/auto-add-ipv6/main/v2.py -O ipv6-manager.py
chmod +x ipv6-manager.py
```

### 2. 安装依赖（Debian/Ubuntu）

```
sudo apt update && sudo apt install -y iproute2 python3
```

### 3. 运行脚本

```
sudo python3 ipv6-manager.py
```

## 详细使用指南

### 主菜单选项

```
1. 自动生成并添加新 IPv6 地址
2. 从 ipv6.txt 批量添加地址
3. 删除手动添加的 IPv6
4. 清空 ipv6.txt 记录
0. 退出
```

### 功能说明

1. **生成新地址**
   * 输入需要生成的地址数量（例如 10）
   * 脚本将自动为每个检测到的网卡生成指定数量的新地址
   * 新地址会自动保存到 `ipv6.txt`
2. **批量添加地址**
   * 预先在 `ipv6.txt` 中按行填写需要添加的 IPv6 地址
   * 选择此选项后脚本会自动验证并添加所有合法地址
3. **清理地址**
   * 保留每个网卡的第一个全局 IPv6 地址
   * 删除所有手动添加的附加地址
4. **清空记录**
   * 清空 `ipv6.txt` 文件内容（不影响已添加的地址）

---

## 示例输出


```
🌐 检测到网卡: eth0@if2，主地址: 2001:db8:abcd:1234::1/64
✅ 已添加地址: 2001:db8:abcd:1234::a9b1/64 ➤ eth0@if2
✅ 已添加地址: 2001:db8:abcd:1234::c6d3/64 ➤ eth0@if2
✅ 已添加地址: 2001:db8:abcd:1234::d2ef/64 ➤ eth0@if2
```

---

## 结果验证

执行以下命令查看已添加的 IPv6 地址：

```
ip -6 addr show | grep 'scope global'
```

---

## 适用场景

* 🖥️ 云服务器批量配置 IPv6 地址
* 🐳 Docker/LXC 容器网络管理
* 🔬 大规模 IPv6 网络压力测试
* 🛠️ 自动化运维工具链集成

---

## 注意事项

⚠️ ​**重要提示**​：

1. 必须使用 **root 权限** 运行脚本
2. 建议先在测试环境验证操作
3. 定期备份 `ipv6.txt` 文件
4. 清理操作不可逆，请确认保留的主地址正确
5. 不支持 Windows/macOS 系统

---

## 支持与贡献

* [提交问题报告](https://github.com/help660vip/auto-add-ipv6/issues)
* [功能建议](https://github.com/help660vip/auto-add-ipv6/discussions)
* ✨ 欢迎提交 Pull Request 改进项目

---

## 许可证

MIT License © 2025 help660vip
