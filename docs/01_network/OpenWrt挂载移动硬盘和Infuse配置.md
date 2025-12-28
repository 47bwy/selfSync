# OpenWrt 挂载移动硬盘并通过 Infuse 访问指南

## 概述
本指南将帮助你在友善 R2S 路由器上配置 OpenWrt，挂载移动硬盘，并通过 Apple TV 的 Infuse 应用访问其中的电影文件。

## 前置准备

1. **硬件要求**
   - 友善 R2S 路由器（已安装 OpenWrt）
   - USB 移动硬盘（建议格式化为 ext4 或 NTFS）
   - Apple TV（已安装 Infuse 应用）

2. **软件要求**
   - OpenWrt 系统（建议使用较新版本）
   - SSH 访问权限

## 步骤一：安装必要的软件包

通过 SSH 登录到 OpenWrt 路由器，安装以下软件包：

```bash
# 更新软件包列表
opkg update

# 安装 USB 支持
opkg install kmod-usb-storage kmod-usb2 kmod-usb3
opkg install usbutils

# 安装文件系统支持（根据你的硬盘格式选择）
# 对于 ext4 格式（推荐，性能最好）
opkg install kmod-fs-ext4 e2fsprogs

# 对于 exFAT 格式（推荐，跨平台兼容，支持大文件）
opkg install kmod-fs-exfat exfat-fsck exfat-mkfs

# 对于 NTFS 格式
opkg install kmod-fs-ntfs ntfs-3g

# 安装自动挂载工具
opkg install block-mount

# 安装 Samba（SMB/CIFS 共享，Infuse 支持）
opkg install samba4-server luci-app-samba4

# 或者安装 NFS（可选，性能更好但配置稍复杂）
# opkg install nfs-kernel-server luci-app-nfs
```

## 步骤二：检查 USB 设备识别情况

### 检查设备是否被识别

即使 `fdisk -l` 不显示，设备可能已经被识别。使用以下命令检查：

```bash
# 方法 1：查看 USB 设备列表
lsusb

# 方法 2：查看块设备（包括未挂载的）
lsblk

# 方法 3：查看系统消息（插入硬盘后立即执行）
dmesg | tail -50

# 方法 4：查看 /dev 目录下的设备
ls -la /dev/sd*

# 方法 5：查看内核消息
dmesg | grep -i "usb\|sd"
```

### 苹果文件系统问题说明（APFS / HFS+）

**重要**：如果你的硬盘是 **APFS（Apple File System）** 或 **HFS+（Mac OS Extended）** 格式，OpenWrt 对它们的支持非常有限：

1. **APFS**：OpenWrt **完全不支持**，无法挂载
2. **HFS+**：OpenWrt 有部分支持，但：
   - 通常只能**只读**访问
   - 写入支持不稳定，可能导致数据损坏
   - 需要安装额外的内核模块
   - 性能较差，不适合作为媒体服务器

**查看你的硬盘格式**：
```bash
fdisk -l
# 如果显示 "Apple HFS/HFS+" 或 "Apple APFS"，就是苹果文件系统
```

**示例输出**（HFS+ 格式）：
```
Device      Start        End    Sectors  Size Type
/dev/sda1      40     409639     409600  200M EFI System
/dev/sda2  409640 3906701271 3906291632  1.8T Apple HFS/HFS+
```

### 解决方案

#### 方案零：尝试挂载 HFS+（仅限 HFS+，不推荐，仅测试用）

如果你的硬盘是 **HFS+** 格式，可以尝试只读挂载（**不推荐用于生产环境**）：

```bash
# 安装 HFS+ 支持（只读）
opkg install kmod-fs-hfsplus

# 尝试只读挂载（注意：是 /dev/sda2，不是 /dev/sda1）
mkdir -p /mnt/usb
mount -t hfsplus -o ro /dev/sda2 /mnt/usb

# 检查是否成功
df -h
ls /mnt/usb
```

**⚠️ 警告**：
- HFS+ 支持不稳定，可能导致数据损坏
- 通常只能只读，无法写入
- 性能较差
- **强烈建议重新格式化**

