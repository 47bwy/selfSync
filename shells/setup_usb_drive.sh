#!/bin/sh

# OpenWrt 移动硬盘格式化和挂载脚本
# 用于 R2S OpenWrt 系统，配置移动硬盘以便通过 Infuse 访问
# 基于文档：docs/01_network/OpenWrt挂载移动硬盘和Infuse配置.md

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认配置
MOUNT_POINT="/mnt/usb"
SHARE_NAME="Media"
FSTYPE=""
DEVICE=""
ROUTER_IP=""

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为 root 用户
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "请使用 root 权限运行此脚本"
        exit 1
    fi
}

# 检查是否为 OpenWrt 系统
check_openwrt() {
    if [ ! -f "/etc/openwrt_release" ]; then
        print_warning "未检测到 OpenWrt 系统，脚本可能无法正常工作"
        printf "是否继续？(y/n): "
        read REPLY
        case "$REPLY" in
            [Yy]*) ;;
            *) exit 1 ;;
        esac
    fi
}

# 更新软件包列表
update_packages() {
    print_info "更新软件包列表..."
    opkg update || {
        print_warning "opkg update 失败，尝试继续..."
    }
}

# 安装必要的软件包
install_packages() {
    print_info "检查并安装必要的软件包..."
    
    # 使用空格分隔的字符串列表（兼容 sh/ash/dash）
    local packages="kmod-usb-storage kmod-usb2 kmod-usb3 usbutils block-mount samba4-server"
    
    local fs_packages=""
    case "$FSTYPE" in
        ext4)
            fs_packages="kmod-fs-ext4 e2fsprogs"
            ;;
        exfat)
            fs_packages="kmod-fs-exfat exfat-fsck exfat-mkfs"
            ;;
        ntfs)
            fs_packages="kmod-fs-ntfs ntfs-3g"
            ;;
    esac
    
    for pkg in $packages; do
        if ! opkg list-installed | grep -q "^$pkg "; then
            print_info "安装 $pkg..."
            opkg install "$pkg" || print_warning "$pkg 安装失败"
        else
            print_info "$pkg 已安装"
        fi
    done
    
    if [ -n "$fs_packages" ]; then
        for pkg in $fs_packages; do
            if ! opkg list-installed | grep -q "^$pkg "; then
                print_info "安装 $pkg..."
                opkg install "$pkg" || print_warning "$pkg 安装失败"
            else
                print_info "$pkg 已安装"
            fi
        done
    fi
}

# 列出可用的 USB 设备
list_usb_devices() {
    print_info "扫描 USB 设备..."
    echo
    
    # 使用 lsblk 列出块设备
    if command -v lsblk >/dev/null 2>&1; then
        print_info "块设备列表 (lsblk):"
        lsblk
        echo
    fi
    
    # 使用 fdisk 列出设备
    if command -v fdisk >/dev/null 2>&1; then
        print_info "磁盘设备列表 (fdisk -l):"
        fdisk -l 2>/dev/null | grep -E "^Disk /dev/" || print_warning "未检测到磁盘设备"
        echo
    fi
    
    # 查看 USB 设备
    if command -v lsusb >/dev/null 2>&1; then
        print_info "USB 设备列表 (lsusb):"
        lsusb
        echo
    fi
    
    # 查看内核消息
    print_info "最近的 USB 相关内核消息:"
    dmesg | grep -i "usb\|sd" | tail -20 || true
    echo
}

# 选择设备
select_device() {
    list_usb_devices
    
    print_info "请输入要使用的设备路径（例如: /dev/sda 或 /dev/sdb）"
    print_warning "注意：请确认设备路径，错误的设备会被格式化！"
    printf "设备路径: "
    read DEVICE
    
    if [ ! -b "$DEVICE" ]; then
        print_error "设备 $DEVICE 不存在或不是块设备"
        exit 1
    fi
    
    # 检查是否已挂载
    if mount | grep -q "$DEVICE"; then
        print_warning "设备 $DEVICE 已被挂载"
        printf "是否卸载? (y/n): "
        read REPLY
        case "$REPLY" in
            [Yy]*)
                # 尝试卸载所有分区
                for part in ${DEVICE}*; do
                    if [ -b "$part" ] && mount | grep -q "$part"; then
                        umount "$part" 2>/dev/null || true
                    fi
                done
                ;;
            *)
                exit 1
                ;;
        esac
    fi
}

