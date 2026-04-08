#!/usr/bin/env python3
"""
PPT Generator - Generate PPT slide images using Google Gemini API.

This script generates PPT slide images based on a slide plan and style template,
then creates an HTML viewer for playback.
"""

import argparse
import base64
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
import requests


# =============================================================================
# Constants
# =============================================================================

DEFAULT_RESOLUTION = "2K"
DEFAULT_TEMPLATE_PATH = "templates/viewer.html"
OUTPUT_BASE_DIR = "outputs"
DEFAULT_OPENROUTER_IMAGE_MODEL = "google/gemini-3.1-flash-image-preview"

# Style template markers
TEMPLATE_START_MARKER = "## "
TEMPLATE_END_MARKER = "## "


# =============================================================================
# Environment Configuration
# =============================================================================

def find_and_load_env() -> bool:
    """
    Find and load .env file from multiple locations.

    Search priority:
    1. Current script directory
    2. Parent directories up to project root (containing .git or .env)
    3. Codex skill standard location (~/\.codex/skills/ppt-generator/)

    Returns:
        True if .env file was found and loaded, False otherwise.
    """
    current_dir = Path(__file__).parent
    env_locations = [
        current_dir / ".env",
        *[parent / ".env" for parent in current_dir.parents],
        Path.home() / ".codex" / "skills" / "ppt-generator-pro" / ".env",
        Path.home() / ".codex" / "skills" / "ppt-generator" / ".env",
        Path.home() / "\.codex" / "skills" / "ppt-generator-pro" / ".env",
        Path.home() / "\.codex" / "skills" / "ppt-generator" / ".env",
    ]

    for env_path in env_locations:
        if env_path.exists():
            load_dotenv(env_path, override=True)
            print(f"Loaded environment from: {env_path}")
            return True

        # Stop at project root if .git exists
        if env_path.parent != current_dir and (env_path.parent / ".git").exists():
            break

    # Fallback: try default loading from system environment
    load_dotenv(override=True)
    print("Warning: No .env file found, using system environment variables")
    return False


# =============================================================================
# Style Template
# =============================================================================

def load_style_template(style_path: str) -> str:
    """
    Load and parse style template file.

    Args:
        style_path: Path to the style template markdown file.

    Returns:
        Extracted base prompt template string.
    """
    with open(style_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract base prompt template section
    start_marker = "## "
    end_marker = "## "

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx + len(start_marker))

    if start_idx == -1 or end_idx == -1:
        print("Warning: Could not parse style template, using full content")
        return content

    return content[start_idx + len(start_marker):end_idx].strip()


# =============================================================================
# Prompt Generation
# =============================================================================

def generate_prompt(
    style_template: str,
    page_type: str,
    content_text: str,
    slide_number: int,
    total_slides: int,
) -> str:
    """
    Generate a prompt for a single slide.

    Args:
        style_template: Base style template text.
        page_type: Type of page (cover, data, content).
        content_text: Text content for the slide.
        slide_number: Current slide number (1-indexed).
        total_slides: Total number of slides.

    Returns:
        Complete prompt string for image generation.
    """
    prompt_parts = [style_template, "\n\n"]

    # Determine page type based on slide position or explicit type
    is_cover = page_type == "cover" or slide_number == 1
    is_data = page_type == "data" or slide_number == total_slides

    if is_cover:
        prompt_parts.append(
            f"""Please generate a cover page based on visual balance aesthetics.
Place a large complex 3D glass object in the center, overlaid with bold text:

{content_text}

Background with extended aurora waves."""
        )
    elif is_data:
        prompt_parts.append(
            f"""Please generate a data/summary page using split-screen design.
Left side: typeset the following text.
Right side: floating large glowing 3D data visualization:

{content_text}"""
        )
    else:
        prompt_parts.append(
            f"""Please generate a content page using Bento grid layout.
Organize the following content in modular rounded rectangle containers.
Container material must be frosted glass with blur effect:

{content_text}"""
        )

    return "".join(prompt_parts)


