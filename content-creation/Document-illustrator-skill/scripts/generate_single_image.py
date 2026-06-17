#!/usr/bin/env python3
"""
Document Illustrator - 单图片生成工具
由 codex 负责文档分析和内容归纳，此脚本只负责调用 Gemini API 生成图片
"""

import os
import sys
import argparse
import base64
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
import requests


def _configure_console_encoding():
    """Reduce UnicodeEncodeError risk on Windows terminals."""
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


_configure_console_encoding()


def find_and_load_env():
    """
    智能查找并加载 .env 文件
    优先级：
    1. 当前脚本所在目录的上一级（Skill 根目录）
    2. 当前工作目录
    3. 用户主目录下的 \.codex/skills/document-illustrator/
    """
    # 获取脚本所在目录的上一级（Skill 根目录）
    skill_root = Path(__file__).parent.parent
    env_path = skill_root / ".env"

    if env_path.exists():
        load_dotenv(env_path, override=True)
        return True

    # 尝试当前工作目录
    if Path(".env").exists():
        load_dotenv(".env", override=True)
        return True

    # 尝试 Codex Skill 标准位置
    codex_skill_env = Path.home() / ".codex" / "skills" / "document-illustrator" / ".env"
    if codex_skill_env.exists():
        load_dotenv(codex_skill_env, override=True)
        return True

    # 尝试 Codex Skill 标准位置
    codex_skill_env = Path.home() / "\.codex" / "skills" / "document-illustrator" / ".env"
    if codex_skill_env.exists():
        load_dotenv(codex_skill_env, override=True)
        return True

    # 如果都没找到，尝试默认加载
    load_dotenv(override=True)
    return False


# 智能加载环境变量
find_and_load_env()


def get_image_dimensions(aspect_ratio, resolution):
    """
    根据比例和分辨率返回图片尺寸

    参数：
    - aspect_ratio: "16:9" 或 "3:4"
    - resolution: "2K" 或 "4K"

    返回：(width, height)
    """
    dimensions = {
        "16:9": {
            "2K": (2560, 1440),
            "4K": (3840, 2160)
        },
        "3:4": {
            "2K": (1920, 2560),
            "4K": (2880, 3840)
        }
    }

    if aspect_ratio not in dimensions:
        raise ValueError(f"不支持的比例: {aspect_ratio}，请使用 '16:9' 或 '3:4'")

    if resolution not in dimensions[aspect_ratio]:
        raise ValueError(f"不支持的分辨率: {resolution}，请使用 '2K' 或 '4K'")

    return dimensions[aspect_ratio][resolution]


