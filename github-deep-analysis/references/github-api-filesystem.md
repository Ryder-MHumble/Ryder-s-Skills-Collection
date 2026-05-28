---
name: github-api-filesystem
description: 当 git clone 失败时，通过 GitHub REST API 逐层探索代码库结构、读取文件内容。适用于快速摸清远程仓库的目录架构和关键文件内容。
tags: [github, exploration, remote-workaround]
---

# GitHub API 作为远程代码库文件系统

当本地无法 `git clone`（代理问题、权限问题、仓库过大），但需要了解远程代码库结构时，用 GitHub API 充当只读文件系统。

## 核心操作

### 1. 列出目录内容
```bash
curl -s "https://api.github.com/repos/{owner}/{repo}/contents/{path}" \
  | python3 -c "import json,sys; items=json.load(sys.stdin); [print(i['type'], i['name']) for i in items]"
```
返回文件/目录列表，每行格式：`file filename` 或 `dir dirname`

### 2. 读取文件内容
```bash
curl -s "https://api.github.com/repos/{owner}/{repo}/contents/{path}/{filename}" \
  | python3 -c "import json,sys; data=json.load(sys.stdin); import base64; print(base64.b64decode(data['content']).decode('utf-8'))"
```
适用于任意文本文件（Python、YAML、JSON、Markdown 等）

### 3. 批量读取同一目录下多个文件
```bash
# 一次性获取多个文件路径的内容
for file in "app/crawlers/base.py" "app/crawlers/registry.py" "sources/talent.yaml"; do
  echo "=== $file ===" >&2
  curl -s "https://api.github.com/repos/{owner}/{repo}/contents/$file" \
    | python3 -c "import json,sys; data=json.load(sys.stdin); import base64; print(base64.b64decode(data['content']).decode('utf-8'))"
done
```

### 4. 递归探索子目录
```bash
# 用 jq 提取所有子目录（如果安装了 jq）
curl -s "https://api.github.com/repos/{owner}/{repo}/contents/app/services" \
  | python3 -c "import json,sys; items=json.load(sys.stdin); [print(i['name']) for i in items if i['type']=='dir']"
```

## 踩坑记录

### 代理问题导致 git clone 失败
- 现象：`git clone` 报 `Failed to connect to 127.0.0.1:7890`
- 原因：全局 git proxy 设置指向本地代理，但该端口不可达
- 解法：直接用 GitHub API，绕过 git 协议

### browser_navigate 超时
- 现象：GitHub 页面 `browser_navigate` 超时
- 解法：用 API 代替，速度更快且更可靠

### base64 编码内容读取失败
- `contents` API 返回的内容是 base64 编码的，需解码
- 二进制文件（图片等）无法用此方式读文本内容
- 超大文件可能超过 API 限制（建议 < 1MB）

## 实用脚本模板
```bash
#!/bin/bash
# explore_repo.sh - 探索远程仓库结构
REPO="Ryder-MHumble/DeanAgent-Backend"
PATH="${1:-.}"  # 默认根目录，可传子目录路径

curl -s "https://api.github.com/repos/$REPO/contents/$PATH" \
  | python3 -c "
import json, sys
items = json.load(sys.stdin)
for i in items:
    t = i['type']
    n = i['name']
    if t == 'dir':
        print(f'dir  {n}/')
    else:
        print(f'file {n}')
"
```

## 注意事项
- GitHub API 有速率限制（60 req/hr 未认证，5000 req/hr 已认证）
- 不要在循环中大量请求，用上面的一次性获取多个文件的方式
- `Accept: application/vnd.github.v3+json` 是默认的，无需特别指定
- 私有仓库需要 Token：添加 `Authorization: Bearer {token}` header
