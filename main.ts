// news-image-20261118 — entry program.
//
// The entry is a single image: a newspaper front page summing up the world
// news of Wednesday 18 November 2026, drawn programmatically by
// build_image.py and committed beside this file as entry.png. All this
// program has to do is place that image where the judge looks for it:
// $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });

const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");

// Sanity-check the source before copying: it must carry the PNG magic
// bytes, so a truncated or swapped file fails loudly instead of being
// handed to the judge.
const head = readFileSync(src).subarray(0, 8);
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
if (!PNG_MAGIC.every((b, i) => head[i] === b)) {
  throw new Error(`entry.png next to main.ts is not a PNG file: ${src}`);
}

copyFileSync(src, dst);

console.log(`entry.png: ${statSync(dst).size} bytes -> ${dst}`);
