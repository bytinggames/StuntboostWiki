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
- Lines directly below each other stay together (as a list or with a line
  break), an empty line in between starts a new paragraph.
"""
import argparse
import html
import re
import sys
from pathlib import Path

TAB_SIZE = 4
VARIABLE = re.compile(r"\$([A-Za-z_]\w*)")
VARIABLE_DEFINITION = re.compile(r"\$([A-Za-z_]\w*)\s*=\s*(.*)")


class Node:
    def __init__(self, text, blank_before=False):
        self.text = text
        self.blank_before = blank_before
        self.children = []


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


def render(nodes, out):
    prev_line = None
    for node in nodes:
        if node.children:
            out.append("<details>")
            out.append(f"<summary><strong>{html.escape(node.text, quote=False)}</strong></summary>")
            # GitHub strips CSS, a one-cell table is what boxes the folded content
            out.append("<table><tr><td>")
            out.append("")
            render(node.children, out)
            out.append("</td></tr></table>")
            out.append("</details>")
            out.append("")
            prev_line = None
        else:
            if prev_line is not None and not node.blank_before:
                out.pop()
                # plain line followed by another plain line -> force a hard line break
                if not is_list_item(prev_line) and not is_list_item(node.text):
                    out[-1] += "  "
            out.append(node.text)
            out.append("")
            prev_line = node.text


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("input", nargs="?", type=Path, default=here / "README.txt")
    parser.add_argument("output", nargs="?", type=Path, default=here / "README.md")
    args = parser.parse_args()

    title, nodes = parse_txt(args.input.read_text(encoding="utf-8"))

    out = [f"# {title}"] if title else []
    render(nodes, out)
    args.output.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    sys.exit(main())
