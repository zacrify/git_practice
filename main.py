"""
Video Subtitle Translator (English → Thai)
Batch process MP4 videos: transcribe with Whisper, translate with DeepL.
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

from whisper_client import transcribe_video
from deepl_client import translate_srt
from srt_utils import write_srt

load_dotenv()

VIDEOS_DIR = Path("videos")
OUTPUT_DIR = Path("output")
LOGS_DIR = Path("logs")


def setup_logging():
    LOGS_DIR.mkdir(exist_ok=True)
    logger = logging.getLogger("subtitle_translator")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    file_handler = logging.FileHandler(LOGS_DIR / "run.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def get_pending_videos(logger):
    """Return list of MP4 files that don't already have translated output."""
    if not VIDEOS_DIR.exists():
        logger.error("Videos directory not found: %s", VIDEOS_DIR)
        return []

    pending = []
    for mp4 in sorted(VIDEOS_DIR.glob("*.mp4")):
        output_path = OUTPUT_DIR / f"{mp4.stem}.th.srt"
        if output_path.exists():
            logger.info("Skipping (already translated): %s", mp4.name)
        else:
            pending.append(mp4)

    return pending


def process_video(video_path: Path, logger):
    """Transcribe and translate a single video."""
    logger.info("Processing: %s", video_path.name)

    # Step 1: Transcribe English audio → SRT segments
    logger.info("  Transcribing with Whisper...")
    segments = transcribe_video(video_path)
    logger.info("  Transcription complete: %d segments", len(segments))

    # Step 2: Translate English text → Thai
    logger.info("  Translating to Thai with DeepL...")
    translated_segments = translate_srt(segments)
    logger.info("  Translation complete")

    # Step 3: Write Thai .srt file
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / f"{video_path.stem}.th.srt"
    write_srt(translated_segments, output_path)
    logger.info("  Saved: %s", output_path)


def main():
    logger = setup_logging()
    logger.info("=== Video Subtitle Translator ===")

    videos = get_pending_videos(logger)
    if not videos:
        logger.info("No pending videos to process.")
        return

    logger.info("Found %d video(s) to process", len(videos))

    success = 0
    failed = 0

    for video in videos:
        try:
            process_video(video, logger)
            success += 1
        except Exception as e:
            logger.error("Failed to process %s: %s", video.name, e)
            failed += 1

    logger.info("=== Done: %d success, %d failed ===", success, failed)


if __name__ == "__main__":
    main()