def _extract_openrouter_message_text(message: Dict[str, Any]) -> str:
    """Extract plain text output for diagnostics."""
    content = message.get("content")
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""

    parts: List[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") == "text" and item.get("text"):
            parts.append(str(item["text"]))
            continue
        if item.get("text"):
            parts.append(str(item["text"]))
    return "\n".join(parts).strip()


def _collect_openrouter_image_urls(message: Dict[str, Any]) -> List[str]:
    """Collect image URLs from known OpenRouter response structures."""
    urls: List[str] = []

    for item in message.get("images", []) or []:
        if not isinstance(item, dict):
            continue
        image_url = item.get("image_url")
        if isinstance(image_url, dict) and image_url.get("url"):
            urls.append(str(image_url["url"]))
            continue
        if isinstance(image_url, str):
            urls.append(image_url)
            continue
        if item.get("url"):
            urls.append(str(item["url"]))

    content = message.get("content")
    if isinstance(content, list):
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "image_url":
                image_url = item.get("image_url")
                if isinstance(image_url, dict) and image_url.get("url"):
                    urls.append(str(image_url["url"]))
                elif isinstance(image_url, str):
                    urls.append(image_url)
                continue
            if item.get("type") in {"image", "output_image"}:
                image_url = item.get("image_url")
                if isinstance(image_url, dict) and image_url.get("url"):
                    urls.append(str(image_url["url"]))
                elif isinstance(image_url, str):
                    urls.append(image_url)
                elif item.get("url"):
                    urls.append(str(item["url"]))

    unique_urls: List[str] = []
    seen: set[str] = set()
    for url in urls:
        if not url or url in seen:
            continue
        seen.add(url)
        unique_urls.append(url)
    return unique_urls


def _extract_openrouter_image_bytes(response_json: Dict[str, Any]) -> Optional[bytes]:
    """Extract image bytes from OpenRouter chat-completions response."""
    try:
        choices = response_json.get("choices", [])
        if not choices:
            return None
        message = choices[0].get("message", {})
        image_urls = _collect_openrouter_image_urls(message)
        if not image_urls:
            return None

        for image_url in image_urls:
            if image_url.startswith("data:"):
                _, b64_data = image_url.split(",", 1)
                return base64.b64decode(b64_data)

            r = requests.get(image_url, timeout=30)
            r.raise_for_status()
            return r.content
    except Exception:
        return None

    return None


def _simplify_prompt_for_openrouter(prompt: str, max_chars: int = 2200) -> str:
    """Compress long markdown instructions into concise visual guidance."""
    lines: List[str] = []
    for line in prompt.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("```"):
            continue
        if re.match(r"^[-*]\s+", stripped):
            stripped = re.sub(r"^[-*]\s+", "", stripped)
        lines.append(stripped)

    compact = " ".join(lines)
    compact = re.sub(r"\s+", " ", compact).strip()
    if len(compact) > max_chars:
        compact = compact[:max_chars].rsplit(" ", 1)[0].strip()
    return compact


def _build_openrouter_prompt(prompt: str, simplified: bool = False) -> str:
    strict_rules = (
        "Output rules:\n"
        "1. Generate exactly ONE image.\n"
        "2. Do NOT return markdown, JSON, code blocks, or analysis text.\n"
        "3. Return image output only."
    )
    if simplified:
        concise = _simplify_prompt_for_openrouter(prompt)
        return (
            "Create one high-quality illustration image based on this brief:\n"
            f"{concise}\n\n"
            f"{strict_rules}"
        )
    return f"{prompt.strip()}\n\n{strict_rules}"


def _get_openrouter_image_models() -> List[str]:
    """Return ordered image-model fallback list for OpenRouter."""
    primary = os.environ.get("OPENROUTER_IMAGE_MODEL", "google/gemini-3.1-flash-image-preview").strip()
    configured_fallbacks = os.environ.get("OPENROUTER_IMAGE_MODEL_FALLBACKS", "").strip()

    models: List[str] = [primary] if primary else []
    if configured_fallbacks:
        models.extend([item.strip() for item in configured_fallbacks.split(",") if item.strip()])
    else:
        models.extend(
            [
                "google/gemini-3-pro-image-preview",
                "google/gemini-2.5-flash-image",
                "openai/gpt-5-image-mini",
                "openai/gpt-5-image",
            ]
        )

    deduped: List[str] = []
    seen: set[str] = set()
    for model in models:
        if model in seen:
            continue
        seen.add(model)
        deduped.append(model)
    return deduped


def _request_openrouter_image(
    api_key: str,
    prompt: str,
    aspect_ratio: str,
    resolution: str,
) -> Optional[bytes]:
    """Request an image with retry + simplified prompt fallback."""
    base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
    timeout_sec = int(os.environ.get("OPENROUTER_TIMEOUT_SEC", "120"))
    max_attempts = max(1, int(os.environ.get("OPENROUTER_IMAGE_RETRIES", "3")))
    retryable_statuses = {408, 409, 429, 500, 502, 503, 504}
    candidate_models = _get_openrouter_image_models()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost",
        "X-Title": "Document-illustrator-skill",
    }

    for model_idx, model in enumerate(candidate_models, start=1):
        if model_idx > 1:
            print(f"提示: 当前模型不可用，尝试备用模型 {model}", file=sys.stderr)

        for attempt in range(1, max_attempts + 1):
            use_simplified_prompt = attempt > 1
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an image generation engine. Return exactly one image.",
                    },
                    {"role": "user", "content": _build_openrouter_prompt(prompt, simplified=use_simplified_prompt)},
                ],
                "modalities": ["image", "text"],
                "image_config": {
                    "aspect_ratio": aspect_ratio,
                    "image_size": resolution,
                },
            }
            if not model.startswith("openai/"):
                payload["temperature"] = 0.2

            try:
                response = requests.post(
                    f"{base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=timeout_sec,
                )
            except requests.RequestException as exc:
                if attempt >= max_attempts:
                    print(f"错误: OpenRouter 请求失败 - {exc}", file=sys.stderr)
                    break
                delay = min(8, 2 ** (attempt - 1))
                print(f"警告: 请求异常，{delay}s 后重试 ({attempt}/{max_attempts})", file=sys.stderr)
                time.sleep(delay)
                continue

            if response.status_code >= 400:
                snippet = response.text[:300]
                lowered = snippet.lower()
                model_unavailable = (
                    response.status_code in {400, 403}
                    and ("not available in your region" in lowered or "no endpoints found" in lowered)
                )
                if model_unavailable and model_idx < len(candidate_models):
                    print(
                        f"警告: 模型 {model} 当前不可用，切换到备用模型",
                        file=sys.stderr,
                    )
                    break

                if response.status_code in retryable_statuses and attempt < max_attempts:
                    delay = min(8, 2 ** (attempt - 1))
                    print(
                        f"警告: OpenRouter HTTP {response.status_code}，{delay}s 后重试 ({attempt}/{max_attempts})",
                        file=sys.stderr,
                    )
                    time.sleep(delay)
                    continue
                print(
                    f"错误: OpenRouter 请求失败 HTTP {response.status_code} (model={model}): {snippet}",
                    file=sys.stderr,
                )
                return None

            response_json = response.json()
            image_bytes = _extract_openrouter_image_bytes(response_json)
            if image_bytes:
                return image_bytes

            if attempt < max_attempts:
                message = response_json.get("choices", [{}])[0].get("message", {})
                text_preview = _extract_openrouter_message_text(message)[:180]
                prompt_label = "简化提示词" if use_simplified_prompt else "原始提示词"
                print(
                    f"警告: OpenRouter 返回了文本未返回图片（{prompt_label}，model={model}），准备重试。文本预览: {text_preview}",
                    file=sys.stderr,
                )
                time.sleep(1.5)
                continue

            if model_idx < len(candidate_models):
                print(f"警告: 模型 {model} 未返回图片，切换到备用模型", file=sys.stderr)
                break

            print("错误: OpenRouter 未返回可用图片数据", file=sys.stderr)
            return None

    return None


