#!/usr/bin/env python3
"""Compose a system prompt from a manifest.

Usage: python compose.py manifest.yaml

Reads the manifest, concatenates modules → types → overlay → team prompt,
(or, with `overlays:` instead of `overlay:`, writes one prompt per surface
that share an identical prefix, so the prefix can be prompt-cached),
strips the sections the manifest lists, and writes the output file.
Warns if the overlay's `foundation:` pin doesn't match the package VERSION.
No dependencies beyond the standard library (the YAML subset used here is
simple enough to parse by hand; swap in PyYAML if manifests grow).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_manifest(path):
    data, key = {}, None
    for raw in Path(path).read_text().splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and key:
            data.setdefault(key, []).append(line[4:].strip())
        elif ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            key, val = key.strip(), val.strip()
            if val.startswith("[") and val.endswith("]"):
                data[key] = [v.strip() for v in val[1:-1].split(",") if v.strip()]
            elif val:
                data[key] = val
            else:
                data[key] = []
    return data


def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text


def strip_section(text, heading):
    """Remove a '## <heading>' section up to the next '## ' heading or EOF."""
    pattern = rf"(?ms)^## {re.escape(heading)}\s*$.*?(?=^## |\Z)"
    return re.sub(pattern, "", text)


def strip_changed(text):
    return re.sub(r"(?m)^Changed:.*$\n?", "", text)


def clean(text, strip):
    if "frontmatter" in strip:
        text = strip_frontmatter(text)
    if "builder-notes" in strip:
        text = strip_section(text, "Builder notes")
    if "rubric" in strip:
        text = strip_section(text, "Rubric")
    if "anti-patterns" in strip:
        text = strip_section(text, "Anti-patterns")
    if "changed" in strip:
        text = strip_changed(text)
    return text.strip() + "\n"


def pin_ok(pin, version):
    """An overlay written against >=X.Y is fine for any X.* at or above Y,
    and stale once the package's major version moves past X (breaking)."""
    m = re.match(r">=\s*(\d+)\.(\d+)", pin or "")
    if not m:
        return True
    major, minor = map(int, m.groups())
    vmaj, vmin = map(int, version.split(".")[:2])
    return vmaj == major and vmin >= minor


REQUIRED = [
    "## Part C — How to emit a response",   # output contract (02)
    "## Scope",                              # platform scope (00)
    "## Where to send people",               # destinations (06)
]


def lint(text, label):
    """Fail if composition stripped something the model needs."""
    missing = [h for h in REQUIRED if h not in text]
    if missing:
        sys.exit(f"LINT FAILED for {label}: missing {missing}")


def main(manifest_path):
    m = parse_manifest(manifest_path)
    overlays = m.get("overlays") or [m["overlay"]]
    if isinstance(overlays, str):
        overlays = [overlays]
    for ov in overlays:
        compose_one(m, ov, manifest_path, many=len(overlays) > 1)


def compose_one(m, overlay_name, manifest_path, many):
    strip = set(m.get("strip", []))
    version = (ROOT / "VERSION").read_text().strip()
    parts, tokens = [], 0

    def add(path, label):
        nonlocal tokens
        text = clean(path.read_text(), strip)
        est = int(len(text.split()) * 1.3)
        tokens += est
        parts.append(f"<!-- {label} -->\n{text}")
        print(f"  {label:<45} ~{est:>5} tokens")

    print(f"Composing {m['name']} [{overlay_name}] from chat-responses@{version}")
    for mod in m.get("modules", []):
        path = ROOT / mod
        if not path.exists():  # allow prefixes: "00" -> 00-foundation.md
            matches = sorted(ROOT.glob(f"{mod}*.md"))
            if len(matches) != 1:
                sys.exit(f"module {mod!r} matches {len(matches)} files")
            path = matches[0]
        add(path, path.name)
    for t in m.get("types", []):
        add(ROOT / "types" / f"{t}.md", f"types/{t}.md")

    overlay = ROOT / "overlays" / f"{overlay_name}.md"
    fm = overlay.read_text()
    pin = re.search(r'^foundation:\s*"?([^"\n]+)"?', fm, re.M)
    if pin and not pin_ok(pin.group(1), version):
        print(f"WARNING: overlay pins foundation {pin.group(1)}, package is {version}")
    add(overlay, f"overlays/{overlay_name}.md")

    team = Path(manifest_path).parent / m.get("team_prompt", "")
    if m.get("team_prompt") and team.exists():
        add(team, m["team_prompt"])
    elif m.get("team_prompt"):
        print(f"  (team prompt {m['team_prompt']} not found — skipped)")

    default = f"build/{overlay_name}.system.md" if many else f"build/{m['name']}.system.md"
    out = Path(manifest_path).parent / (m.get("output", default).replace("{overlay}", overlay_name))
    lint("\n".join(parts), overlay_name)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(parts))
    print(f"Wrote {out} (~{tokens} tokens)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