#### 方案一：重新格式化为 OpenWrt 支持的文件系统（强烈推荐）

**⚠️ 警告：格式化会删除所有数据，请先备份！**

在 Mac 上备份数据后，重新格式化：

1. **在 Mac 上格式化**：
   - 打开"磁盘工具"
   - 选择移动硬盘
   - 点击"抹掉"
   - 选择格式：
     - **exFAT**：Mac 和 Windows 都能读写，OpenWrt 也支持（推荐）
     - **NTFS**：跨平台兼容
     - **MS-DOS (FAT32)**：兼容性最好，但单文件不能超过 4GB

2. **或者使用命令行**（在 Mac 上）：
   ```bash
   # 查看磁盘
   diskutil list
   
   # 格式化为 exFAT（推荐，支持大文件）
   diskutil eraseDisk exFAT "Movies" /dev/disk2
   
   # 或格式化为 MS-DOS (FAT32)
   diskutil eraseDisk MS-DOS "Movies" /dev/disk2
   ```

3. **然后在 OpenWrt 上安装对应支持**：
   ```bash
   # 对于 exFAT
   opkg install kmod-fs-exfat exfat-fsck exfat-mkfs
   
   # 对于 NTFS（如果选择 NTFS）
   opkg install kmod-fs-ntfs ntfs-3g
   ```

#### 方案二：在 OpenWrt 上格式化（如果设备能被识别）

如果 `fdisk -l` 能显示设备（如 `/dev/sda`），可以在 OpenWrt 上直接格式化：

```bash
# 首先确认设备（非常重要！不要选错）
fdisk -l
lsblk

# 假设设备是 /dev/sda，先卸载所有分区（如果已挂载）
umount /dev/sda1 2>/dev/null
umount /dev/sda2 2>/dev/null

# 删除所有分区并创建新分区表（会删除所有数据）
fdisk /dev/sda
# 在 fdisk 中：
# 输入 'g' 创建新的 GPT 分区表（或 'o' 创建 DOS 分区表）
# 输入 'n' 创建新分区
# 输入 'p' 主分区（如果是 DOS 分区表）
# 按回车使用默认起始扇区
# 按回车使用默认结束扇区（使用整个磁盘）
# 输入 'w' 保存并退出

# 格式化为 ext4（推荐，性能最好）
opkg install kmod-fs-ext4 e2fsprogs
mkfs.ext4 /dev/sda1

# 或格式化为 exFAT（推荐，跨平台兼容，支持大文件）
opkg install kmod-fs-exfat exfat-fsck exfat-mkfs
mkfs.exfat /dev/sda1

# 或格式化为 NTFS
opkg install kmod-fs-ntfs ntfs-3g
mkfs.ntfs /dev/sda1
```

**注意**：如果你的硬盘有多个分区（如 EFI 分区 + 数据分区），格式化会删除所有分区。建议在 Mac 上使用磁盘工具格式化更安全。

#### 方案三：使用网络共享（临时方案，不推荐）

如果数据不能丢失且暂时无法格式化，可以考虑：

1. 将硬盘连接到 Mac
2. 在 Mac 上启用文件共享
3. Infuse 直接连接 Mac 的共享

这不是长期解决方案，因为需要 Mac 一直开机。

## 步骤三：格式化移动硬盘（如果需要）

如果你的硬盘已经被识别且格式正确，可以跳过此步骤。如果需要格式化：

```bash
# 查看连接的 USB 设备
lsblk
# 或
fdisk -l

# 找到你的移动硬盘设备（通常是 /dev/sda1 或 /dev/sdb1）
# 注意：格式化会删除所有数据，请先备份！

# 格式化为 ext4（推荐，性能最好）
mkfs.ext4 /dev/sda1

# 或格式化为 exFAT（跨平台兼容，支持大文件）
mkfs.exfat /dev/sda1

# 或格式化为 NTFS（跨平台兼容）
mkfs.ntfs /dev/sda1
```

## 步骤四：手动挂载测试

在配置自动挂载之前，先手动挂载测试：