def generate_image(title, content, style_prompt, output_path, aspect_ratio="16:9", resolution="2K", is_cover=False):
    """
    调用 Gemini API 生成单张配图

    参数：
    - title: 图片标题
    - content: 图片内容文本
    - style_prompt: 风格提示词
    - output_path: 输出文件路径（包含文件名）
    - aspect_ratio: 宽高比 "16:9" 或 "3:4"
    - resolution: 分辨率 "2K" 或 "4K"
    - is_cover: 是否为封面图

    返回：成功返回图片路径，失败返回 None
    """
    # 组合提示词
    if is_cover:
        # 封面图的提示词，强调概括性和引导性
        full_prompt = f"""{style_prompt}

这是一张封面图，需要概括整个文档的核心信息。

标题：{title}

核心内容（需要在一张图中体现）：
{content}

要求：
- 封面图需要突出主题，具有引导性
- 信息要精炼但完整，能代表整个系列
- 视觉冲击力强，吸引读者注意
"""
    else:
        # 普通内容配图
        full_prompt = f"""{style_prompt}

根据以下内容生成配图：

标题：{title}

内容：
{content}
"""

    try:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Provider 1: Native Gemini
        gemini_key = os.environ.get("GEMINI_API_KEY")
        if gemini_key:
            try:
                from google import genai
                from google.genai import types
            except ImportError:
                print("错误: 未安装 google-genai 库", file=sys.stderr)
                print("请运行: pip install google-genai", file=sys.stderr)
                return None

            client = genai.Client(api_key=gemini_key)
            response = client.models.generate_content(
                model=os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3-pro-image-preview"),
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE'],
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio,
                        image_size=resolution
                    )
                )
            )
            for part in response.parts:
                if part.inline_data is not None:
                    image = part.as_image()
                    image.save(output_path)
                    return output_path
            print("警告: Gemini 未返回图片数据", file=sys.stderr)
            return None

        # Provider 2: OpenRouter (OpenAI-compatible)
        openrouter_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if not openrouter_key:
            print("错误: 未设置 GEMINI_API_KEY 或 OPENROUTER_API_KEY", file=sys.stderr)
            return None

        image_bytes = _request_openrouter_image(
            api_key=openrouter_key,
            prompt=full_prompt,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
        )
        if not image_bytes:
            return None

        with open(output_path, "wb") as f:
            f.write(image_bytes)
        return output_path

    except Exception as e:
        import traceback
        print(f"错误: 图片生成失败 - {e}", file=sys.stderr)
        print(f"详细错误信息:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return None


def main():
    """主流程"""
    parser = argparse.ArgumentParser(
        description='Document Illustrator - 单图片生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 生成普通内容配图
  python generate_single_image.py \\
    --title "AI 工具演化" \\
    --content "从 Rules 到 Skills 的演化历程..." \\
    --style-file ../styles/ticket.md \\
    --output /path/to/output/image-01.png \\
    --ratio 16:9 \\
    --resolution 2K

  # 生成封面图
  python generate_single_image.py \\
    --title "AI 编程工具完全指南" \\
    --content "本文介绍..." \\
    --style-file ../styles/gradient-glass.md \\
    --output /path/to/output/cover.png \\
    --ratio 3:4 \\
    --resolution 2K \\
    --cover

环境变量:
  GEMINI_API_KEY: Google AI API 密钥（必需）
"""
    )

    parser.add_argument('--title', required=True, help='图片标题')
    parser.add_argument('--content', required=True, help='图片内容文本')
    parser.add_argument('--style-file', required=True, help='风格提示词文件路径')
    parser.add_argument('--output', required=True, help='输出文件路径（包含文件名）')
    parser.add_argument(
        '--ratio',
        choices=['16:9', '3:4'],
        default='16:9',
        help='宽高比（默认: 16:9）'
    )
    parser.add_argument(
        '--resolution',
        choices=['2K', '4K'],
        default='2K',
        help='分辨率（默认: 2K）'
    )
    parser.add_argument(
        '--cover',
        action='store_true',
        help='标记为封面图（会使用不同的提示词策略）'
    )

    args = parser.parse_args()

    # 读取风格提示词
    style_file_path = Path(args.style_file)
    if not style_file_path.exists():
        print(f"错误: 风格文件不存在: {args.style_file}", file=sys.stderr)
        sys.exit(1)

    with open(style_file_path, 'r', encoding='utf-8') as f:
        style_prompt = f.read()

    # 显示生成信息
    image_type = "封面图" if args.cover else "内容配图"
    print(f"正在生成{image_type}...")
    print(f"  标题: {args.title}")
    print(f"  比例: {args.ratio}")
    print(f"  分辨率: {args.resolution}")

    width, height = get_image_dimensions(args.ratio, args.resolution)
    print(f"  尺寸: {width}x{height}")

    # 生成图片
    result_path = generate_image(
        title=args.title,
        content=args.content,
        style_prompt=style_prompt,
        output_path=args.output,
        aspect_ratio=args.ratio,
        resolution=args.resolution,
        is_cover=args.cover
    )

    if result_path:
        print(f"[OK] 已保存: {result_path}")
        sys.exit(0)
    else:
        print("[ERROR] 生成失败", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
