#!/usr/bin/env python3
"""
YouTube KOL Intelligence Scanner v4
扫描信源频道最新视频，三层漏斗过滤，Tier 1 + Tier 2 均自动跑全流程。

v4 changes:
- Tier 2 也纳入自动处理队列（不再只推荐）
- 每日全流程上限 3 个（Tier 1 + Tier 2 合计），Tier 1 优先
- 超出部分写入 pending_queue，次日优先处理
"""
import json
import subprocess
import sys
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

STATE_FILE = Path(os.path.expanduser("~/.hermes/cache/youtube_scanner_state.json"))

SOURCES = [
    {"type": "channel", "url": "https://www.youtube.com/@a16z", "name": "a16z", "tier": "high"},
    {"type": "channel", "url": "https://www.youtube.com/@axios", "name": "Axios", "tier": "medium"},
    {"type": "channel", "url": "https://www.youtube.com/@GoogleDeepMind", "name": "DeepMind", "tier": "high"},
    {"type": "channel", "url": "https://www.youtube.com/@DwarkeshPatel", "name": "Dwarkesh Patel", "tier": "high"},
    {"type": "channel", "url": "https://www.youtube.com/@EyeonAI", "name": "Eye on AI", "tier": "medium"},
    {"type": "channel", "url": "https://www.youtube.com/@PeterDiamandis", "name": "Peter Diamandis", "tier": "medium"},
    {"type": "channel", "url": "https://www.youtube.com/@TheDiaryOfACEO", "name": "Diary of a CEO", "tier": "medium"},
    {"type": "channel", "url": "https://www.youtube.com/@TheRobotBrainsPodcast", "name": "Robot Brains", "tier": "high"},
    {"type": "playlist", "url": "https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8", "name": "Training Data (Sequoia)", "tier": "high"},
    {"type": "channel", "url": "https://www.youtube.com/@ycombinator", "name": "Y Combinator", "tier": "medium"},
    {"type": "channel", "url": "https://www.youtube.com/@NoPriorsPodcast", "name": "No Priors", "tier": "high"},
    {"type": "channel", "url": "https://www.youtube.com/@DataDrivenNYC", "name": "MAD Podcast (Matt Turck)", "tier": "medium"},
    {"type": "channel", "url": "https://www.youtube.com/@hardfork", "name": "Hard Fork", "tier": "medium"},
]

BIG_NAMES = [
    "karpathy", "andrej",
    "musk", "elon",
    "jensen huang", "jensen",
    "ilya", "sutskever", "ilya sutskever",
    "dario amodei", "dario",
    "sam altman", "altman",
    "geoffrey hinton", "geoff hinton", "hinton",
    "yann lecun", "lecun", "le cun",
    "demis hassabis", "hassabis", "demis",
    "jim fan",
    "john carmack", "carmack",
    "fei-fei li", "feifei li",
    "sutton", "barto",
    "schmidhuber",
    "bengio", "yoshua",
    "sundar pichai", "pichai",
    "satya nadella", "nadella",
    "mark zuckerberg", "zuckerberg", "zuck",
    "eric schmidt",
    "noam brown",
    "terence tao",
    "francois chollet", "françois chollet",
]

AI_KEYWORDS = [
    "world model", "world models",
    "foundation model",
    "open source model", "open-source",
    "vibe coding",
    "software engineer", "software engineering",
    "future of",
    "artificial intelligence",
    "deep learning",
    "machine learning",
    "reinforcement learning",
    "rl from human",
    "frontier model",
    "code generation",
    "agent", "agents",
    "llm", "llms",
    "agi",
    "reasoning",
    "scaling",
    "alignment",
    "robotics",
    "transformer",
    "rlhf",
    "multimodal",
    "inference",
    "fine-tun",
    "autonomous",
    "chatgpt",
    "claude",
    "gemini",
    "copilot",
    "cursor",
    "devin",
    "consciousness",
    "superintellig",
    "singularity",
    "self-play",
    "grpo",
]

NEWS_PATTERNS = [
    r"vs\.?",
    r"can\s+\w+\s+be\s+trusted",
    r"what\s+would\s+you\s+do",
    r"spacex\s+buys",
    r"grok.*disaster",
    r"replacement\s+plan",
    r"attack",
    r"calls\s+\w+\s+disappointment",
]

MIN_DURATION_SEC = 300
PREFERRED_DURATION_SEC = 900
DAILY_PROCESS_LIMIT = 3  # Tier 1 + Tier 2 合计上限


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"processed_ids": [], "wiki_ids": [], "pending_queue": [], "last_scan": None}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def fetch_recent_videos(source_url, source_type, days=3):
    cmd = [
        "/opt/anaconda3/bin/yt-dlp",
        "--flat-playlist",
        "--dump-json",
        "--playlist-end", "30",
        "--no-download",
        source_url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"  [WARN] yt-dlp failed for {source_url}: {result.stderr[:200]}", file=sys.stderr)
            return []
    except subprocess.TimeoutExpired:
        print(f"  [WARN] yt-dlp timeout for {source_url}", file=sys.stderr)
        return []

    videos = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue

        vid = d.get("id", "")
        title = d.get("title", "")
        duration = d.get("duration") or 0
        upload_date = d.get("upload_date") or ""

        if upload_date:
            try:
                dt = datetime.strptime(upload_date, "%Y%m%d")
                if dt < datetime.now() - timedelta(days=days):
                    continue
            except ValueError:
                pass

        videos.append({
            "id": vid,
            "title": title,
            "duration": duration,
            "upload_date": upload_date,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "channel": d.get("channel", "") or d.get("uploader", ""),
        })

    return videos