# =============================================================================
# Image Generation
# =============================================================================

def _resolution_to_openrouter_size(resolution: str) -> str:
    """
    Map project resolution labels to OpenAI-compatible image sizes.

    Note: OpenRouter providers vary by supported sizes. We keep a conservative
    default to maximize compatibility.
    """
    normalized = (resolution or "").strip().upper()
    if normalized in {"0.5K", "1K", "2K", "4K"}:
        return normalized
    return "2K"


def _decode_data_url_to_bytes(data_url: str) -> Optional[bytes]:
    """Decode data URL like data:image/png;base64,... into raw bytes."""
    if not data_url or not data_url.startswith("data:"):
        return None
    try:
        _, b64_data = data_url.split(",", 1)
        return base64.b64decode(b64_data)
    except Exception:
        return None


def _extract_openrouter_message_text(message: Dict[str, Any]) -> str:
    """Extract text content from OpenRouter message for diagnostics."""
    content = message.get("content")
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""

    chunks: List[str] = []
    for part in content:
        if not isinstance(part, dict):
            continue
        if part.get("type") == "text":
            text = part.get("text", "")
            if text:
                chunks.append(str(text))
            continue
        if "text" in part and part.get("text"):
            chunks.append(str(part["text"]))
    return "\n".join(chunks).strip()


def _collect_openrouter_image_urls(message: Dict[str, Any]) -> List[str]:
    """Collect possible image URLs from several OpenRouter response shapes."""
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
        for part in content:
            if not isinstance(part, dict):
                continue

            if part.get("type") == "image_url":
                image_url = part.get("image_url")
                if isinstance(image_url, dict) and image_url.get("url"):
                    urls.append(str(image_url["url"]))
                elif isinstance(image_url, str):
                    urls.append(image_url)
                continue

            if part.get("type") in {"image", "output_image"}:
                image_url = part.get("image_url")
                if isinstance(image_url, dict) and image_url.get("url"):
                    urls.append(str(image_url["url"]))
                elif isinstance(image_url, str):
                    urls.append(image_url)
                elif part.get("url"):
                    urls.append(str(part["url"]))

    seen: set[str] = set()
    deduped: List[str] = []
    for url in urls:
        if not url or url in seen:
            continue
        seen.add(url)
        deduped.append(url)
    return deduped


def _extract_openrouter_image_bytes(response_json: Dict[str, Any]) -> Optional[bytes]:
    """
    Extract generated image bytes from OpenRouter chat-completions response.
    Expected shape:
    choices[0].message.images[0].image_url.url = data:image/png;base64,...
    """
    try:
        choices = response_json.get("choices", [])
        if not choices:
            return None
        message = choices[0].get("message", {})
        image_urls = _collect_openrouter_image_urls(message)
        if not image_urls:
            return None

        for image_url in image_urls:
            data_url_bytes = _decode_data_url_to_bytes(image_url)
            if data_url_bytes:
                return data_url_bytes

            download = requests.get(image_url, timeout=30)
            download.raise_for_status()
            return download.content
    except Exception:
        return None

    return None


def _simplify_prompt_for_image_only(prompt: str, max_chars: int = 2200) -> str:
    """Strip markdown-heavy scaffolding and keep a concise visual brief."""
    filtered_lines: List[str] = []
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
        filtered_lines.append(stripped)

    compact = " ".join(filtered_lines)
    compact = re.sub(r"\s+", " ", compact).strip()
    if len(compact) > max_chars:
        compact = compact[:max_chars].rsplit(" ", 1)[0].strip()
    return compact


