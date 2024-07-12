在 Ubuntu 中，可以通过几种方式设置 IP 地址：使用网络管理器图形界面、命令行工具（如 `nmcli` 或 `nmtui`）、或直接编辑网络配置文件。以下是这几种方法的详细步骤。

### 方法一：使用图形界面（Network Manager）

1. **打开网络设置**：
   - 点击屏幕右上角的网络图标。
   - 选择“设置”或“网络设置”。

2. **选择网络连接**：
   - 在左侧面板中选择要配置的网络连接（例如，有线网络或无线网络）。
   - 点击齿轮图标以打开该连接的设置。

3. **配置 IPv4 设置**：
   - 选择“IPv4”标签。
   - 在“方法”下拉菜单中选择“手动”。
   - 输入所需的 IP 地址、子网掩码和网关。
   - 在 DNS 设置中输入 DNS 服务器地址（如果需要）。

4. **保存更改**：
   - 点击“应用”按钮以保存更改。

### 方法二：使用 `nmcli` 命令行工具

1. **列出所有连接**：
   ```bash
   nmcli connection show
   ```

2. **修改连接的 IP 地址**：
   假设要修改的连接名是 `Wired connection 1`，并将 IP 地址设置为 `192.168.1.100`，子网掩码为 `24`，网关为 `192.168.1.1`：
   ```bash
   nmcli connection modify "Wired connection 1" ipv4.addresses 192.168.1.100/24
   nmcli connection modify "Wired connection 1" ipv4.gateway 192.168.1.1
   nmcli connection modify "Wired connection 1" ipv4.method manual
   nmcli connection up "Wired connection 1"
   ```

3. **设置 DNS 服务器**：
   ```bash
   nmcli connection modify "Wired connection 1" ipv4.dns "8.8.8.8 8.8.4.4"
   ```

### 方法三：使用 `nmtui` 命令行工具

1. **启动 `nmtui` 工具**：
   ```bash
   nmtui
   ```

2. **选择“编辑连接”**。

3. **选择要编辑的连接**并按回车键。

4. **配置 IPv4 设置**：
   - 将“方法”设置为“手动”。
   - 输入 IP 地址、子网掩码和网关。
   - 输入 DNS 服务器地址。

5. **保存更改**并退出。

### 方法四：手动编辑网络配置文件（Netplan）

对于 Ubuntu 18.04 及更高版本，可以使用 Netplan 来配置网络：

1. **打开 Netplan 配置文件**：
   ```bash
   sudo nano /etc/netplan/01-netcfg.yaml
   ```

2. **编辑文件以设置静态 IP**：
   假设你的网络接口名是 `eth0`，配置如下：
   ```yaml
   network:
     version: 2
     ethernets:
       eth0:
         dhcp4: no
         addresses: [192.168.1.100/24]
         gateway4: 192.168.1.1
         nameservers:
           addresses: [8.8.8.8, 8.8.4.4]
   ```

3. **应用配置**：
   ```bash
   sudo netplan apply
   ```

选择适合你的方法来设置 IP 地址。如果不确定，可以从图形界面或 `nmtui` 工具开始，这些方法相对更为直观。