```bash
# 创建挂载点
mkdir -p /mnt/usb

# 挂载硬盘（ext4）
mount -t ext4 /dev/sda1 /mnt/usb

# 或挂载硬盘（exFAT）
mount -t exfat /dev/sda1 /mnt/usb

# 或挂载硬盘（NTFS）
mount -t ntfs-3g /dev/sda1 /mnt/usb

# 如果是 HFS+ 格式（不推荐，仅测试）
# mount -t hfsplus -o ro /dev/sda2 /mnt/usb  # 注意：可能是 sda2 而不是 sda1

# 检查挂载是否成功
df -h
ls /mnt/usb

# 如果成功，创建测试文件
echo "test" > /mnt/usb/test.txt
cat /mnt/usb/test.txt

# 卸载测试
umount /mnt/usb
```

## 步骤五：配置自动挂载

### 方法一：使用 Web 界面（推荐）

1. 登录 OpenWrt Web 管理界面（通常是 `http://192.168.1.1`）
2. 进入 **系统** → **挂载点**
3. 在 **挂载点** 部分，点击 **添加**
4. 配置如下：
   - **设备**：选择你的 USB 硬盘（如 `/dev/sda1`）
   - **挂载点**：`/mnt/usb` 或 `/mnt/sda1`
   - **文件系统**：选择对应的文件系统类型
   - **选项**：可以留空或添加 `rw,noatime`（读写，不更新访问时间）
5. 勾选 **启用此挂载点**
6. 点击 **保存并应用**

### 方法二：使用命令行

编辑 `/etc/config/fstab` 文件：

```bash
vi /etc/config/fstab
```

添加以下内容：

```
config mount
    option device '/dev/sda1'
    option target '/mnt/usb'
    option fstype 'ext4'
    option options 'rw,noatime'
    option enabled '1'
```

保存后应用配置：

```bash
/etc/init.d/fstab enable
/etc/init.d/fstab restart
```

## 步骤六：配置 Samba 共享（命令行方式）

本配置使用**访客访问**方式，无需输入用户名密码，连接方便，适合家庭内网使用。配置完成后，可以从 Mac 或其他设备向共享目录中拷贝电影文件。

### 第一步：编辑 Samba 配置文件

```bash
vi /etc/config/samba4
```

如果文件不存在或为空，添加以下完整配置：

```
config samba
    option name 'OpenWrt'
    option workgroup 'WORKGROUP'
    option description 'OpenWrt NAS'
    option charset 'UTF-8'
    option homes '0'
    option interface 'lan'

config sambashare
    option name 'Media'
    option path '/mnt/usb'
    option read_only 'no'
    option guest_ok 'yes'
    option create_mask '0666'
    option dir_mask '0777'
    option force_user 'root'
    option force_group 'root'
    option browseable 'yes'
```

**关键配置说明**（确保写入权限）：
- `read_only 'no'`：**必须**设置为 'no'，允许写入
- `guest_ok 'yes'`：允许访客（匿名）访问，无需密码
- `force_user 'root'`：**重要**，强制使用 root 用户，确保有写入权限
- `force_group 'root'`：强制使用 root 组
- `create_mask '0666'`：新创建的文件权限（所有用户可读写）
- `dir_mask '0777'`：新创建的目录权限（所有用户可读写执行）
- `browseable 'yes'`：在网络上可见

保存文件（vi 中按 `Esc`，然后输入 `:wq` 回车）。

### 第二步：设置目录权限

```bash
# 设置挂载点目录权限为 777（所有用户可读写执行）
chmod 777 /mnt/usb

# 如果目录中已有文件，递归设置所有文件和目录权限
chmod -R 777 /mnt/usb
```

### 第三步：启动并启用 Samba 服务

```bash
# 启用 Samba 服务（开机自启）
/etc/init.d/samba4 enable

# 启动 Samba 服务
/etc/init.d/samba4 start

# 检查服务状态
/etc/init.d/samba4 status
```

### 第四步：验证配置

