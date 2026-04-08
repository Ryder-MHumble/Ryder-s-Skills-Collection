#!/usr/bin/env python3
"""
Transition Prompt Generator Module.

Uses codex AI to analyze slide images and generate transition descriptions
for video generation.
"""

import base64
import os
from pathlib import Path
from typing import Any, Optional, Tuple

from anthropic import Anthropic


# =============================================================================
# Constants
# =============================================================================

DEFAULT_TEMPLATE_PATH = "prompts/transition_template.md"
DEFAULT_MODEL = "codex-sonnet-4-5-20250929"
DEFAULT_OPENROUTER_MODEL = "anthropic/codex-sonnet-4"
DEFAULT_MAX_TOKENS = 2000
DEFAULT_TEMPERATURE = 0.7

# Media type mapping
MEDIA_TYPE_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


# =============================================================================
# Exceptions
# =============================================================================

class PromptGeneratorError(Exception):
    """Exception for prompt generation errors."""
    pass


# =============================================================================
# Transition Prompt Generator
# =============================================================================

class TransitionPromptGenerator:
    """Generator for transition prompts using codex AI."""

    def __init__(self, template_path: str = DEFAULT_TEMPLATE_PATH) -> None:
        """
        Initialize transition prompt generator.

        Args:
            template_path: Path to transition template markdown file.

        Raises:
            FileNotFoundError: If template file not found.
            PromptGeneratorError: If codex API initialization fails.
        """
        self.template_path = template_path

        # Load template
        if not os.path.exists(template_path):
            raise FileNotFoundError(
                f"Transition template not found: {template_path}\n"
                "Please ensure the file exists."
            )

        with open(template_path, "r", encoding="utf-8") as f:
            self.template = f.read()

        print(f"Transition template loaded: {template_path}")

        self.backend = "anthropic"
        self.model = DEFAULT_MODEL

        # Initialize text model client
        self.client = self._init_codex_client()
        print(f"Text model client initialized ({self.backend}, model={self.model})")

    def _init_codex_client(self) -> Any:
        """
        Initialize text API client.
        Priority:
        1. OpenRouter (OPENROUTER_API_KEY / OPENAI_API_KEY)
        2. Anthropic API key
        3. Codex default auth

        Returns:
            Configured API client instance.

        Raises:
            PromptGeneratorError: If initialization fails.
        """
        openrouter_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if openrouter_key:
            try:
                from openai import OpenAI
            except ImportError as e:
                raise PromptGeneratorError(
                    "OpenRouter key detected but openai library is missing. "
                    "Run: pip install openai"
                ) from e

            self.backend = "openrouter"
            self.model = os.environ.get("OPENROUTER_TRANSITION_MODEL", DEFAULT_OPENROUTER_MODEL)
            base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
            return OpenAI(api_key=openrouter_key, base_url=base_url)

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            self.backend = "anthropic"
            self.model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
            return Anthropic(api_key=api_key)

        # Try default config (Codex environment)
        try:
            self.backend = "anthropic"
            self.model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
            return Anthropic()
        except Exception as e:
            raise PromptGeneratorError(
                f"Text model initialization failed.\n"
                f"Please set OPENROUTER_API_KEY or ANTHROPIC_API_KEY in .env file,\n"
                f"or run in Codex environment.\n"
                f"Error: {e}"
            )

    def _to_openai_content(self, message_content: list[dict]) -> list[dict]:
        """Convert Anthropic-style multimodal content blocks to OpenAI format."""
        converted: list[dict] = []
        for item in message_content:
            if item.get("type") == "text":
                converted.append({"type": "text", "text": item.get("text", "")})
                continue

            if item.get("type") == "image":
                source = item.get("source", {})
                media_type = source.get("media_type", "image/jpeg")
                data = source.get("data", "")
                converted.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{media_type};base64,{data}"},
                })
        return converted

    def _call_text_model(self, message_content: list[dict], max_tokens: int) -> str:
        """Call configured text model backend and return plain text output."""
        if self.backend == "openrouter":
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=DEFAULT_TEMPERATURE,
                messages=[{"role": "user", "content": self._to_openai_content(message_content)}],
            )
            return (response.choices[0].message.content or "").strip()

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=DEFAULT_TEMPERATURE,
            messages=[{"role": "user", "content": message_content}],
        )
        return response.content[0].text.strip()

    # -------------------------------------------------------------------------
    # Image Processing
    # -------------------------------------------------------------------------

    @staticmethod
    def _encode_image(image_path: str) -> Tuple[str, str]:
        """
        Encode image to base64 with media type.

        Args:
            image_path: Path to image file.

        Returns:
            Tuple of (base64_string, media_type).
        """
        with open(image_path, "rb") as f:
            image_data = f.read()

        base64_str = base64.standard_b64encode(image_data).decode("utf-8")

        ext = Path(image_path).suffix.lower()
        media_type = MEDIA_TYPE_MAP.get(ext, "image/jpeg")

        return base64_str, media_type

    # -------------------------------------------------------------------------
    # Prompt Generation
    # -------------------------------------------------------------------------

    def generate_prompt(
        self,
        frame_start_path: str,
        frame_end_path: str,
        content_context: Optional[str] = None,
    ) -> str:
        """
        Generate transition prompt by analyzing two frames.

        Args:
            frame_start_path: Path to start frame image.
            frame_end_path: Path to end frame image.
            content_context: Optional context about the content transition.

        Returns:
            Generated transition description.

        Raises:
            PromptGeneratorError: If API call fails.
        """
        print(f"\nAnalyzing transition scene...")
        print(f"  Start: {Path(frame_start_path).name}")
        print(f"  End: {Path(frame_end_path).name}")

        # Encode images
        start_b64, start_media = self._encode_image(frame_start_path)
        end_b64, end_media = self._encode_image(frame_end_path)

        # Build system message with text handling rules
        system_message = self.template + """

**Important - Text Handling Rules**:
1. Video models have issues with text (blur, distortion, garbled). Avoid text changes.
2. If there is text in the frame, explicitly state "text content remains clear and stable"
3. Prioritize transitions through background, decorations, lighting, and color changes
4. If text areas are involved, use fade in/out instead of transformation or movement
5. Avoid descriptions like "text gradually changes", "text moves", "text rotates"
6. Recommended: "text transitions via fade in/out", "text remains clear and stable"

Now, based on the provided [Start Frame] (Image A) and [End Frame] (Image B), generate your transition description.
"""

        if content_context:
            system_message += f"\n**Content Context**: {content_context}\n"

        system_message += "\nPlease generate the transition description."

        # Build multimodal message
        message_content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": start_media,
                    "data": start_b64,
                },
            },
            {"type": "text", "text": "This is the [Start Frame] (Image A)"},
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": end_media,
                    "data": end_b64,
                },
            },
            {"type": "text", "text": "This is the [End Frame] (Image B)"},
            {"type": "text", "text": system_message},
        ]

        print(f"Calling text model API for transition analysis ({self.backend})...")

        try:
            transition_prompt = self._call_text_model(message_content, DEFAULT_MAX_TOKENS)

            print("Transition prompt generated!")
            print(f"\n{'=' * 60}")
            print(transition_prompt)
            print(f"{'=' * 60}\n")

            return transition_prompt

        except Exception as e:
            raise PromptGeneratorError(f"codex API call failed: {e}")

    def generate_preview_prompt(self, first_slide_path: str) -> str:
        """
        Generate preview video prompt for first slide (looping animation).

        Args:
            first_slide_path: Path to first slide image.

        Returns:
            Generated preview animation description.

        Raises:
            PromptGeneratorError: If API call fails.
        """
        print(f"\nGenerating preview prompt...")
        print(f"  Slide: {Path(first_slide_path).name}")

        # Encode image
        image_b64, media_type = self._encode_image(first_slide_path)

        # Build message
        message_content = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": image_b64,
                },
            },
            {
                "type": "text",
                "text": """Please generate a subtle animation prompt for this PPT cover image, for a looping preview video.

Requirements:
1. First and last frames are the same image, video should loop seamlessly
2. Animation should be subtle and elegant, not exaggerated
3. Suggested animation types:
   - Light flow (aurora-like light slowly moving)
   - Glass surface breathing effect (subtle reflection changes)
   - Subtle background gradient color changes
   - Slow rotation of 3D objects (if present)
   - Particle effects (floating light dots)
4. **Important**: Text content must remain clear and stable, no changes, distortion or blur
5. Overall atmosphere should be serene, breathing, waiting to be clicked

Please describe this subtle animation in one paragraph (150-250 words).""",
            },
        ]

        print(f"Calling text model API for preview prompt ({self.backend})...")

        try:
            preview_prompt = self._call_text_model(message_content, 1000)

            print("Preview prompt generated!")
            print(f"\n{'=' * 60}")
            print(preview_prompt)
            print(f"{'=' * 60}\n")

            return preview_prompt

        except Exception as e:
            raise PromptGeneratorError(f"codex API call failed: {e}")


# =============================================================================
# Main (for testing)
# =============================================================================

if __name__ == "__main__":
    print("TransitionPromptGenerator Test")
    print("=" * 60)

    try:
        generator = TransitionPromptGenerator()
        print("\nGenerator initialized successfully.")
        print("To test, provide slide image paths.")
    except Exception as e:
        print(f"Initialization failed: {e}")
