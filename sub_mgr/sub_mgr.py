import os
from typing import List
from .core.sub_mgr import SubscriptionConverter, load_config_from_toml
import shutil


def list_subscriptions(config_path: str):
    """列出所有订阅配置"""
    config = load_config_from_toml(config_path)
    if not config:
        print("❌ 配置文件加载失败")
        return

    subscriptions = config.get('subscriptions', [])
    if not subscriptions:
        print("❌ 没有找到订阅配置")
        return

    print(f"📋 找到 {len(subscriptions)} 个订阅配置")
    print("\n" + "="*60)
    print(f"{'名称':<20} {'目标路径':<25} {'订阅URL数量':<12} {'状态':<8}")
    print("-" * 60)

    for sub in subscriptions:
        name = sub.get('name', '未命名')
        dst_path = sub.get('dst_path', '未设置')
        sub_urls = sub.get('sub_urls', [])
        enable = sub.get('enable', True)
        status = "✅ 启用" if enable else "❌ 禁用"

        print(f"{name:<20} {dst_path:<25} {len(sub_urls):<12} {status:<8}")

    print("=" * 60)


def list_location_links(config_path: str):
    """列出订阅的完整location链接"""
    config = load_config_from_toml(config_path)
    if not config:
        print("❌ 配置文件加载失败")
        return

    # 获取location配置
    settings_config = config.get('settings', {})
    location_base = settings_config.get('location')

    if not location_base:
        print("❌ 配置文件中未找到 location 配置")
        print("请在 [settings] 部分添加 location = \"https://example.com/file/\"")
        return

    subscriptions = config.get('subscriptions', [])
    if not subscriptions:
        print("❌ 没有找到订阅配置")
        return

    print(f"📍 基于 location 生成订阅链接")
    print(f"📁 基础路径: {location_base}")
    print("\n" + "="*80)

    enabled_count = 0
    for sub in subscriptions:
        # 只处理启用的订阅
        enable = sub.get('enable', True)
        if not enable:
            continue

        name = sub.get('name', '未命名')
        dst_path = sub.get('dst_path', '')

        if dst_path:
            # 拼接完整的location链接
            full_link = location_base.rstrip('/') + '/' + dst_path.lstrip('/')
            print(f"{name}: {full_link}")
            enabled_count += 1

    print("=" * 80)
    print(f"📊 总计: {enabled_count} 个启用的订阅配置")


def convert_subscriptions(config_path: str, out_dir: str, name: str):
    """转换订阅配置"""
    config = load_config_from_toml(config_path)
    if not config:
        print("❌ 配置文件加载失败")
        return

    subscriptions = config.get('subscriptions', [])
    if not subscriptions:
        print("❌ 没有找到有效的订阅配置")
        return

    for sub in subscriptions:
        if name and sub.get('name') == name:
            subscriptions = [sub]
            break
    print(f"📋 找到 {len(subscriptions)} 个订阅配置")

    # 从配置中获取转换器参数
    converter_config = config.get('converter', {})
    base_url = converter_config.get('base_url')
    config_url = converter_config.get('config_url')
    opts = converter_config.get('opts', {})

    # 创建转换器实例
    converter = SubscriptionConverter(
        base_url=base_url,
        config_url=config_url,
        opts=opts
    )

    # 打印使用的配置
    print(f"🔧 使用转换服务: {converter.base_url}")
    print(f"📄 使用规则配置: {converter.config_url}")
    print(f"⚙️  全局转换选项: {converter.opts}")

    # 检查并创建输出目录
    if not os.path.exists(out_dir):
        print(f"📁 创建输出目录: {out_dir}")
        os.makedirs(out_dir, exist_ok=True)
    else:
        print(f"📁 使用现有输出目录: {out_dir}")

    # 批量转换
    results = converter.batch_convert(subscriptions, out_dir)

    # 打印结果摘要
    print("\n" + "="*50)
    print("📊 转换结果摘要:")
    success_count = 0
    for path, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"  {path}: {status}")
        if success:
            success_count += 1

    print(f"\n🎯 总计: {success_count}/{len(subscriptions)} 个订阅转换成功")


def quick_convert(sub_urls: List[str], dst_path: str):
    """快速转换单个订阅"""
    converter = SubscriptionConverter()
    converter.convert_subscription(sub_urls, dst_path)

def install_subscription(config_path: str, name: str):
    """安装订阅配置到服务器"""
    config = load_config_from_toml(config_path)
    if not config:
        print("❌ 配置文件加载失败")
        return

    subscriptions = config.get('subscriptions', [])
    if not subscriptions:
        print("❌ 没有找到订阅配置")
        return

    # 查找指定名称的订阅配置
    sub_to_install = None
    for sub in subscriptions:
        if sub.get('name') == name:
            sub_to_install = sub
            break

    if not sub_to_install:
        print(f"❌ 没有找到名称为 '{name}' 的订阅配置")
        return

    # 获取安装目录配置
    settings_config = config.get('settings', {})
    install_dir = settings_config.get('install_dir')

    if not install_dir:
        print("❌ 配置文件中未找到 install_dir 配置")
        print("请在 [settings] 部分添加 install_dir = \"/path/to/install/dir\"")
        return

    # 模拟安装过程（实际安装逻辑需要根据具体需求实现）
    dst_dir = os.path.join(install_dir, os.path.dirname(sub_to_install.get('dst_path', '')))
    src_dir = os.path.join(config.get('base_dir', './out'), os.path.dirname(sub_to_install.get('dst_path', '')))

    print(f"📦 正在安装订阅 '{name}' 到服务器...")
    print(f"📁 安装路径: {dst_dir}")

    # 将 out 的相应目录以管理员权限复制到安装目录
    import subprocess
    try:
        subprocess.run([
            'sudo', 'cp', '-r', src_dir, dst_dir
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 以管理员权限复制目录失败: {e}")
        return

    print(f"✅ 订阅 '{name}' 安装完成")