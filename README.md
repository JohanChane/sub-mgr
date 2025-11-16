# SubMgr

## Config Sample

```toml
# SubMgr 配置文件
[converter]
base_url = "https://api.wcc.best/sub"  # 转换服务的基础URL
config_url = "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online.ini"  # 规则配置文件URL
location = "https://www.example.com/file/"

[converter.opts]
target = "clash"    # 目标格式：clash, surge, quanx 等
list = false        # 是否显示节点列表
udp = true          # 是否启用UDP

[[subscriptions]]
name = "主订阅配置"  # 订阅名称
enable = true       # 是否启用该订阅
sub_urls = [
    "https://example.com/subscribe1",
    "https://example.com/subscribe2"
]
dst_path = "clash/main.yaml"  # 输出文件路径（相对输出目录）
opts = { target = "clash", udp = false }  # 自定义选项（完全覆盖全局选项）
append_opts = { scv = false }  # 追加选项（在全局选项基础上追加）

[[subscriptions]]
name = "备用订阅"    # 订阅名称
enable = true       # 是否启用该订阅
sub_urls = [
    "https://backup.example.com/sub"
]
dst_path = "clash/backup.yaml"  # 输出文件路径
opts = { target = "surge", list = true }  # 使用不同的目标格式

[[subscriptions]]
name = "测试订阅"    # 订阅名称
enable = false      # 禁用该订阅，不会进行转换
sub_urls = [
    "https://test.example.com/sub"
]
dst_path = "clash/test.yaml"  # 输出文件路径

[[subscriptions]]
name = "简单订阅"    # 订阅名称
enable = true       # 是否启用该订阅
sub_urls = [
    "https://simple.example.com/sub"
]
dst_path = "clash/simple.yaml"  # 输出文件路径
# 不自定义选项，使用全局配置

[[subscriptions]]
name = "多URL合并订阅"  # 订阅名称
enable = true       # 是否启用该订阅
sub_urls = [
    "https://provider1.com/sub",
    "https://provider2.com/sub",
    "https://provider3.com/sub"
]
dst_path = "clash/merged.yaml"  # 输出文件路径
append_opts = { emoji = false, new_name = false }  # 微调配置
```