def _build_openrouter_prompt(prompt: str, simplified: bool = False) -> str:
    strict_rules = (
        "Output rules:\n"
        "1. Generate exactly ONE image.\n"
        "2. Do NOT return markdown, JSON, or explanatory text.\n"
        "3. Return image output only."
    )

    if simplified:
        concise = _simplify_prompt_for_image_only(prompt)
        return (
            "Create one polished presentation slide image (16:9) based on this brief:\n"
            f"{concise}\n\n"
            f"{strict_rules}"
        )

    return f"{prompt.strip()}\n\n{strict_rules}"


def _get_openrouter_image_models() -> List[str]:
    """Return ordered image-model fallback list for OpenRouter."""
    primary = os.environ.get("OPENROUTER_IMAGE_MODEL", DEFAULT_OPENROUTER_IMAGE_MODEL).strip()
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
    resolution: str,
    slide_number: int,
) -> Optional[bytes]:
    """Request one image from OpenRouter with retry and simplified-prompt fallback."""
    base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
    request_timeout = int(os.environ.get("OPENROUTER_TIMEOUT_SEC", "120"))
    max_attempts = max(1, int(os.environ.get("OPENROUTER_IMAGE_RETRIES", "3")))
    retryable_statuses = {408, 409, 429, 500, 502, 503, 504}
    candidate_models = _get_openrouter_image_models()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost",
        "X-Title": "NanoBanana-PPT-Skills",
    }

    for model_idx, model in enumerate(candidate_models, start=1):
        if model_idx > 1:
            print(f"  Slide {slide_number}: switching to fallback model {model}")

        for attempt in range(1, max_attempts + 1):
            use_simplified_prompt = attempt > 1
            prompt_to_send = _build_openrouter_prompt(prompt, simplified=use_simplified_prompt)
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an image generator. Always return exactly one image result.",
                    },
                    {"role": "user", "content": prompt_to_send},
                ],
                "modalities": ["image", "text"],
                "image_config": {
                    "aspect_ratio": "16:9",
                    "image_size": _resolution_to_openrouter_size(resolution),
                },
            }
            if not model.startswith("openai/"):
                payload["temperature"] = 0.2

            try:
                response = requests.post(
                    f"{base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=request_timeout,
                )
            except requests.RequestException as exc:
                if attempt >= max_attempts:
                    print(f"  Slide {slide_number}: request error with model {model}: {exc}")
                    break
                delay = min(8, 2 ** (attempt - 1))
                print(f"  Slide {slide_number}: request error, retrying in {delay}s ({attempt}/{max_attempts})")
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
                        f"  Slide {slide_number}: model {model} unavailable ({response.status_code}), trying fallback"
                    )
                    break

                if response.status_code in retryable_statuses and attempt < max_attempts:
                    delay = min(8, 2 ** (attempt - 1))
                    print(
                        f"  Slide {slide_number}: OpenRouter HTTP {response.status_code}, "
                        f"retrying in {delay}s ({attempt}/{max_attempts})"
                    )
                    time.sleep(delay)
                    continue

                print(
                    f"  Slide {slide_number} failed: OpenRouter HTTP {response.status_code} "
                    f"(model={model}): {snippet}"
                )
                return None

            response_json = response.json()
            image_bytes = _extract_openrouter_image_bytes(response_json)
            if image_bytes:
                return image_bytes

            if attempt < max_attempts:
                message = (
                    response_json.get("choices", [{}])[0].get("message", {})
                    if response_json.get("choices")
                    else {}
                )
                text_preview = _extract_openrouter_message_text(message)[:180]
                mode = "simplified prompt" if use_simplified_prompt else "original prompt"
                print(
                    f"  Slide {slide_number}: no image returned ({mode}, model={model}), "
                    f"retrying ({attempt}/{max_attempts}). Text preview: {text_preview}"
                )
                time.sleep(1.5)
                continue

            # Give next model a chance if available.
            if model_idx < len(candidate_models):
                print(f"  Slide {slide_number}: model {model} returned no image, trying fallback model")
                break

            print(f"  Slide {slide_number} failed: OpenRouter returned no image data")
            return None

    return None


