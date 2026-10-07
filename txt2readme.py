#!/usr/bin/env python3
"""Converts the wiki .txt outline into a foldable wiki README.md.

Usage: python txt2readme.py [input.txt] [output.md]

Format of the .txt file:
- The first line can be "# Title" and becomes the heading of the README.
- Below that, variables can be defined, one per line: $name = value
  Every $name in the rest of the file gets replaced by its value.
- Indentation defines the structure (4 spaces or a tab per level).
- A line with deeper indented lines below it becomes a foldable section,
  with that line as its title.
- All other lines are the text inside the section. Markdown works there.
- Lines directly below each other stay together (with a line break), an
  empty line in between starts a new paragraph.
- Lines starting with "- " are shown with a "•" in front instead of as a real
  list, so they don't get indented.
- [[Section title]] or [[Parent title/Section title]] becomes a link that
  jumps to that section, with the text between the brackets as link text.
"""
import argparse
import html
import re
import sys
from pathlib import Path

TAB_SIZE = 4
VARIABLE = re.compile(r"\$([A-Za-z_]\w*)")
VARIABLE_DEFINITION = re.compile(r"\$([A-Za-z_]\w*)\s*=\s*(.*)")
SECTION_LINK = re.compile(r"\[\[(.+?)\]\]")


class Node:
    def __init__(self, text, blank_before=False):
        self.text = text
        self.blank_before = blank_before
        self.children = []
        self.anchor = None  # set when a [[link]] points to this section


def insert_variables(text, variables, number):
    def replace(match):
        if match[1] in variables:
            return variables[match[1]]
        print(f"Warning: line {number}: unknown variable {match[0]}")
        return match[0]

    return VARIABLE.sub(replace, text)


def parse_txt(content):
    """Returns (title, nodes): the heading (or None) and the top level nodes."""
    lines = content.lstrip("﻿").splitlines()

    title = None
    first = next((i for i, line in enumerate(lines) if line.strip()), None)
    if first is not None and lines[first].startswith("# "):
        title = lines[first][2:].strip()
        lines[first] = ""

    # variable definitions, up to the first line that isn't one
    variables = {}
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        match = VARIABLE_DEFINITION.fullmatch(line.strip())
        if not match or line[0].isspace():
            break
        variables[match[1]] = match[2]
        lines[i] = ""

    root = Node(None)
    # (indent, node the lines of that indent get added to)
    stack = [(0, root)]
    last = None
    blank = False
    for number, raw in enumerate(lines, 1):
        line = raw.expandtabs(TAB_SIZE)
        text = line.strip()
        if not text:
            blank = True
            continue

        indent = len(line) - len(line.lstrip())
        if indent > stack[-1][0]:
            if last is None:
                sys.exit(f"line {number}: the first line must not be indented")
            stack.append((indent, last))
        else:
            while indent < stack[-1][0]:
                stack.pop()
            if indent != stack[-1][0]:
                sys.exit(f"line {number}: indentation doesn't match any level above")

        last = Node(insert_variables(text, variables, number), blank)
        stack[-1][1].children.append(last)
        blank = False

    return title, root.children


def is_list_item(line):
    return line.startswith(("- ", "* ", "+ "))


def collect_sections(nodes, path=(), top=None):
    """Yields (path of titles, top level section it is in) for every section."""
    for node in nodes:
        if node.children:
            node_path = path + (node.text.lower(),)
            yield node_path, top or node
            yield from collect_sections(node.children, node_path, top or node)


def link_sections(nodes):
    """Replaces every [[Section title]] with a link to that section.

    GitHub can't unfold a section when a link is clicked and can't jump to
    something inside a folded section, so the link jumps to the top level
    section the target is in.
    """
    sections = list(collect_sections(nodes))
    anchors = set()

    def replace(match):
        target = tuple(part.strip().lower() for part in match[1].split("/"))
        section = next((node for path, node in sections if path[-len(target):] == target), None)
        if section is None:
            print(f"Warning: no section found for {match[0]}")
            return match[0]
        if section.anchor is None:
            slug = base = re.sub(r"[^a-z0-9]+", "-", section.text.lower()).strip("-") or "section"
            count = 1
            while slug in anchors:
                count += 1
                slug = f"{base}-{count}"
            anchors.add(slug)
            section.anchor = slug
        return f"[{match[1]}](#{section.anchor})"

    def visit(nodes):
        for node in nodes:
            if node.children:
                visit(node.children)
            else:
                node.text = SECTION_LINK.sub(replace, node.text)

    visit(nodes)


def render(nodes, out):
    prev_line = None
    for node in nodes:
        if node.children:
            out.append("<details>")
            anchor = f'<a name="{node.anchor}"></a>' if node.anchor else ""
            out.append(f"<summary>{anchor}<strong>{html.escape(node.text, quote=False)}</strong></summary>")
            # GitHub strips CSS, a definition list is what indents the folded content
            out.append("<dl><dd>")
            if node.children[0].children:
                out.append("<br>")  # empty line between the title and a section right below it
            out.append("")
            render(node.children, out)
            out.append("</dd></dl>")
            if any(child.children for child in node.children):
                out.append("<hr>")  # marks the end of an unfolded section that has sections in it
            out.append("</details>")
            out.append("")
            prev_line = None
        else:
            if prev_line is not None and not node.blank_before:
                # lines directly below each other -> force a hard line break
                out.pop()
                out[-1] += "  "
            # GitHub indents real lists a lot, so list items are written as
            # plain lines starting with a dot
            out.append("• " + node.text[2:] if is_list_item(node.text) else node.text)
            out.append("")
            prev_line = node.text


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("input", nargs="?", type=Path, default=here / "README.txt")
    parser.add_argument("output", nargs="?", type=Path, default=here / "README.md")
    args = parser.parse_args()

    title, nodes = parse_txt(args.input.read_text(encoding="utf-8"))

    link_sections(nodes)

    out = [f"# {title}"] if title else []
    render(nodes, out)
    args.output.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    sys.exit(main())
