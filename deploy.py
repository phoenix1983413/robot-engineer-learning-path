#!/usr/bin/env python3
"""
部署机器人工程师学习路径到 GitHub Pages
"""

import os
import sys
import subprocess
import json
import urllib.request
import urllib.error

REPO_NAME = "robot-engineer-learning-path"


def github_api_request(method, endpoint, token, data=None):
    """发送 GitHub API 请求"""
    url = f"https://api.github.com/{endpoint}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }
    if data:
        payload = json.dumps(data).encode("utf-8")
    else:
        payload = None

    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_info = json.loads(error_body)
            print(f"❌ API 错误: {error_info.get('message', error_body)}")
        except Exception:
            print(f"❌ API 错误: {error_body}")
        sys.exit(1)


def create_repo(token, username):
    """创建 GitHub 仓库"""
    print(f"📦 正在创建仓库 {username}/{REPO_NAME} ...")
    data = {
        "name": REPO_NAME,
        "description": "机器人工程师学习路径 - 从入门到精通的完整知识体系",
        "private": False,
        "auto_init": False,
    }
    result = github_api_request("POST", "user/repos", token, data)
    print(f"✅ 仓库创建成功: {result['html_url']}")
    return result["clone_url"]


def ensure_repo(token, username):
    """确保仓库存在，不存在则创建"""
    try:
        result = github_api_request("GET", f"repos/{username}/{REPO_NAME}", token)
        print(f"✅ 仓库已存在: {result['html_url']}")
        return result["clone_url"]
    except SystemExit:
        return create_repo(token, username)
    except Exception as e:
        print(f"❌ 检查仓库失败: {e}")
        sys.exit(1)


def git_operations(clone_url, token):
    """配置 remote 并推送"""
    # 将 token 嵌入 URL（仅用于本次推送）
    auth_url = clone_url.replace("https://github.com", f"https://{token}@github.com")

    print("🔗 配置 git remote ...")
    subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", auth_url], check=True)

    print("🚀 推送代码到 GitHub ...")
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
    print("✅ 代码推送成功")


def enable_pages(token, username):
    """启用 GitHub Pages"""
    print("🌐 正在启用 GitHub Pages ...")
    data = {
        "source": {"branch": "main", "path": "/"},
        "build_type": "legacy",
    }
    result = github_api_request(
        "POST", f"repos/{username}/{REPO_NAME}/pages", token, data
    )
    print(f"✅ GitHub Pages 已启用: {result['html_url']}")


def main():
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_USERNAME")

    if not token or not username:
        print("❌ 请设置环境变量 GITHUB_TOKEN 和 GITHUB_USERNAME")
        sys.exit(1)

    # 确保在项目目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    clone_url = ensure_repo(token, username)
    git_operations(clone_url, token)
    enable_pages(token, username)

    print(f"\n🎉 部署完成!")
    print(f"📖 访问地址: https://{username}.github.io/{REPO_NAME}/")
    print(f"💻 仓库地址: https://github.com/{username}/{REPO_NAME}")


if __name__ == "__main__":
    main()
