# Video Subtitle Translator (English → Thai)

Batch process MP4 videos to generate Thai subtitles using OpenAI Whisper (transcription) and DeepL (translation).

## Project Structure

```
main.py             # Entry point — batch runner, logging, skip logic
whisper_client.py   # Transcription (local Whisper large-v3 or OpenAI API)
deepl_client.py     # Translation (DeepL EN → TH)
srt_utils.py        # SRT parsing, formatting, file I/O
videos/             # Input: place .mp4 files here
output/             # Output: translated .th.srt files
logs/               # Runtime logs (run.log)
```

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy .env.example → .env and fill in API keys
cp .env.example .env

# 3. Place MP4 files in videos/
# 4. Run
python main.py
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DEEPL_API_KEY` | Yes | DeepL free or pro API key |
| `OPENAI_API_KEY` | If API mode | Required when `USE_WHISPER_API=true` |
| `USE_WHISPER_API` | No | `false` (default) = local model, `true` = OpenAI API |

## Key Conventions

- **Resume logic**: Videos with existing `output/<name>.th.srt` are skipped automatically.
- **Error handling**: Failures on individual videos are logged and do not stop the batch.
- **Timestamps**: Translation only touches subtitle text — timing and sequence numbers are never modified.
- **Whisper model**: Uses `large-v3` locally for best accuracy on Malaysian English accents. Requires ~10GB VRAM (falls back to CPU if unavailable).
- **DeepL free tier**: 500k chars/month — sufficient for most batches.

## Development Notes

- Python 3.10+ required (uses `list[dict]` type hints).
- `ffmpeg` must be installed on the system for Whisper to process video files.
- Logs go to both console and `logs/run.log`.
- All SRT files are written as UTF-8.
