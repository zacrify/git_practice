"""
Whisper transcription client.
Supports local model (openai-whisper) or OpenAI Whisper API.
"""

import os
from pathlib import Path


def transcribe_video(video_path: Path) -> list[dict]:
    """
    Transcribe a video file and return SRT segments.

    Returns:
        List of dicts with keys: index, start, end, text
        Times are in seconds (float).
    """
    use_api = os.getenv("USE_WHISPER_API", "false").lower() == "true"

    if use_api:
        return _transcribe_api(video_path)
    else:
        return _transcribe_local(video_path)


def _transcribe_local(video_path: Path) -> list[dict]:
    """Transcribe using local Whisper model (large-v3)."""
    import whisper

    model = whisper.load_model("large-v3")
    result = model.transcribe(
        str(video_path),
        language="en",
        verbose=False,
    )

    segments = []
    for i, seg in enumerate(result["segments"], start=1):
        segments.append({
            "index": i,
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
        })

    return segments


def _transcribe_api(video_path: Path) -> list[dict]:
    """Transcribe using OpenAI Whisper API."""
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with open(video_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="en",
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )

    segments = []
    for i, seg in enumerate(response.segments, start=1):
        segments.append({
            "index": i,
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
        })

    return segments
