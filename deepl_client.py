"""
DeepL translation client.
Translates English subtitle text to Thai, preserving timing.
"""

import os
import deepl


def translate_srt(segments: list[dict]) -> list[dict]:
    """
    Translate subtitle segments from English to Thai.

    Takes segments with keys: index, start, end, text
    Returns new segments with translated text (timing preserved).
    """
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is not set")

    translator = deepl.Translator(api_key)

    texts = [seg["text"] for seg in segments]

    # Batch translate for efficiency
    results = translator.translate_text(
        texts,
        source_lang="EN",
        target_lang="TH",
    )

    translated_segments = []
    for seg, result in zip(segments, results):
        translated_segments.append({
            "index": seg["index"],
            "start": seg["start"],
            "end": seg["end"],
            "text": result.text,
        })

    return translated_segments