def get_image_client():
    """
    Initialize and return image generation client.
    Provider priority:
    1) GEMINI_API_KEY (native Google GenAI)
    2) OPENROUTER_API_KEY / OPENAI_API_KEY (OpenRouter via OpenAI SDK)

    Returns:
        Tuple(provider, configured client)

    Raises:
        SystemExit: If no supported API key is found.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            from google import genai
        except ImportError:
            print("Error: google-genai library not installed")
            print("Please run: pip install google-genai")
            sys.exit(1)
        return "gemini", genai.Client(api_key=gemini_key)

    openrouter_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if openrouter_key:
        return "openrouter", openrouter_key

    print("Error: no image API key found")
    print("Set one of: GEMINI_API_KEY, OPENROUTER_API_KEY, OPENAI_API_KEY")
    sys.exit(1)


def generate_slide(
    prompt: str,
    slide_number: int,
    output_dir: str,
    resolution: str = DEFAULT_RESOLUTION,
) -> Optional[str]:
    """
    Generate a single PPT slide image using configured image provider.

    Args:
        prompt: The generation prompt.
        slide_number: Slide number for filename.
        output_dir: Output directory path.
        resolution: Image resolution (2K or 4K).

    Returns:
        Path to saved image, or None if generation failed.
    """
    print(f"Generating slide {slide_number}...")
    image_path = os.path.join(output_dir, "images", f"slide-{slide_number:02d}.png")

    try:
        provider, client = get_image_client()

        if provider == "gemini":
            from google.genai import types

            model = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3-pro-image-preview")
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(
                        aspect_ratio="16:9",
                        image_size=resolution,
                    ),
                ),
            )

            for part in response.parts:
                if part.inline_data is not None:
                    image = part.as_image()
                    image.save(image_path)
                    print(f"  Slide {slide_number} saved: {image_path}")
                    return image_path

            print(f"  Slide {slide_number} failed: No image data received from Gemini")
            return None

        image_bytes = _request_openrouter_image(
            api_key=client,
            prompt=prompt,
            resolution=resolution,
            slide_number=slide_number,
        )
        if not image_bytes:
            return None

        with open(image_path, "wb") as f:
            f.write(image_bytes)
        print(f"  Slide {slide_number} saved: {image_path}")
        return image_path

    except Exception as e:
        print(f"  Slide {slide_number} failed: {e}")
        return None


# =============================================================================
# Output Generation
# =============================================================================

def generate_viewer_html(
    output_dir: str,
    slide_count: int,
    template_path: str,
) -> str:
    """
    Generate HTML viewer for slides playback.

    Args:
        output_dir: Output directory path.
        slide_count: Total number of slides.
        template_path: Path to HTML template.

    Returns:
        Path to generated HTML file.
    """
    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    # Generate image list
    slides_list = [f"'images/slide-{i:02d}.png'" for i in range(1, slide_count + 1)]

    # Replace placeholder
    html_content = html_template.replace(
        "/* IMAGE_LIST_PLACEHOLDER */",
        ",\n            ".join(slides_list),
    )

    html_path = os.path.join(output_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"  Viewer HTML generated: {html_path}")
    return html_path


def save_prompts(output_dir: str, prompts_data: Dict[str, Any]) -> str:
    """
    Save all prompts to JSON file.

    Args:
        output_dir: Output directory path.
        prompts_data: Dictionary containing all prompts and metadata.

    Returns:
        Path to saved JSON file.
    """
    prompts_path = os.path.join(output_dir, "prompts.json")
    with open(prompts_path, "w", encoding="utf-8") as f:
        json.dump(prompts_data, f, ensure_ascii=False, indent=2)
    print(f"  Prompts saved: {prompts_path}")
    return prompts_path


# =============================================================================
# Main Entry Point
# =============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="PPT Generator - Generate PPT images using Gemini API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md --resolution 2K

Environment variables:
  GEMINI_API_KEY: Google AI API key (required)
""",
    )

    parser.add_argument(
        "--plan",
        required=True,
        help="Path to slides plan JSON file (generated by Skill)",
    )
    parser.add_argument(
        "--style",
        required=True,
        help="Path to style template file",
    )
    parser.add_argument(
        "--resolution",
        choices=["2K", "4K"],
        default=DEFAULT_RESOLUTION,
        help=f"Image resolution (default: {DEFAULT_RESOLUTION})",
    )
    parser.add_argument(
        "--output",
        help="Output directory path (default: outputs/TIMESTAMP)",
    )
    parser.add_argument(
        "--template",
        default=DEFAULT_TEMPLATE_PATH,
        help=f"HTML template path (default: {DEFAULT_TEMPLATE_PATH})",
    )

    return parser


