#!/usr/bin/env python3
"""Search the bundled React Bits catalog and rank components for a UI brief."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'references' / 'component-catalog.json'

SYNONYMS = {
    'hero': ['headline', 'landing', 'intro', 'banner', 'title'],
    'text': ['typography', 'headline', 'letters', 'words', 'copy'],
    'scroll': ['sticky', 'stack', 'parallax', 'reveal', 'timeline', 'pinned'],
    'chatbot': ['conversation', 'assistant', 'message', 'ai', 'consumer'],
    'card': ['cards', 'stack', 'panel', 'tile', 'bento'],
    'background': ['bg', 'canvas', 'webgl', 'shader', 'particles', 'grid', 'aurora'],
    'cursor': ['mouse', 'pointer', 'hover', 'magnet', 'trail'],
    'gallery': ['image', 'masonry', 'carousel', 'media'],
    'logo': ['marquee', 'brand', 'loop'],
    'menu': ['nav', 'navbar', 'dock', 'tabs'],
    'mobile': ['app', 'phone', 'touch'],
    'dashboard': ['metric', 'data', 'counter', 'stats'],
}

CATEGORY_HINTS = {
    'TextAnimations': ['text', 'headline', 'typography', 'letters', 'words', 'copy', 'title', 'scramble', 'blur'],
    'Animations': ['hover', 'cursor', 'scroll reveal', 'wrapper', 'click', 'spark', 'magnet', 'transition'],
    'Components': ['card', 'dock', 'carousel', 'menu', 'profile', 'stack', 'gallery', 'layout', 'component'],
    'Backgrounds': ['background', 'hero bg', 'particles', 'webgl', 'shader', 'grid', 'aurora', 'waves', 'orb'],
}

TOKEN_RE = re.compile(r"[a-z0-9\u4e00-\u9fff]+", re.I)

def tokens(text: str) -> set[str]:
    base = set(t.lower() for t in TOKEN_RE.findall(text))
    expanded = set(base)
    for key, vals in SYNONYMS.items():
        if key in base or any(v in base for v in vals):
            expanded.add(key)
            expanded.update(vals)
    return expanded

def score_component(component: dict, query_tokens: set[str], raw_query: str) -> float:
    hay = ' '.join([
        component['name'], component['category'], component.get('description',''),
        ' '.join(component.get('tags', [])), ' '.join(component.get('keywords', [])),
        ' '.join(p['name'] for p in component.get('props', [])),
    ]).lower()
    comp_tokens = tokens(hay)
    score = len(query_tokens & comp_tokens) * 3.0

    raw = raw_query.lower()
    name = component['name'].lower()
    if name in raw or name.replace('-', '') in raw.replace('-', '').replace(' ', ''):
        score += 30
    for cat, hints in CATEGORY_HINTS.items():
        if component['category'] == cat and any(h in raw for h in hints):
            score += 5
    # Penalize heavy WebGL/3D unless explicitly requested.
    heavy = 'heavy' in component.get('keywords', [])
    explicit_heavy = any(x in raw for x in ['3d', 'webgl', 'shader', 'three', 'particles', 'background'])
    if heavy and not explicit_heavy:
        score -= 4
    # Prefer lower dependency components for generic UI requests.
    if not component.get('dependencies'):
        score += 1
    return score

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='UI brief, module name, or component name')
    parser.add_argument('-n', '--limit', type=int, default=8)
    parser.add_argument('--category', choices=['TextAnimations','Animations','Components','Backgrounds'])
    parser.add_argument('--json', action='store_true', help='Print JSON instead of Markdown')
    args = parser.parse_args()

    data = json.loads(CATALOG.read_text())
    qtok = tokens(args.query)
    results = []
    for c in data['components']:
        if args.category and c['category'] != args.category:
            continue
        s = score_component(c, qtok, args.query)
        if s > 0:
            results.append((s, c))
    results.sort(key=lambda x: (-x[0], x[1]['category'], x[1]['name']))
    chosen = [dict(score=round(s, 2), **c) for s, c in results[:args.limit]]

    if args.json:
        print(json.dumps(chosen, ensure_ascii=False, indent=2))
        return
    if not chosen:
        print('No strong matches. Try broader words like text, background, cards, scroll, cursor, hero.')
        return
    for c in chosen:
        deps = ', '.join(c['dependencies']) if c['dependencies'] else 'none'
        props = ', '.join(p['name'] + (f"={p['default']}" if p.get('default') is not None else '') for p in c.get('props', [])[:10])
        print(f"- {c['name']} [{c['category']}] score={c['score']}")
        print(f"  {c['description']}")
        print(f"  deps: {deps}; variants: {', '.join(c['variants'])}")
        if props:
            print(f"  key props: {props}")
        print(f"  source key: {c['key']}")

if __name__ == '__main__':
    main()
