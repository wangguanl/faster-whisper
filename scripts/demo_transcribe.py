"""Demo transcription for local verification (wanggang-run-oss)."""

from __future__ import annotations

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="faster-whisper demo transcription")
    parser.add_argument("--model", default="large-v3")
    parser.add_argument("--audio", required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--compute-type", default="float16")
    parser.add_argument("--beam-size", type=int, default=5)
    args = parser.parse_args()

    from faster_whisper import WhisperModel

    print(
        f"Loading WhisperModel({args.model!r}, device={args.device!r}, "
        f"compute_type={args.compute_type!r}) ..."
    )
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    segments, info = model.transcribe(args.audio, beam_size=args.beam_size)
    print(
        f"Detected language {info.language!r} "
        f"with probability {info.language_probability:.4f}"
    )
    count = 0
    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        count += 1
    print(f"Done. segments={count}")
    return 0 if count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