def _resolve_existing_path(path_value: str, script_dir: Path) -> Path:
    """
    Resolve a path robustly across different working directories.

    Priority:
    1) Absolute path as-is
    2) Current working directory
    3) Script directory
    """
    candidate = Path(path_value)
    if candidate.is_absolute():
        return candidate

    cwd_candidate = (Path.cwd() / candidate).resolve()
    if cwd_candidate.exists():
        return cwd_candidate

    script_candidate = (script_dir / candidate).resolve()
    return script_candidate


def main() -> None:
    """Main entry point for PPT generation."""
    # Load environment variables
    find_and_load_env()

    # Parse arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    script_dir = Path(__file__).resolve().parent
    plan_path = _resolve_existing_path(args.plan, script_dir)
    style_path = _resolve_existing_path(args.style, script_dir)
    template_path = _resolve_existing_path(args.template, script_dir)

    # Load slides plan
    with open(plan_path, "r", encoding="utf-8") as f:
        slides_plan = json.load(f)

    # Load style template
    style_template = load_style_template(str(style_path))

    # Create output directory
    if args.output:
        output_dir = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"{OUTPUT_BASE_DIR}/{timestamp}"

    os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)

    # Print configuration
    slides = slides_plan["slides"]
    total_slides = len(slides)

    print("=" * 60)
    print("PPT Generator Started")
    print("=" * 60)
    print(f"Style: {style_path}")
    print(f"Resolution: {args.resolution}")
    print(f"Slides: {total_slides}")
    print(f"Output: {output_dir}")
    print("=" * 60)
    print()

    # Initialize prompts data
    prompts_data: Dict[str, Any] = {
        "metadata": {
            "title": slides_plan.get("title", "Untitled Presentation"),
            "total_slides": total_slides,
            "resolution": args.resolution,
            "style": str(style_path),
            "generated_at": datetime.now().isoformat(),
        },
        "slides": [],
    }

    # Generate each slide
    for slide_info in slides:
        slide_number = slide_info["slide_number"]
        page_type = slide_info.get("page_type", "content")
        content_text = slide_info["content"]

        # Generate prompt
        prompt = generate_prompt(
            style_template,
            page_type,
            content_text,
            slide_number,
            total_slides,
        )

        # Generate image
        image_path = generate_slide(prompt, slide_number, output_dir, args.resolution)

        # Record prompt data
        prompts_data["slides"].append({
            "slide_number": slide_number,
            "page_type": page_type,
            "content": content_text,
            "prompt": prompt,
            "image_path": image_path,
        })

        print()

    # Save prompts
    save_prompts(output_dir, prompts_data)

    # Generate viewer HTML
    generate_viewer_html(output_dir, total_slides, str(template_path))

    # Print completion summary
    print()
    print("=" * 60)
    print("Generation Complete!")
    print("=" * 60)
    print(f"Output directory: {output_dir}")
    print(f"Viewer HTML: {os.path.join(output_dir, 'index.html')}")
    print()
    print("Open viewer in browser:")
    print(f"  open {os.path.join(output_dir, 'index.html')}")
    print()


if __name__ == "__main__":
    main()