# 选择文件系统类型
select_filesystem() {
    echo
    print_info "请选择文件系统类型:"
    echo "1) ext4   - Linux 原生，性能最好（推荐）"
    echo "2) exFAT  - 跨平台兼容，支持大文件（推荐用于媒体）"
    echo "3) NTFS   - Windows 兼容，跨平台"
    echo
    printf "请选择 (1-3) [默认: 2]: "
    read choice
    
    case "${choice:-2}" in
        1)
            FSTYPE="ext4"
            ;;
        2)
            FSTYPE="exfat"
            ;;
        3)
            FSTYPE="ntfs"
            ;;
        *)
            print_error "无效的选择"
            exit 1
            ;;
    esac
    
    print_success "已选择文件系统: $FSTYPE"
}

# 确认格式化
confirm_format() {
    echo
    print_warning "警告：格式化会删除设备上的所有数据！"
    print_info "设备: $DEVICE"
    print_info "文件系统: $FSTYPE"
    echo
    printf "确认要格式化吗? 输入 'YES' 继续: "
    read confirm
    
    if [ "$confirm" != "YES" ]; then
        print_info "已取消操作"
        exit 0
    fi
}

# 创建分区和格式化
format_device() {
    print_info "开始格式化设备 $DEVICE..."
    
    # 保存原始设备路径（可能是 /dev/sda）
    local base_device="$DEVICE"
    
    # 检查并卸载所有现有分区
    print_info "检查现有分区..."
    local partitions_found=false
    for part in ${base_device}*; do
        if [ -b "$part" ] && [ "$part" != "$base_device" ]; then
            partitions_found=true
            print_info "检测到分区: $part"
            # 尝试卸载分区
            if mount | grep -q "$part"; then
                print_info "卸载分区: $part"
                umount "$part" 2>/dev/null || print_warning "卸载 $part 失败，继续尝试..."
            fi
        fi
    done
    
    if [ "$partitions_found" = true ]; then
        print_info "检测到现有分区，将删除所有分区并重新创建"
    else
        print_info "未检测到分区，将创建新分区表"
    fi
    
    # 删除所有分区并创建新的分区表
    print_info "删除所有现有分区并创建新分区表..."
    local target_device=""
    
    if command -v parted >/dev/null 2>&1; then
        print_info "使用 parted 删除分区并创建新分区..."
        # 使用 parted 删除所有分区并创建新分区表
        # 尝试先删除所有分区（如果存在）
        if [ "$partitions_found" = true ]; then
            print_info "删除现有分区..."
            parted -s "$base_device" print 2>/dev/null | grep -E "^[[:space:]]+[0-9]+" | awk '{print $1}' | while read -r part_num; do
                [ -n "$part_num" ] && parted -s "$base_device" rm "$part_num" 2>/dev/null || true
            done
            sleep 1
        fi
        # 创建新的 GPT 分区表（这会清空所有分区信息）
        parted -s "$base_device" mklabel gpt || {
            print_error "创建 GPT 分区表失败"
            exit 1
        }
        # 创建新分区（使用整个磁盘）
        parted -s "$base_device" mkpart primary 0% 100%
        # 等待设备节点创建
        sleep 3
        # 重新扫描分区表
        partprobe "$base_device" 2>/dev/null || true
        sleep 1
    else
        print_info "使用 fdisk 删除分区并创建新分区..."
        # 使用 fdisk 非交互式删除所有分区并创建新分区
        # fdisk 的删除操作需要逐个删除，但我们可以使用 'o' 命令先创建新的 DOS 分区表
        # 然后再转换为 GPT，这样可以快速清空所有分区
        (
            echo o      # 创建新的 DOS 分区表（这会删除所有现有分区和分区表）
            echo g      # 转换为 GPT 分区表
            echo n      # 创建新分区
            echo 1      # 分区号
            echo        # 默认起始扇区（通常是 2048 或最小对齐值）
            echo        # 默认结束扇区（使用整个磁盘）
            echo w      # 写入并退出
        ) | fdisk "$base_device" 2>/dev/null || {
            print_error "创建分区失败"
            exit 1
        }
        sleep 3
        # 重新扫描分区表
        partprobe "$base_device" 2>/dev/null || true
        sleep 1
    fi
    
    # 查找新创建的分区
    for i in 1 2 3; do
        if [ -b "${base_device}1" ]; then
            target_device="${base_device}1"
            break
        elif [ -b "${base_device}p1" ]; then
            target_device="${base_device}p1"
            break
        else
            print_info "等待分区节点创建... ($i/3)"
            sleep 1
        fi
    done
    
    if [ -z "$target_device" ] || [ ! -b "$target_device" ]; then
        print_error "无法找到新创建的分区"
        print_info "尝试手动检查: ls -la ${base_device}*"
        exit 1
    fi
    
    print_success "新分区已创建: $target_device"
    
    # 格式化新分区
    print_info "格式化分区 $target_device 为 $FSTYPE..."
    
    case "$FSTYPE" in
        ext4)
            mkfs.ext4 -F "$target_device" || {
                print_error "格式化失败"
                exit 1
            }
            ;;
        exfat)
            mkfs.exfat "$target_device" || {
                print_error "格式化失败"
                exit 1
            }
            ;;
        ntfs)
            mkfs.ntfs -F "$target_device" || {
                print_error "格式化失败"
                exit 1
            }
            ;;
    esac
    
    DEVICE="$target_device"
    print_success "格式化完成: $DEVICE"
}