```bash
# 1. 查看 UCI 配置
uci show samba4.@sambashare[0]

# 应该看到：
# samba4.@sambashare[0].name='Media'
# samba4.@sambashare[0].path='/mnt/usb'
# samba4.@sambashare[0].read_only='no'
# samba4.@sambashare[0].guest_ok='yes'
# samba4.@sambashare[0].force_user='root'
# samba4.@sambashare[0].force_group='root'

# 2. 查看实际生成的 Samba 配置文件
cat /etc/samba/smb.conf | grep -A 15 "\[Media\]"

# 应该看到：
# [movies]
#    path = /mnt/usb
#    valid users = 
#    read only = No
#    guest ok = Yes
#    force user = root
#    force group = root
#    create mask = 0666
#    directory mask = 0777

# 3. 检查目录权限
ls -ld /mnt/usb
# 应该显示：drwxrwxrwx（777 权限）

# 4. 检查挂载选项（确保是 rw，可读写）
mount | grep /mnt/usb
# 应该显示 rw 选项，不是 ro

# 5. 测试 Samba 连接和写入（在 OpenWrt 本地测试）
smbclient //localhost/Media -N

# 在 smbclient 提示符下测试写入：
# mkdir test_write
# put /etc/passwd test_write/passwd.txt
# ls test_write
# rm test_write/passwd.txt
# rmdir test_write
# quit
```

### 第五步：从 Mac 连接测试

1. 在 Mac 上打开"访达"（Finder）
2. 按 `Cmd + K` 或菜单栏选择"前往" → "连接服务器"
3. 输入：`smb://192.168.1.1`（替换为你的路由器 IP）
4. 点击"连接"
5. 选择"访客"（Guest），点击"连接"
6. 选择共享：`movies`
7. **尝试创建文件夹或复制文件，验证写入权限**

### 如果无法写入，按以下步骤排查

```bash
# 1. 确认所有关键配置
uci get samba4.@sambashare[0].read_only      # 应该是 'no'
uci get samba4.@sambashare[0].guest_ok       # 应该是 'yes'
uci get samba4.@sambashare[0].force_user      # 应该是 'root'

# 2. 如果配置不对，修复它
uci set samba4.@sambashare[0].read_only='no'
uci set samba4.@sambashare[0].guest_ok='yes'
uci set samba4.@sambashare[0].force_user='root'
uci set samba4.@sambashare[0].force_group='root'
uci commit samba4

# 3. 重新设置权限
chmod 777 /mnt/usb
chmod -R 777 /mnt/usb

# 4. 重启 Samba 服务
/etc/init.d/samba4 restart

# 5. 查看 Samba 日志（如果有错误）
logread | grep samba | tail -20
```

## 步骤七：配置防火墙（如果需要）

确保 Samba 端口可以通过防火墙：

```bash
# 查看防火墙规则
uci show firewall

# 如果 Samba 无法访问，添加规则
uci add firewall rule
uci set firewall.@rule[-1].name='Allow-Samba'
uci set firewall.@rule[-1].src='lan'
uci set firewall.@rule[-1].proto='tcp'
uci set firewall.@rule[-1].dest_port='445'
uci set firewall.@rule[-1].target='ACCEPT'
uci commit firewall
/etc/init.d/firewall restart
```

## 步骤八：在 Infuse 中配置

1. 打开 Apple TV 上的 Infuse 应用
2. 进入 **设置** → **添加文件源**
3. 选择 **网络共享** → **添加**
4. 选择 **SMB** 或 **CIFS**
5. 填写信息：
   - **名称**：自定义名称（如 "R2S Movies"）
   - **地址**：输入路由器的 IP 地址（如 `192.168.1.1`）
   - **用户名**：留空（如果允许匿名访问）
   - **密码**：留空（如果允许匿名访问）
   - **共享**：`movies`（你在 Samba 中设置的共享名称）
6. 点击 **添加**
7. Infuse 会自动扫描并索引媒体文件

## 步骤九：优化设置（可选）

### 1. 设置开机自动挂载

确保 `/etc/config/fstab` 中的挂载点已启用：