def is_news_commentary(title):
    title_lower = title.lower()
    for pattern in NEWS_PATTERNS:
        if re.search(pattern, title_lower):
            return True
    return False


def classify_video(video, source):
    title_lower = video["title"].lower()
    duration = video.get("duration", 0)

    if duration > 0 and duration < MIN_DURATION_SEC:
        return "skip"

    if duration == 0:
        short_indicators = ["#short", "#shorts", "clip", "moment", "quick", "in 60 sec", "in 30 sec"]
        if any(ind in title_lower for ind in short_indicators):
            return "skip"

    has_big_name = any(name in title_lower for name in BIG_NAMES)

    if has_big_name and not is_news_commentary(video["title"]):
        return "tier1"

    if has_big_name and is_news_commentary(video["title"]):
        return "tier2"

    if any(kw in title_lower for kw in AI_KEYWORDS):
        return "tier2"

    if source.get("tier") == "high" and duration >= PREFERRED_DURATION_SEC:
        return "tier2"

    return "skip"


def main():
    state = load_state()
    processed = set(state.get("processed_ids", []))
    wiki_ids = set(state.get("wiki_ids", []))
    pending_queue = state.get("pending_queue", [])

    tier1_new = []
    tier2_new = []

    print(f"=== YouTube KOL Scanner v4 — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")

    # Step 0: 先处理 pending_queue 中未做 wiki 的视频
    pending_to_process = []
    for item in pending_queue:
        if item["id"] not in wiki_ids:
            pending_to_process.append(item)

    if pending_to_process:
        print(f"⏳ 待处理队列中有 {len(pending_to_process)} 个待处理视频")

    # 扫描新视频
    for source in SOURCES:
        print(f"Scanning: {source['name']}...")
        videos = fetch_recent_videos(source["url"], source["type"])

        for v in videos:
            if v["id"] in processed:
                continue

            classification = classify_video(v, source)
            if classification == "skip":
                continue

            mins = v.get("duration", 0) // 60
            already_wiki = v["id"] in wiki_ids
            entry = {
                "id": v["id"],
                "title": v["title"],
                "channel": v.get("channel", source["name"]),
                "duration_min": mins,
                "upload_date": v.get("upload_date", ""),
                "url": v["url"],
                "source": source["name"],
                "already_wiki": already_wiki,
                "tier": classification,
            }

            if classification == "tier1":
                tier1_new.append(entry)
                processed.add(v["id"])
            elif classification == "tier2":
                tier2_new.append(entry)
                processed.add(v["id"])

    # 构建处理队列：pending 优先 → Tier 1 → Tier 2，每日上限 3
    to_process = []
    overflow = []

    # 1. pending_queue 先填
    for item in pending_to_process:
        if len(to_process) < DAILY_PROCESS_LIMIT:
            to_process.append({**item, "from_queue": True})
        else:
            overflow.append(item)

    # 2. Tier 1 新发现
    tier1_not_wiki = [v for v in tier1_new if not v["already_wiki"]]
    tier1_done = [v for v in tier1_new if v["already_wiki"]]

    for item in tier1_not_wiki:
        if len(to_process) < DAILY_PROCESS_LIMIT:
            to_process.append({**item, "from_queue": False})
        else:
            overflow.append(item)

    # 3. Tier 2 新发现
    tier2_not_wiki = [v for v in tier2_new if not v["already_wiki"]]
    tier2_done = [v for v in tier2_new if v["already_wiki"]]

    for item in tier2_not_wiki:
        if len(to_process) < DAILY_PROCESS_LIMIT:
            to_process.append({**item, "from_queue": False})
        else:
            overflow.append(item)

    # 输出结果
    output = {
        "to_process": to_process,       # 今日需要跑全流程的视频
        "already_wiki": tier1_done + tier2_done,  # 已做过 wiki 的
        "overflow": overflow,            # 溢出到 pending 的
        "scan_time": datetime.now().isoformat(),
    }

    result_file = Path("/tmp/youtube_scanner_results.json")
    with open(result_file, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # 打印结果
    if to_process:
        print(f"\n📋 今日处理队列 ({len(to_process)}/{DAILY_PROCESS_LIMIT})")
        for v in to_process:
            tier_label = "🔴" if v.get("tier") == "tier1" else "🟡"
            src = " [from队列]" if v.get("from_queue") else ""
            print(f"  {tier_label} {v['title']} ({v['duration_min']}min) — {v['channel']}{src}")
            print(f"    {v['url']}")

    if tier1_done or tier2_done:
        print(f"\n✅ 已完成 wiki ({len(tier1_done) + len(tier2_done)} 个)")
        for v in tier1_done + tier2_done:
            print(f"  • {v['title']} — 已写入 wiki")

    if overflow:
        print(f"\n⏳ 溢出到待处理队列 ({len(overflow)} 个，次日优先)")
        for v in overflow:
            tier_label = "🔴" if v.get("tier") == "tier1" else "🟡"
            print(f"  {tier_label} {v['title']} ({v['duration_min']}min) — {v['channel']}")
            print(f"    {v['url']}")

    if not to_process and not overflow:
        print("\n✅ 今日无新的高价值视频")

    # 更新状态
    state["processed_ids"] = list(processed)[-500:]
    state["pending_queue"] = overflow
    state["last_scan"] = datetime.now().isoformat()
    save_state(state)

    print(f"\n结果已保存: {result_file}")


if __name__ == "__main__":
    main()