# 创建挂载点
create_mount_point() {
    if [ ! -d "$MOUNT_POINT" ]; then
        print_info "创建挂载点: $MOUNT_POINT"
        mkdir -p "$MOUNT_POINT"
    fi
}

# 手动挂载测试
test_mount() {
    print_info "测试挂载设备..."
    
    case "$FSTYPE" in
        ext4)
            mount -t ext4 "$DEVICE" "$MOUNT_POINT" || {
                print_error "挂载失败"
                exit 1
            }
            ;;
        exfat)
            mount -t exfat "$DEVICE" "$MOUNT_POINT" || {
                print_error "挂载失败"
                exit 1
            }
            ;;
        ntfs)
            mount -t ntfs-3g "$DEVICE" "$MOUNT_POINT" || {
                print_error "挂载失败"
                exit 1
            }
            ;;
    esac
    
    # 测试写入
    print_info "测试写入权限..."
    echo "test" > "$MOUNT_POINT/.test_write" 2>/dev/null && {
        rm -f "$MOUNT_POINT/.test_write"
        print_success "挂载和写入测试成功"
    } || {
        print_warning "挂载成功但写入测试失败，可能需要调整权限"
    }
    
    # 显示挂载信息
    df -h "$MOUNT_POINT"
}

# 配置自动挂载
configure_auto_mount() {
    print_info "配置自动挂载..."
    
    # 检查是否已有配置
    local mount_config_exists=false
    if uci show fstab | grep -q "mount.*target.*$MOUNT_POINT"; then
        mount_config_exists=true
        print_warning "检测到现有挂载配置"
        printf "是否更新现有配置? (y/n): "
        read REPLY
        case "$REPLY" in
            [Yy]*) ;;
            *)
                print_info "跳过自动挂载配置"
                return
                ;;
        esac
    fi
    
    # 删除旧的挂载配置（如果存在）
    if [ "$mount_config_exists" = true ]; then
        uci show fstab | grep "mount.*target.*$MOUNT_POINT" | cut -d'.' -f2 | while read -r section; do
            uci delete "fstab.$section"
        done
    fi
    
    # 添加新的挂载配置
    uci add fstab mount
    uci set fstab.@mount[-1].device="$DEVICE"
    uci set fstab.@mount[-1].target="$MOUNT_POINT"
    uci set fstab.@mount[-1].fstype="$FSTYPE"
    uci set fstab.@mount[-1].options="rw,noatime"
    uci set fstab.@mount[-1].enabled="1"
    uci commit fstab
    
    # 启用并重启 fstab 服务
    /etc/init.d/fstab enable
    /etc/init.d/fstab restart
    
    print_success "自动挂载配置完成"
}