```bash
uci set fstab.@mount[0].enabled='1'
uci commit fstab
```

### 2. 优化 Samba 性能

编辑 `/etc/config/samba4`，添加性能优化选项：

```
config samba
    option socket_options 'TCP_NODELAY IPTOS_LOWDELAY SO_RCVBUF=131072 SO_SNDBUF=131072'
    option read_size '2048'
    option max_xmit '65536'
```

### 3. 设置文件权限（重要：确保有写入权限）

**这是确保能够写入文件的关键步骤！**

```bash
# 方法 1：完全开放权限（最简单，适合家庭使用）
chmod 777 /mnt/usb
chmod -R 777 /mnt/usb  # 递归设置所有文件和目录

# 方法 2：更安全的设置（推荐）
# 设置目录权限为 755，文件权限为 644
chmod 755 /mnt/usb
find /mnt/usb -type d -exec chmod 755 {} \;
find /mnt/usb -type f -exec chmod 644 {} \;

# 如果需要允许所有用户写入（推荐用于媒体服务器）
chmod 777 /mnt/usb
find /mnt/usb -type d -exec chmod 777 {} \;
find /mnt/usb -type f -exec chmod 666 {} \;

# 设置所有者（可选）
chown -R nobody:nogroup /mnt/usb
# 或者
chown -R root:root /mnt/usb
```

**重要提示**：
- 如果使用 ext4 文件系统，需要确保挂载时使用了 `rw` 选项
- 如果使用 exFAT 或 NTFS，通常权限设置会被文件系统忽略，主要依赖 Samba 配置

## 故障排查

### 问题 1：USB 设备无法识别或 fdisk -l 不显示

```bash
# 检查 USB 设备（即使 fdisk 不显示，设备可能已被识别）
lsusb
lsblk

# 查看系统消息（插入硬盘后立即执行）
dmesg | tail -50
dmesg | grep -i "usb\|sd"

# 检查内核模块
lsmod | grep usb

# 检查 /dev 目录
ls -la /dev/sd*

# 如果设备是 APFS 格式，fdisk -l 可能不显示分区信息
# 如果设备是 HFS+ 格式，fdisk -l 会显示 "Apple HFS/HFS+"
# 但 OpenWrt 对这两种格式支持很差，建议重新格式化为 ext4、exFAT 或 NTFS
```

### 问题 2：挂载失败

```bash
# 查看系统日志
logread | tail -50

# 检查文件系统类型
blkid /dev/sda1

# 检查文件系统（根据实际类型选择）
fsck.ext4 -f /dev/sda1      # 对于 ext4
fsck.exfat /dev/sda1        # 对于 exFAT
fsck.ntfs /dev/sda1         # 对于 NTFS

# 如果显示 "unknown filesystem type"、"APFS" 或 "HFS+"
# 说明文件系统不被支持或支持很差，需要重新格式化

# 尝试手动指定文件系统类型挂载
mount -t ext4 /dev/sda1 /mnt/usb
mount -t exfat /dev/sda1 /mnt/usb
mount -t ntfs-3g /dev/sda1 /mnt/usb

# 如果是 HFS+ 格式，可以尝试只读挂载（不推荐）
# opkg install kmod-fs-hfsplus
# mount -t hfsplus -o ro /dev/sda2 /mnt/usb  # 注意：可能是 sda2 而不是 sda1

# 查看分区信息，确认哪个是数据分区
fdisk -l
# 通常 EFI 分区是 sda1，数据分区是 sda2
```

### 问题 3：Samba 无法访问

```bash
# 检查 Samba 服务状态
/etc/init.d/samba4 status

# 重启 Samba
/etc/init.d/samba4 restart

# 查看 Samba 日志
logread | grep samba

# 测试连接（从其他设备，访客模式）
smbclient //192.168.1.1/movies -N

# 如果使用用户访问，测试时输入用户名：
# smbclient //192.168.1.1/movies -U nasuser
```

### 问题 3.5：访客访问无法写入文件

这是最常见的问题！按照以下步骤排查：

