#!/usr/bin/env python3
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CLIPS = [
    {
        "name": "IROS 2026 Humanoid VLA",
        "url": "https://www.youtube.com/watch?v=t13_h03ouIQ",
        "start": "00:00:46",
        "end": "00:00:52",
        "output": "iros26_humanoid.mp4",
    },
    {
        "name": "RA-L 2025 Tidiness",
        "url": "https://www.youtube.com/watch?v=uVFTlOq-sxg",
        "start": "00:01:14",
        "end": "00:01:17",
        "output": "ral25_tidiness.mp4",
    },
    {
        "name": "IROS 2025 Language-Guided Planning",
        "url": "https://www.youtube.com/watch?v=v2KtgnkRj-8",
        "start": "00:01:57",
        "end": "00:02:01",
        "output": "iros25_scenegraph.mp4",
    },
    {
        "name": "IROS 2020 MixGAIL",
        "url": "https://www.youtube.com/watch?v=4Ozcn9T6RRM",
        "start": "00:01:10",
        "end": "00:01:15",
        "output": "iros20_mixgail.mp4",
    },
    {
        "name": "IROS 2022 Defensive Autonomous Driving",
        "url": "https://www.youtube.com/watch?v=BSajtGNlbnM",
        "start": "00:00:43",
        "end": "00:00:48",
        "output": "iros22_defensive.mp4",
    },
]

def run(cmd):
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    missing = [tool for tool in ("yt-dlp", "ffmpeg") if shutil.which(tool) is None]
    if missing:
        print("Missing required command(s):", ", ".join(missing))
        print()
        print("Install yt-dlp:")
        print("  python -m pip install -U yt-dlp")
        print("Install ffmpeg with your OS package manager if needed.")
        sys.exit(1)

    output_dir = Path("assets/img/publication_preview")
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="publication_previews_") as tmp:
        tmp = Path(tmp)

        for i, clip in enumerate(CLIPS, 1):
            print(f"\n[{i}/{len(CLIPS)}] {clip['name']}")
            raw_template = tmp / f"clip_{i}.%(ext)s"

            # Download only the requested time range.
            run([
                "yt-dlp",
                "--no-playlist",
                "--download-sections", f"*{clip['start']}-{clip['end']}",
                "--force-keyframes-at-cuts",
                "-f", "bv*[height<=1080]/b[height<=1080]/best",
                "-o", str(raw_template),
                clip["url"],
            ])

            candidates = list(tmp.glob(f"clip_{i}.*"))
            if not candidates:
                raise RuntimeError(f"No downloaded file found for {clip['name']}")
            raw = candidates[0]

            out = output_dir / clip["output"]

            # Web-friendly, silent thumbnail video.
            run([
                "ffmpeg", "-y",
                "-i", str(raw),
                "-an",
                "-vf", r"scale=min(640\,iw):-2",
                "-c:v", "libx264",
                "-preset", "slow",
                "-crf", "24",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                str(out),
            ])

            print("Created:", out)

    print("\nDone.")
    print("Add these files to papers.bib with preview = {...}:")
    for clip in CLIPS:
        print(f"  {clip['output']}")

if __name__ == "__main__":
    main()
