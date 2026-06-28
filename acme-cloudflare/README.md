# acme-cf

ACME SSL 证书管理工具，基于 acme.sh + Cloudflare DNS。

## 安装

```bash
uv sync
```

## 配置

编辑 `config.jsonc`，填入 Cloudflare 凭证和域名列表。

## 使用

```bash
uv run acme-cf apply [--force]   # 签发证书
uv run acme-cf install            # 安装证书到 nginx
uv run acme-cf check              # 检查证书过期时间
uv run acme-cf refresh            # 清除 Cloudflare 缓存
uv run acme-cf list               # 列出 acme.sh 已签发证书

uv run acme-cf -c /path/to/config.jsonc apply
```

## 依赖

- [acme.sh](https://github.com/acmesh-official/acme.sh)
- openssl
- curl