```bash
# 1. 检查 Samba 配置
uci show samba4

# 2. 确认关键配置项
# 访客访问必须有以下配置：
uci get samba4.@sambashare[0].guest_ok        # 应该是 'yes'
uci get samba4.@sambashare[0].read_only      # 应该是 'no'
uci get samba4.@sambashare[0].force_user      # 应该是 'root' 或存在用户

# 3. 如果没有 force_user，添加它
uci set samba4.@sambashare[0].force_user='root'
uci set samba4.@sambashare[0].force_group='root'
uci commit samba4

# 4. 检查目录权限
ls -ld /mnt/usb
# 应该显示 drwxrwxrwx（777 权限）

# 5. 如果权限不对，修复它
chmod 777 /mnt/usb
chmod -R 777 /mnt/usb  # 递归设置所有文件

# 6. 检查挂载选项（确保是 rw）
mount | grep /mnt/usb
# 应该显示 rw 选项，不是 ro

# 7. 查看实际生成的 Samba 配置文件
cat /etc/samba/smb.conf | grep -A 10 "\[movies\]"
# 应该看到：
#   writable = yes
#   guest ok = yes
#   force user = root
#   create mask = 0666
#   directory mask = 0777

# 8. 如果配置不对，重启 Samba
/etc/init.d/samba4 restart

# 9. 测试写入（在 OpenWrt 上）
smbclient //localhost/movies -N
# 在 smbclient 提示符下：
# mkdir test_write
# put /etc/passwd test_write/passwd
# ls test_write
# quit

# 10. 如果还是不行，检查文件系统类型
# 对于 exFAT/NTFS，权限设置可能无效，主要依赖 Samba 配置
# 确保 Samba 配置中有 force_user='root'
```

### 问题 4：Infuse 无法连接

1. 确认路由器的 IP 地址正确
2. 确认共享名称正确
3. 尝试使用其他设备（如 Mac）连接 Samba 共享测试
4. 检查防火墙设置
5. 尝试使用 IP 地址而不是主机名

### 问题 5：播放卡顿

1. 使用有线连接而不是 Wi-Fi
2. 检查网络速度：`iperf3` 测试
3. 考虑使用 NFS 而不是 SMB（性能更好）
4. 优化视频文件格式（使用 Infuse 支持的格式）

## 使用 NFS 替代 SMB（可选，性能更好）

如果你想要更好的性能，可以使用 NFS：

### 安装 NFS

```bash
opkg install nfs-kernel-server luci-app-nfs
```

### 配置 NFS

编辑 `/etc/exports`：

```
/mnt/usb 192.168.1.0/24(rw,sync,no_subtree_check,no_root_squash)
```

启动 NFS 服务：

```bash
/etc/init.d/nfsd enable
/etc/init.d/nfsd start
```

在 Infuse 中添加 NFS 共享：
- 选择 **NFS** 而不是 **SMB**
- 地址：路由器 IP
- 路径：`/mnt/usb`

## 安全建议

1. **设置 Samba 用户密码**（如果不需要匿名访问）：
   ```bash
   smbpasswd -a root
   ```

2. **限制访问范围**：在防火墙中限制 Samba 只能从内网访问

3. **定期备份**：重要数据要定期备份

4. **文件系统选择**：
   - **ext4**：Linux 原生，性能最好，但 Windows/Mac 无法直接读取（需要额外软件）
   - **exFAT**：跨平台兼容（Mac/Windows/Linux），支持大文件（>4GB），**推荐用于媒体存储**
   - **NTFS**：跨平台兼容，但性能稍差，Windows 原生支持
   - **HFS+**：⚠️ **不推荐**，OpenWrt 只支持只读，不稳定，性能差
   - **APFS**：❌ **完全不支持**，OpenWrt 无法识别和挂载

## 总结

完成以上步骤后，你应该能够：
1. ✅ 移动硬盘自动挂载到 OpenWrt
2. ✅ 通过 Samba 共享访问硬盘内容
3. ✅ 在 Infuse 中浏览和播放电影

如果遇到问题，请参考故障排查部分，或查看 OpenWrt 和 Infuse 的官方文档。

