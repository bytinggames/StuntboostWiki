#!/usr/bin/env python3
"""Converts a .tree file into a foldable wiki README.md.

Usage: python tree2readme.py [input.tree] [output.md] [--title "STUNTBOOST Wiki"]

Nodes with children become foldable <details> sections,
nodes without children become the text inside them.
"""
import argparse
import html
import struct
import sys
from pathlib import Path


class Reader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def unpack(self, fmt):
        values = struct.unpack_from(fmt, self.data, self.pos)
        self.pos += struct.calcsize(fmt)
        return values[0]

    def int7(self):
        # .NET BinaryWriter 7-bit encoded int
        result = shift = 0
        while True:
            b = self.unpack("<B")
            result |= (b & 0x7F) << shift
            shift += 7
            if b < 0x80:
                return result

    def string(self):
        length = self.int7()
        text = self.data[self.pos:self.pos + length].decode("utf-8")
        self.pos += length
        return text


def parse_tree(data):
    """Returns (texts, children, root_id): id -> text, id -> [child ids]."""
    r = Reader(data)
    r.unpack("<B")  # format version

    texts = {}
    root_id = None
    for _ in range(r.unpack("<i")):
        size = r.unpack("<q")
        end = r.pos + size
        node_id = r.unpack("<i")
        texts[node_id] = r.string()
        if root_id is None:
            root_id = node_id
        r.pos = end  # skip the remaining node data (styling etc.)

    children = {}
    for _ in range(r.unpack("<i")):
        parent_id = r.unpack("<i")
        children[parent_id] = [r.unpack("<i") for _ in range(r.int7())]

    return texts, children, root_id


def is_list_item(line):
    return line.lstrip().startswith(("- ", "* ", "+ "))


def format_text(text):
    """Keeps the line breaks of a node's text visible in rendered markdown."""
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    out = []
    for i, line in enumerate(lines):
        next_line = lines[i + 1] if i + 1 < len(lines) else None
        # plain line followed by another plain line -> force a hard line break
        if next_line and line and not is_list_item(line) and not is_list_item(next_line):
            line += "  "
        out.append(line)
    return "\n".join(out)


def render(node_id, texts, children, out):
    prev_leaf = None
    for child_id in children.get(node_id, []):
        text = texts[child_id]
        if children.get(child_id):
            out.append("<details>")
            out.append(f"<summary><strong>{html.escape(text, quote=False)}</strong></summary>")
            # GitHub strips CSS, a one-cell table is what boxes the folded content
            out.append("<table><tr><td>")
            out.append("<br>")  # empty line between the title and the first element
            out.append("")
            render(child_id, texts, children, out)
            out.append("</td></tr></table>")
            out.append("</details>")
            out.append("")
            prev_leaf = None
        else:
            # keep consecutive list items together, separate everything else
            if prev_leaf is not None:
                if is_list_item(prev_leaf.split("\n")[-1]) and is_list_item(text):
                    out.pop()
            out.append(format_text(text))
            out.append("")
            prev_leaf = text


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("input", nargs="?", type=Path, default=here / "StuntboostWiki.tree")
    parser.add_argument("output", nargs="?", type=Path, default=here / "README.md")
    parser.add_argument("--title", default="STUNTBOOST Wiki")
    args = parser.parse_args()

    texts, children, root_id = parse_tree(args.input.read_bytes())

    out = [f"# {args.title}"]
    render(root_id, texts, children, out)
    args.output.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {args.output} ({len(texts) - 1} nodes)")


if __name__ == "__main__":
    sys.exit(main())
