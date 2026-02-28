"""
SRT file parsing and formatting utilities.
"""

from pathlib import Path


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_srt(segments: list[dict], output_path: Path):
    """
    Write segments to an SRT file.

    Each segment: {index, start, end, text}
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    for seg in segments:
        lines.append(str(seg["index"]))
        start_ts = format_timestamp(seg["start"])
        end_ts = format_timestamp(seg["end"])
        lines.append(f"{start_ts} --> {end_ts}")
        lines.append(seg["text"])
        lines.append("")  # blank line between entries

    output_path.write_text("\n".join(lines), encoding="utf-8")


def parse_srt(srt_path: Path) -> list[dict]:
    """
    Parse an SRT file into segments.

    Returns list of dicts: {index, start, end, text}
    """
    content = srt_path.read_text(encoding="utf-8")
    blocks = content.strip().split("\n\n")

    segments = []
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue

        index = int(lines[0])
        timestamps = lines[1].split(" --> ")
        start = _parse_timestamp(timestamps[0].strip())
        end = _parse_timestamp(timestamps[1].strip())
        text = "\n".join(lines[2:])

        segments.append({
            "index": index,
            "start": start,
            "end": end,
            "text": text,
        })

    return segments


def _parse_timestamp(ts: str) -> float:
    """Convert SRT timestamp (HH:MM:SS,mmm) to seconds."""
    time_part, millis = ts.split(",")
    h, m, s = time_part.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(millis) / 1000
