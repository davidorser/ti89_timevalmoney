#!/usr/bin/env python3
"""Convert TI-BASIC source (.txt) into TI-89 variable files (.89f / .89p).

The program is stored in untokenized (source text) form, exactly as the
calculator's Program Editor saves it; the calculator tokenizes it on first run.

Usage:  python3 tools/txt2ti89.py src/pf.txt [src/fp.txt ...] [-o build] [--folder main]

Source format (one statement per line, leading ':' optional):
    :pf(f,i,n)
    :Func
    :...
    :EndFunc
The first line is name(args); the second line, Func or Prgm, picks .89f or .89p.

File layout (all verified against files written by TI Connect):
    0x00  "**TI89**"                 signature
    0x08  01 00
    0x0A  folder name                8 bytes, zero padded
    0x12  comment                    40 bytes, zero padded
    0x3A  01 00 52 00 00 00
    0x40  variable name              8 bytes, zero padded
    0x48  type                       0x13 = FUNC, 0x12 = PRGM
    0x49  03 00 00
    0x4C  total file size            4 bytes, little-endian
    0x50  A5 5A
    0x52  00 00 00 00
    0x56  variable size              2 bytes, big-endian
    0x58  variable data
    end   checksum                   2 bytes, little-endian: sum of the size
                                     and data bytes, low 16 bits
Variable data for untokenized source:
    "(args)" CR "Func" CR ... "EndFunc"   lines joined by 0x0D
    00                                    text terminator
    cursor                                2 bytes, big-endian offset into text
    17 E4 E5 00 01 08 DC                  untokenized-program trailer
"""
import argparse
import os
import re
import sys

TYPE_IDS = {"func": (0x13, ".89f"), "prgm": (0x12, ".89p")}
TRAILER = bytes([0x17, 0xE4, 0xE5, 0x00, 0x01, 0x08, 0xDC])

# Non-ASCII characters accepted in source, mapped to the TI-89 character set.
# Only characters confirmed against real calculator files are listed.
CHARMAP = {"©": 0xA9}


def encode_text(text, src):
    out = bytearray()
    for ch in text:
        if ch in CHARMAP:
            out.append(CHARMAP[ch])
        elif 0x20 <= ord(ch) < 0x7F or ch == "\r":
            out.append(ord(ch))
        else:
            sys.exit(f"{src}: unsupported character {ch!r}; add it to CHARMAP")
    return bytes(out)


def parse_source(path):
    with open(path, encoding="utf-8") as fh:
        lines = [ln.rstrip("\r\n") for ln in fh]
    lines = [ln[1:] if ln.startswith(":") else ln for ln in lines]
    while lines and not lines[-1].strip():
        lines.pop()
    m = re.fullmatch(r"\s*([A-Za-z][A-Za-z0-9_]{0,7})\s*(\(.*\))\s*", lines[0])
    if not m:
        sys.exit(f"{path}: first line must be name(args), name at most 8 characters")
    name, args = m.group(1).lower(), m.group(2)
    kind = lines[1].strip().lower() if len(lines) > 1 else ""
    if kind not in TYPE_IDS:
        sys.exit(f"{path}: second line must be Func or Prgm")
    return name, kind, [args] + lines[1:]


def build_var(name, kind, lines, folder, comment, src):
    text = encode_text("\r".join(lines), src)
    cursor = len(lines[0]) + len(lines[1]) + 2  # start of the body
    data = text + b"\x00" + cursor.to_bytes(2, "big") + TRAILER
    body = len(data).to_bytes(2, "big") + data
    type_id, ext = TYPE_IDS[kind]

    def field(s, n):
        return s.encode("latin-1")[:n].ljust(n, b"\x00")

    header = (b"**TI89**" + b"\x01\x00" + field(folder, 8) + field(comment, 40)
              + b"\x01\x00\x52\x00\x00\x00" + field(name, 8)
              + bytes([type_id, 0x03, 0x00, 0x00]))
    total = len(header) + 4 + 2 + 4 + len(body) + 2
    checksum = (sum(body) & 0xFFFF).to_bytes(2, "little")
    blob = (header + total.to_bytes(4, "little") + b"\xA5\x5A"
            + b"\x00\x00\x00\x00" + body + checksum)
    assert len(blob) == total
    return blob, ext


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("sources", nargs="+")
    ap.add_argument("-o", "--outdir", default="build")
    ap.add_argument("--folder", default="main")
    ap.add_argument("--comment", default="txt2ti89")
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    for src in args.sources:
        name, kind, lines = parse_source(src)
        blob, ext = build_var(name, kind, lines, args.folder, args.comment, src)
        out = os.path.join(args.outdir, name + ext)
        with open(out, "wb") as fh:
            fh.write(blob)
        print(f"{src} -> {out} ({len(blob)} bytes)")


if __name__ == "__main__":
    main()