# 设置目录权限
set_permissions() {
    print_info "设置目录权限..."
    chmod 777 "$MOUNT_POINT"
    if [ "$(ls -A $MOUNT_POINT 2>/dev/null)" ]; then
        chmod -R 777 "$MOUNT_POINT"
    fi
    print_success "权限设置完成"
}

# 配置 Samba 共享
configure_samba() {
    print_info "配置 Samba 共享..."
    
    # 检查 Samba 配置是否存在
    if [ ! -f "/etc/config/samba4" ]; then
        print_info "创建 Samba 配置文件..."
        touch /etc/config/samba4
    fi
    
    # 配置 Samba 全局设置
    if ! uci show samba4 | grep -q "samba.*name"; then
        uci add samba4 samba
        uci set samba4.@samba[0].name='OpenWrt'
        uci set samba4.@samba[0].workgroup='WORKGROUP'
        uci set samba4.@samba[0].description='OpenWrt NAS'
        uci set samba4.@samba[0].charset='UTF-8'
        uci set samba4.@samba[0].homes='0'
        uci set samba4.@samba[0].interface='lan'
    fi
    
    # 检查共享是否已存在
    local share_exists=false
    local share_index=0
    while uci show samba4 | grep -q "sambashare\[$share_index\]"; do
        local share_name=$(uci get "samba4.@sambashare[$share_index].name" 2>/dev/null)
        if [ "$share_name" = "$SHARE_NAME" ]; then
            share_exists=true
            print_warning "共享 '$SHARE_NAME' 已存在"
            printf "是否更新共享配置? (y/n): "
            read REPLY
            case "$REPLY" in
                [Yy]*)
                    uci set "samba4.@sambashare[$share_index].path=$MOUNT_POINT"
                    uci set "samba4.@sambashare[$share_index].read_only=no"
                    uci set "samba4.@sambashare[$share_index].guest_ok=yes"
                    uci set "samba4.@sambashare[$share_index].create_mask=0666"
                    uci set "samba4.@sambashare[$share_index].dir_mask=0777"
                    uci set "samba4.@sambashare[$share_index].force_user=root"
                    uci set "samba4.@sambashare[$share_index].force_group=root"
                    uci set "samba4.@sambashare[$share_index].browseable=yes"
                    ;;
            esac
            break
        fi
        share_index=$((share_index + 1))
    done
    
    if [ "$share_exists" = false ]; then
        # 添加新的共享
        uci add samba4 sambashare
        uci set samba4.@sambashare[-1].name="$SHARE_NAME"
        uci set samba4.@sambashare[-1].path="$MOUNT_POINT"
        uci set samba4.@sambashare[-1].read_only='no'
        uci set samba4.@sambashare[-1].guest_ok='yes'
        uci set samba4.@sambashare[-1].create_mask='0666'
        uci set samba4.@sambashare[-1].dir_mask='0777'
        uci set samba4.@sambashare[-1].force_user='root'
        uci set samba4.@sambashare[-1].force_group='root'
        uci set samba4.@sambashare[-1].browseable='yes'
    fi
    
    uci commit samba4
    
    # 启动并启用 Samba 服务
    /etc/init.d/samba4 enable
    /etc/init.d/samba4 restart
    
    print_success "Samba 共享配置完成"
}

