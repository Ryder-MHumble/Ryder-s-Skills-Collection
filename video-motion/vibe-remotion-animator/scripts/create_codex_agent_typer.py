#!/usr/bin/env python3
"""Create a local Codex-style Remotion typer and agent-run demo."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

FORMATS = {
    "horizontal": (1920, 1080),
    "vertical": (1080, 1920),
    "square": (1080, 1080),
}


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-._")
    return slug or "codex-agent-typer"


def resolve_output_dir(output_dir: str | None, project_name: str) -> Path:
    if output_dir:
        return Path(output_dir).expanduser().resolve()

    root = Path.home() / "Desktop" / "vibe-remotion-animations"
    slug = safe_slug(project_name)
    candidate = root / slug
    if not candidate.exists():
        return candidate.resolve()

    for index in range(2, 1000):
        candidate = root / f"{slug}-{index}"
        if not candidate.exists():
            return candidate.resolve()

    raise SystemExit(f"Could not find an available output directory under {root}")


def replace_in_file(path: Path, replacements: dict[str, str]) -> None:
    text = path.read_text()
    for key, value in replacements.items():
        text = text.replace(key, value)
    path.write_text(text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Codex agent typer Remotion project")
    parser.add_argument(
        "output_dir",
        nargs="?",
        help="Directory to create. Defaults to "${HERMES_OUTPUT:-$HOME/workspace/hermes-output}/vibe-remotion-animations"/<name>",
    )
    parser.add_argument("--name", default="codex-agent-typer", help="Package/project name")
    parser.add_argument("--prompt", default="帮我生成一个办公聊天动效，并渲染关键帧与 MP4。")
    parser.add_argument("--model-label", default="GPT-5 Codex")
    parser.add_argument("--format", choices=sorted(FORMATS), default="horizontal")
    parser.add_argument("--duration", type=float, default=18.0, help="Duration in seconds")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--remotion-version", default="4.0.477")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing output directory")
    args = parser.parse_args()

    out = resolve_output_dir(args.output_dir, args.name)
    template = Path(__file__).resolve().parents[1] / "assets" / "codex-agent-typer-starter"
    if not template.exists():
        raise SystemExit(f"Template not found: {template}")

    if out.exists():
        if not args.force:
            raise SystemExit(f"Output already exists: {out}. Use --force to overwrite.")
        shutil.rmtree(out)

    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, out)
    width, height = FORMATS[args.format]
    duration_frames = max(1, round(args.duration * args.fps))

    replacements = {
        "__PROJECT_NAME__": args.name,
        "__REMOTION_VERSION__": args.remotion_version,
        "__WIDTH__": str(width),
        "__HEIGHT__": str(height),
        "__FPS__": str(args.fps),
        "__DURATION_FRAMES__": str(duration_frames),
        "__FORMAT__": args.format,
        "__PROMPT_JSON__": json.dumps(args.prompt, ensure_ascii=False),
        "__MODEL_LABEL_JSON__": json.dumps(args.model_label, ensure_ascii=False),
    }
    for path in out.rglob("*"):
        if path.is_file() and path.suffix in {".json", ".ts", ".tsx", ".md"}:
            replace_in_file(path, replacements)

    manifest = {
        "project": args.name,
        "kind": "codex-agent-typer",
        "format": args.format,
        "width": width,
        "height": height,
        "fps": args.fps,
        "durationInFrames": duration_frames,
        "durationSeconds": args.duration,
        "prompt": args.prompt,
        "modelLabel": args.model_label,
        "defaultOutputRoot": str(Path.home() / "Desktop" / "vibe-remotion-animations"),
    }
    (out / "codex-agent-typer.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
