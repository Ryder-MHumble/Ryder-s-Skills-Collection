#!/usr/bin/env python3
"""Copy a bundled React Bits component variant into a React project."""
from __future__ import annotations
import argparse, json, shutil, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / 'assets' / 'react-bits'
CATALOG = ROOT / 'references' / 'component-catalog.json'
VARIANTS = ['JS-CSS', 'JS-TW', 'TS-CSS', 'TS-TW']

def load_catalog():
    return json.loads(CATALOG.read_text())['components']

def normalize(s: str) -> str:
    return re.sub(r'[^a-z0-9]', '', s.lower())

def detect_project(project: Path):
    pkg = project / 'package.json'
    data = json.loads(pkg.read_text()) if pkg.exists() else {}
    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
    uses_ts = (project / 'tsconfig.json').exists() or any((project / 'src').glob('**/*.tsx'))
    uses_tailwind = any(name in deps for name in ['tailwindcss', '@tailwindcss/vite', '@tailwindcss/postcss']) or any((project / n).exists() for n in ['tailwind.config.js', 'tailwind.config.ts', 'postcss.config.js'])
    pm = 'npm'
    if (project / 'pnpm-lock.yaml').exists(): pm = 'pnpm'
    elif (project / 'yarn.lock').exists(): pm = 'yarn'
    elif (project / 'bun.lockb').exists() or (project / 'bun.lock').exists(): pm = 'bun'
    return data, deps, uses_ts, uses_tailwind, pm

def choose_variant(component, requested, uses_ts, uses_tailwind):
    if requested != 'auto':
        if requested not in component['sources']:
            raise SystemExit(f"Variant {requested} not available for {component['name']}. Available: {', '.join(component['sources'])}")
        return requested
    preference = []
    if uses_ts and uses_tailwind:
        preference = ['TS-TW','TS-CSS','JS-TW','JS-CSS']
    elif uses_ts:
        preference = ['TS-CSS','TS-TW','JS-CSS','JS-TW']
    elif uses_tailwind:
        preference = ['JS-TW','JS-CSS','TS-TW','TS-CSS']
    else:
        preference = ['JS-CSS','JS-TW','TS-CSS','TS-TW']
    for v in preference:
        if v in component['sources']:
            return v
    raise SystemExit(f"No usable variant found for {component['name']}")

def install_command(pm, deps):
    pkgs = [d.split('@^')[0] if '@^' in d and not d.startswith('@') else d for d in deps]
    cleaned = []
    for dep in deps:
        if dep.startswith('@'):
            # Keep scoped package and version, e.g. @react-three/fiber@^9
            cleaned.append(dep)
        else:
            cleaned.append(dep)
    if not cleaned:
        return ''
    if pm == 'pnpm': return 'pnpm add ' + ' '.join(cleaned)
    if pm == 'yarn': return 'yarn add ' + ' '.join(cleaned)
    if pm == 'bun': return 'bun add ' + ' '.join(cleaned)
    return 'npm install ' + ' '.join(cleaned)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('component', help='Component name, e.g. ScrollStack')
    parser.add_argument('--project', default='.', help='React project root')
    parser.add_argument('--variant', choices=['auto'] + VARIANTS, default='auto')
    parser.add_argument('--dest', default='src/components/reactbits', help='Destination directory inside project')
    parser.add_argument('--install-deps', action='store_true', help='Run package manager install for missing dependencies')
    args = parser.parse_args()

    project = Path(args.project).resolve()
    catalog = load_catalog()
    matches = [c for c in catalog if normalize(c['name']) == normalize(args.component)]
    if not matches:
        names = [c['name'] for c in catalog if normalize(args.component) in normalize(c['name'])]
        hint = f" Similar: {', '.join(names[:10])}" if names else ''
        raise SystemExit(f"Unknown React Bits component: {args.component}.{hint}")
    component = matches[0]
    _, deps, uses_ts, uses_tailwind, pm = detect_project(project)
    variant = choose_variant(component, args.variant, uses_ts, uses_tailwind)
    src_file = ASSET / component['sources'][variant]
    src_dir = src_file.parent
    dest_dir = project / args.dest / component['name']
    dest_dir.mkdir(parents=True, exist_ok=True)
    for item in src_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, dest_dir / item.name)
    missing = []
    for dep in component.get('dependencies', []):
        pkg = dep.split('@^')[0] if '@^' in dep and not dep.startswith('@') else dep
        if dep.startswith('@') and '@^' in dep:
            pkg = dep.split('@^')[0]
        elif '@' in dep and not dep.startswith('@'):
            pkg = dep.split('@', 1)[0]
        if pkg not in deps:
            missing.append(dep)
    print(f"Copied {component['name']} ({variant}) to {dest_dir}")
    print(f"Import example: import {component['name']} from './components/reactbits/{component['name']}/{component['name']}'")
    if component['name'] == 'ScrollStack':
        print("Named import also available: import ScrollStack, { ScrollStackItem } from './components/reactbits/ScrollStack/ScrollStack'")
    if missing:
        cmd = install_command(pm, missing)
        if args.install_deps:
            import subprocess
            subprocess.run(cmd.split(), cwd=project, check=True)
            print('Installed dependencies:', ', '.join(missing))
        else:
            print('Missing dependencies. Run:')
            print('  ' + cmd)
    else:
        print('Dependencies already satisfied or none required.')

if __name__ == '__main__':
    main()
