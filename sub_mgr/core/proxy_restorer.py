import yaml
import requests


def _fetch_original_proxies(url: str) -> list:
    resp = requests.get(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
        timeout=30
    )
    resp.raise_for_status()
    data = yaml.safe_load(resp.text)
    if isinstance(data, dict) and 'proxies' in data:
        return data['proxies']
    return []


def restore_proxies(dst_path: str, composed_url: str) -> bool:
    try:
        original_proxies = _fetch_original_proxies(composed_url)
        if not original_proxies:
            print(f"  ⚠️  原始URL未返回有效proxies，跳过还原")
            return False

        with open(dst_path, 'r', encoding='utf-8') as f:
            output_data = yaml.safe_load(f)

        if not isinstance(output_data, dict):
            print(f"  ⚠️  输出文件格式异常，跳过还原")
            return False

        if 'proxies' not in output_data:
            print(f"  ⚠️  输出文件中没有proxies字段，跳过还原")
            return False

        output_data['proxies'] = original_proxies

        with open(dst_path, 'w', encoding='utf-8') as f:
            yaml.dump(
                output_data,
                f,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
                width=4096
            )

        print(f"  ✅ 已从原始URL还原 {len(original_proxies)} 个proxies")
        return True

    except requests.exceptions.RequestException as e:
        print(f"  ⚠️  获取原始proxies网络错误: {e}")
        return False
    except Exception as e:
        print(f"  ⚠️  还原proxies失败: {e}")
        return False
