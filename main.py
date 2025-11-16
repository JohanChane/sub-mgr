#!/usr/bin/env python3
"""
SubMgr Main Program Entry
"""

import argparse
from sub_mgr import list_subscriptions, convert_subscriptions, quick_convert, list_location_links


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="订阅配置转换工具")
    parser.add_argument("-c", "--config",
                       default="./configs/config.toml",
                       help="配置文件路径 (默认: ./configs/config.toml)")

    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # convert 命令
    convert_parser = subparsers.add_parser('convert', help='转换订阅配置')
    convert_parser.add_argument("-o", "--out-dir",
                               default="./out",
                               help="输出目录路径 (默认: ./out)")

    # list 命令
    list_parser = subparsers.add_parser('list', help='列出订阅配置')

    # list-location 命令
    list_location_parser = subparsers.add_parser('list-location', help='列出订阅的完整location链接')

    args = parser.parse_args()

    if args.command == 'convert':
        convert_subscriptions(args.config, args.out_dir)
    elif args.command == 'list':
        list_subscriptions(args.config)
    elif args.command == 'list-location':
        list_location_links(args.config)
    else:
        # 如果没有指定子命令，显示帮助信息
        parser.print_help()


if __name__ == "__main__":
    main()