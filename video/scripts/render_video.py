import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEO_DIR = PROJECT_ROOT / "video"
REMOTION_DIR = VIDEO_DIR / "remotion"


def run_step(label: str, cmd: list[str], cwd: Optional[Path] = None):
    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"{'=' * 60}\n")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"\nFailed at step: {label}")
        sys.exit(result.returncode)


def render_pipeline(
    input_path: str,
    theme: str = "dark",
    voice_id: Optional[str] = None,
    output_dir: Optional[str] = None,
    skip_tts: bool = False,
):
    input_file = Path(input_path).resolve()
    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        sys.exit(1)

    scripts_dir = VIDEO_DIR / "scripts"

    spec_cmd = [
        sys.executable,
        str(scripts_dir / "slide_to_spec.py"),
        str(input_file),
        "--theme",
        theme,
    ]
    if output_dir:
        spec_cmd.extend(["--output-dir", output_dir])

    run_step("1/4  Generating video spec from thread...", spec_cmd)

    detected_output = VIDEO_DIR / "output"
    spec_dirs = sorted(detected_output.iterdir()) if detected_output.exists() else []
    if not spec_dirs:
        print("No output directory found after spec generation.")
        sys.exit(1)

    latest_dir = spec_dirs[-1]
    spec_path = latest_dir / "video_spec.json"

    if not skip_tts:
        tts_cmd = [
            sys.executable,
            str(scripts_dir / "generate_tts.py"),
            str(spec_path),
        ]
        if voice_id:
            tts_cmd.extend(["--voice-id", voice_id])

        run_step("2/4  Generating TTS audio + captions...", tts_cmd)

    output_mp4 = latest_dir / "final.mp4"
    render_cmd = [
        "npx",
        "remotion",
        "render",
        "ThreadVideo",
        f"--props={spec_path}",
        f"--output={output_mp4}",
        "--codec=h264",
        "--image-format=jpeg",
        "--concurrency=50%",
    ]

    run_step("3/4  Rendering video with Remotion...", render_cmd, cwd=REMOTION_DIR)

    print(f"\n{'=' * 60}")
    print(f"  4/4  Done!")
    print(f"{'=' * 60}")
    print(f"\n  Video: {output_mp4}")
    print(f"  Spec:  {spec_path}")
    print(
        f"\n  To upload: python {scripts_dir / 'youtube_upload.py'} {spec_path} {output_mp4}"
    )


def main():
    parser = argparse.ArgumentParser(description="Full thread-to-video pipeline")
    parser.add_argument("input_path", help="Path to published thread (.json or .md)")
    parser.add_argument("--theme", default="dark", help="Visual theme (default: dark)")
    parser.add_argument("--voice-id", default=None, help="ElevenLabs voice ID")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    parser.add_argument(
        "--skip-tts",
        action="store_true",
        help="Skip TTS generation (use existing audio)",
    )
    args = parser.parse_args()

    render_pipeline(
        input_path=args.input_path,
        theme=args.theme,
        voice_id=args.voice_id,
        output_dir=args.output_dir,
        skip_tts=args.skip_tts,
    )


if __name__ == "__main__":
    main()