# 配置防火墙
configure_firewall() {
    print_info "检查防火墙配置..."
    
    # 检查 Samba 规则是否已存在
    local rule_exists=false
    local rule_index=0
    while uci show firewall | grep -q "rule\[$rule_index\]"; do
        local rule_name=$(uci get "firewall.@rule[$rule_index].name" 2>/dev/null)
        if [ "$rule_name" = "Allow-Samba" ]; then
            rule_exists=true
            print_info "防火墙规则已存在"
            break
        fi
        rule_index=$((rule_index + 1))
    done
    
    if [ "$rule_exists" = false ]; then
        print_info "添加防火墙规则..."
        uci add firewall rule
        uci set firewall.@rule[-1].name='Allow-Samba'
        uci set firewall.@rule[-1].src='lan'
        uci set firewall.@rule[-1].proto='tcp'
        uci set firewall.@rule[-1].dest_port='445'
        uci set firewall.@rule[-1].target='ACCEPT'
        uci commit firewall
        /etc/init.d/firewall restart
        print_success "防火墙规则已添加"
    fi
}

# 获取路由器 IP
get_router_ip() {
    # 尝试多种方法获取 IP
    ROUTER_IP=$(ip addr show | grep -E "inet.*brd" | grep -v "127.0.0.1" | head -1 | awk '{print $2}' | cut -d'/' -f1)
    
    if [ -z "$ROUTER_IP" ]; then
        ROUTER_IP=$(ip route | grep default | awk '{print $3}' | head -1)
    fi
    
    if [ -z "$ROUTER_IP" ]; then
        ROUTER_IP="192.168.1.1"  # 默认值
    fi
}

# 显示配置摘要
show_summary() {
    echo
    print_success "=========================================="
    print_success "配置完成！"
    print_success "=========================================="
    echo
    print_info "设备: $DEVICE"
    print_info "文件系统: $FSTYPE"
    print_info "挂载点: $MOUNT_POINT"
    print_info "Samba 共享名: $SHARE_NAME"
    echo
    get_router_ip
    print_info "路由器 IP: $ROUTER_IP"
    echo
    print_info "在 Infuse 中添加 SMB 共享:"
    print_info "  地址: smb://$ROUTER_IP"
    print_info "  共享: $SHARE_NAME"
    print_info "  用户名: (留空)"
    print_info "  密码: (留空)"
    echo
    print_info "测试连接（在 Mac 上）:"
    print_info "  访达 > 前往 > 连接服务器 > smb://$ROUTER_IP"
    echo
}

# 主函数
main() {
    clear
    print_info "=========================================="
    print_info "OpenWrt 移动硬盘格式化和挂载脚本"
    print_info "=========================================="
    echo
    
    check_root
    check_openwrt
    
    # 步骤 1: 更新和安装软件包
    printf "是否先更新和安装软件包? (y/n) [默认: y]: "
    read REPLY
    case "$REPLY" in
        [Nn]*)
            select_filesystem
            ;;
        *)
            update_packages
            select_filesystem
            install_packages
            ;;
    esac
    
    # 步骤 2: 选择设备
    select_device
    
    # 步骤 3: 确认并格式化
    confirm_format
    format_device
    
    # 步骤 4: 创建挂载点并测试挂载
    create_mount_point
    test_mount
    
    # 步骤 5: 配置自动挂载
    printf "是否配置自动挂载? (y/n) [默认: y]: "
    read REPLY
    case "$REPLY" in
        [Nn]*) ;;
        *) configure_auto_mount ;;
    esac
    
    # 步骤 6: 设置权限
    set_permissions
    
    # 步骤 7: 配置 Samba
    printf "是否配置 Samba 共享? (y/n) [默认: y]: "
    read REPLY
    case "$REPLY" in
        [Nn]*) ;;
        *)
            configure_samba
            configure_firewall
            ;;
    esac
    
    # 显示摘要
    show_summary
}

# 运行主函数
main "$@"

