# Thread-to-Video Pipeline: Implementation Plan

**Created**: 2026-04-06
**Status**: Reviewed (self-review complete, 5 issues fixed)
**Architecture Decision**: Python orchestrator + Remotion renderer (hybrid)

---

## 0. Executive Summary

**Input**: An approved 7-slide Korean thread (JSON from existing pipeline per `thread_run_output.json`, or manually created `.md`)
**Output**: A 9:16 (1080x1920) YouTube-ready MP4 video, ~2-3 minutes, with TTS narration and TikTok-style word-highlighting captions.

**Confirmed Stack**:
- **TTS**: ElevenLabs Creator ($22/mo, 100min, Multilingual v2, word-level timestamps, Voice Cloning)
- **Video Rendering**: Remotion (React/TypeScript) - local rendering for MVP, Lambda later
- **Subtitles**: ElevenLabs word-level alignment -> `@remotion/captions` TikTok-style word highlighting
- **Orchestration**: Python scripts (existing pipeline extended)
- **Upload**: YouTube Data API v3 (OAuth 2.0, private-first, human approval)
- **Format**: 9:16 vertical (1080x1920), ~2-3 minutes per video

**Data Flow**:
```
published .md -> [slide_to_spec.py] -> video_spec.json
                 [generate_tts.py]  -> per-slide .mp3 + captions.json
                 [Remotion render]  -> final .mp4
                 [human review]
                 [youtube_upload.py] -> YouTube (private -> public)
```

---

## 1. Directory & File Structure

```
threadautomationplan/
|-- (existing files unchanged)
|
|-- video/                              # NEW - all video pipeline code
|   |-- remotion/                       # Remotion project root
|   |   |-- package.json                # Node dependencies
|   |   |-- tsconfig.json               # TypeScript config
|   |   |-- remotion.config.ts          # Remotion bundle config
|   |   |-- public/                     # Static assets served by Remotion
|   |   |   |-- fonts/                  # Korean fonts
|   |   |   |   |-- PretendardVariable.woff2
|   |   |   |-- audio/                  # Generated TTS (written by Python)
|   |   |       |-- (per-run dirs)
|   |   |-- src/
|   |   |   |-- Root.tsx                # Remotion <Composition> registration
|   |   |   |-- index.ts                # Entry point for remotion bundle
|   |   |   |-- types.ts                # Shared TypeScript types
|   |   |   |-- constants.ts            # FPS, WIDTH, HEIGHT, colors, timing
|   |   |   |-- load-font.ts            # Font loading (Pretendard)
|   |   |   |-- calculate-metadata.ts   # Dynamic duration from audio files
|   |   |   |-- compositions/
|   |   |   |   |-- ThreadVideo.tsx      # Main composition (top-level orchestrator)
|   |   |   |-- components/
|   |   |   |   |-- IntroSequence.tsx    # Logo + handle entrance animation
|   |   |   |   |-- SlideScene.tsx       # Single slide: bg + number + text + audio + captions
|   |   |   |   |-- SlideBackground.tsx  # Gradient/solid per-slide background
|   |   |   |   |-- SlideNumber.tsx      # "1/7" indicator
|   |   |   |   |-- SlideText.tsx        # Korean text with line-by-line fade animation
|   |   |   |   |-- CaptionOverlay.tsx   # TikTok-style word-by-word highlight
|   |   |   |   |-- OutroSequence.tsx    # CTA + follow prompt
|   |   |   |-- hooks/
|   |   |       |-- useCaptionPages.ts   # createTikTokStyleCaptions wrapper
|   |   |-- test/
|   |       |-- types.test.ts            # Schema validation tests
|   |       |-- calculate-metadata.test.ts
|   |
|   |-- scripts/                        # Python scripts for pipeline
|   |   |-- slide_to_spec.py            # .md -> video_spec.json
|   |   |-- generate_tts.py             # ElevenLabs TTS + alignment -> .mp3 + captions.json
|   |   |-- youtube_upload.py           # YouTube Data API v3 upload
|   |   |-- render_video.py             # Orchestrates full pipeline
|   |   |-- utils/
|   |       |-- __init__.py
|   |       |-- elevenlabs_client.py    # ElevenLabs API wrapper with retry
|   |       |-- alignment_converter.py  # Character alignment -> word-level Caption[]
|   |       |-- youtube_auth.py         # OAuth 2.0 + refresh token management
|   |       |-- spec_validator.py       # Validates video_spec.json against schema
|   |
|   |-- schemas/
|   |   |-- video_spec.schema.json      # JSON Schema for video_spec.json
|   |
|   |-- output/                         # Rendered videos (gitignored)
|   |
|   |-- fixtures/                       # Test fixtures
|   |   |-- sample_video_spec.json
|   |   |-- sample_captions.json
|   |   |-- sample_slide.md
|   |
|   |-- config/
|       |-- themes.json                 # Visual theme presets
|       |-- music/                      # Background music tracks (gitignored)
```

---

## 2. JSON Schema Specifications

### 2.1 `video_spec.json` - The Contract Between Python and Remotion

```json
{
  "id": "2026-04-06__perplexity-incognito-sham",
  "title": "Perplexity incognito mode was a sham",
  "created_at": "2026-04-06T14:30:00+09:00",

  "settings": {
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "theme": "dark",
    "background_music": "ambient_loop.mp3",
    "background_music_volume": 0.08,
    "transition_duration_frames": 15
  },

  "intro": {
    "duration_seconds": 0.5,
    "handle": "@jisang0914",
    "logo_text": "JSup"
  },

  "outro": {
    "duration_seconds": 2.0,
    "cta_text": "AI follow CTA text here",
    "handle": "@jisang0914"
  },

  "slides": [
    {
      "slide_number": 1,
      "total_slides": 7,
      "text": "Slide text content here",
      "audio_file": "slide_01.mp3",
      "captions_file": "slide_01_captions.json",
      "duration_ms": null,
      "theme_override": null
    }
  ],

  "youtube": {
    "title": "YouTube title | AI news",
    "description": "Description with sources",
    "tags": ["AI", "tech"],
    "category_id": "28",
    "default_language": "ko",
    "playlist_id": null,
    "contains_synthetic_media": true
  }
}
```

### 2.2 `slide_NN_captions.json` - Per-Slide Caption Format

Follows `@remotion/captions` `Caption[]` type exactly:

```json
[
  {
    "text": "Perplexity",
    "startMs": 0,
    "endMs": 620,
    "timestampMs": 310,
    "confidence": null
  },
  {
    "text": " mode",
    "startMs": 620,
    "endMs": 1040,
    "timestampMs": 830,
    "confidence": null
  }
]
```

### 2.3 `themes.json` - Visual Theme Presets

```json
{
  "dark": {
    "background_gradient": ["#0a0a0a", "#1a1a2e"],
    "text_color": "#FFFFFF",
    "accent_color": "#39E508",
    "caption_highlight_color": "#39E508",
    "caption_base_color": "#FFFFFF",
    "slide_number_color": "#666666",
    "font_family": "Pretendard Variable",
    "intro_bg": "#000000",
    "outro_bg": "#0a0a0a"
  },
  "midnight_blue": {
    "background_gradient": ["#0f0c29", "#302b63"],
    "text_color": "#E0E0FF",
    "accent_color": "#00D4FF",
    "caption_highlight_color": "#00D4FF",
    "caption_base_color": "#E0E0FF",
    "slide_number_color": "#4a4a7a",
    "font_family": "Pretendard Variable",
    "intro_bg": "#0f0c29",
    "outro_bg": "#0f0c29"
  }
}
```

---

## 3. Per-File Implementation Specs

### 3.1 Python Scripts

#### `slide_to_spec.py`

- **Input**: Path to thread output (JSON from existing pipeline per `thread_run_output.json` schema, OR plain markdown if manually created). Auto-detects format by extension.
- **Output**: `video/output/{id}/video_spec.json`
- **Dependencies**: `spec_validator.py`, `themes.json`
- **Key Logic**:
  1. Auto-detect input format (.json or .md)
  2. For JSON: extract slides from `thread_run_output.json` `slides` array (each has `slide_number`, `text`, `source_url`)
  3. For MD: parse fenced blocks as fallback
  4. Extract source_footer from last slide (URL line)
  5. Extract follow_cta from last slide
  6. Generate YouTube metadata (title from slide 1 hook, description with sources, tags from topic)
  7. Build video_spec.json with placeholder audio fields
  8. Validate against JSON schema
  9. Create output directory
- **Error Handling**: Abort if < 2 slides, warn if slide > 500 chars
- **Functions**: `parse_thread_json()`, `parse_published_markdown()`, `build_video_spec()`, `main()`
- **Note**: `content/published/` is currently empty. Actual published format TBD - support both JSON and MD for flexibility.

#### `generate_tts.py`

- **Input**: `video/output/{id}/video_spec.json`
- **Output**: Per-slide `.mp3` + `_captions.json`, updated spec with `duration_ms`
- **Dependencies**: `elevenlabs_client.py`, `alignment_converter.py`
- **Key Logic**:
  1. Load spec, iterate slides
  2. Call ElevenLabs `POST /v1/text-to-speech/{voice_id}/with-timestamps`
     - `model_id`: `"eleven_multilingual_v2"`
     - `language_code`: `"ko"` (forces Korean text normalization)
     - `apply_language_text_normalization`: `true`
     - `voice_settings`: `{ stability: 0.55, similarity_boost: 0.75, speed: 0.9 }`
  3. Decode `audio_base64` -> write `.mp3`
  4. Convert `normalized_alignment` (not `alignment`) to word-level `Caption[]`
  5. Write captions JSON
  6. Measure audio duration -> update spec `duration_ms`
  7. Copy audio to `video/remotion/public/audio/{id}/`
- **Error Handling**: Retry 3x with exponential backoff, skip on permanent failure
- **Functions**: `generate_slide_tts()`, `process_all_slides()`, `main()`

#### `elevenlabs_client.py`

```python
def tts_with_timestamps(
    text: str,
    voice_id: str,
    api_key: str,
    model_id: str = "eleven_multilingual_v2",
    stability: float = 0.55,
    similarity_boost: float = 0.75,
    speed: float = 0.9,
    language_code: str = "ko",
) -> tuple[bytes, dict]:
    """
    POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps
    Returns: (decoded_audio_bytes, normalized_alignment_dict)
    """
```

- Error handling: HTTP 429 -> exponential backoff, HTTP 401 -> raise immediately, HTTP 400 -> log text

#### `alignment_converter.py`

- Converts ElevenLabs character-level alignment to word-level `Caption[]`
- Algorithm: iterate chars, accumulate into words, flush on space/newline
- Convert seconds -> milliseconds
- Set `timestampMs` = midpoint of word
- Use `normalized_alignment` when `apply_language_text_normalization=true`

#### `youtube_upload.py`

- **Input**: `video_spec.json` + rendered `.mp4`
- **Output**: YouTube video ID
- **Key Logic**:
  1. OAuth 2.0 auth via `youtube_auth.py`
  2. Build request from spec `youtube` section
  3. Always set `privacyStatus: "private"`, `containsSyntheticMedia: true`
  4. Resumable upload with retry
  5. Optional: custom thumbnail, playlist assignment
- **Functions**: `upload_video()`, `set_thumbnail()`, `add_to_playlist()`, `make_public()`

#### `youtube_auth.py`

- OAuth 2.0 flow + refresh token persistence
- Scopes: `youtube.upload`, `youtube`
- One-time browser auth -> save `token.json` -> auto-refresh

#### `render_video.py` - Full Pipeline Orchestrator

```python
def render_pipeline(md_path: str, theme: str = "dark", voice_id: str = None):
    """
    1. slide_to_spec.py -> video_spec.json
    2. generate_tts.py  -> per-slide .mp3 + captions.json + updated spec
    3. npx remotion render ThreadVideo \
         --props=video/output/{id}/video_spec.json \
         --output=video/output/{id}/final.mp4 \
         --codec=h264 --image-format=jpeg --concurrency=50%
    4. Print output path + prompt for YouTube upload
    """
```

### 3.2 Remotion Components

#### TypeScript Types (`types.ts`)

```typescript
interface VideoSpec {
  id: string;
  title: string;
  created_at: string;
  settings: VideoSettings;
  intro: IntroConfig;
  outro: OutroConfig;
  slides: SlideData[];
  youtube: YouTubeMetadata;
}

interface VideoSettings {
  width: number;       // 1080
  height: number;      // 1920
  fps: number;         // 30
  theme: string;
  background_music: string;
  background_music_volume: number;
  transition_duration_frames: number;
}

interface SlideData {
  slide_number: number;
  total_slides: number;
  text: string;
  audio_file: string;
  captions_file: string;
  duration_ms: number | null;
  theme_override: string | null;
}

interface Theme {
  background_gradient: [string, string];
  text_color: string;
  accent_color: string;
  caption_highlight_color: string;
  caption_base_color: string;
  slide_number_color: string;
  font_family: string;
  intro_bg: string;
  outro_bg: string;
}
```

#### Constants (`constants.ts`)

```typescript
export const WIDTH = 1080;
export const HEIGHT = 1920;
export const FPS = 30;
export const INTRO_DURATION_SECONDS = 0.5;
export const OUTRO_DURATION_SECONDS = 2.0;
export const TRANSITION_DURATION_FRAMES = 15;
export const CAPTION_SWITCH_MS = 900;       // Korean speech density
export const CAPTION_MAX_CHARS_PER_LINE = 10; // Korean chars are wider
export const SLIDE_TEXT_FONT_SIZE = 42;
export const CAPTION_FONT_SIZE = 52;
export const SLIDE_NUMBER_FONT_SIZE = 28;
export const SLIDE_PADDING = 60;
```

#### `Root.tsx`

- Registers `ThreadVideo` composition with `calculateMetadata` for dynamic duration

#### `calculate-metadata.ts`

- Sums all slide `duration_ms` -> total frames
- Accounts for intro/outro duration
- Subtracts transition overlap (`(slides.length - 1) * transition_frames`)

#### `ThreadVideo.tsx` (Main Composition)

```
<AbsoluteFill>
  <Audio loop volume={bgmVolume} />   // Background music
  <TransitionSeries>
    <IntroSequence />
    <Transition fade />
    {slides.map(slide => (
      <>
        <SlideScene slide={slide} />
        <Transition fade />
      </>
    ))}
    <OutroSequence />
  </TransitionSeries>
</AbsoluteFill>
```

#### `SlideScene.tsx`

- Assembles: `SlideBackground` + `SlideNumber` + `SlideText` + `<Audio>` + `CaptionOverlay`
- Each slide is a self-contained unit

#### `SlideText.tsx`

- Korean text centered, line-by-line staggered fade-in
- Each line: 5-frame delay, 10-frame opacity 0->1, 15px translateY

#### `CaptionOverlay.tsx`

- Loads `slide_NN_captions.json` via `useDelayRender`
- `createTikTokStyleCaptions({ combineTokensWithinMilliseconds: 900 })`
- Renders pages as `<Sequence>` with word highlighting
- Active word = `caption_highlight_color`, inactive = `caption_base_color`

#### `IntroSequence.tsx`

- Black bg, `@jisang0914` scales 0->1 over 15 frames (spring), white text centered

#### `OutroSequence.tsx`

- CTA text fades in line-by-line, handle at bottom with subtle pulse

#### `SlideBackground.tsx`

- CSS linear-gradient from theme colors, optional per-slide override

#### `SlideNumber.tsx`

- Top-right corner, `"1/7"` format, muted color

---

## 4. Configuration

### Environment Variables (add to `config/.env.example`)

```bash
# NEW - ElevenLabs
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=your_voice_id_here

# NEW - YouTube
YOUTUBE_CLIENT_SECRET_PATH=config/youtube_client_secret.json
YOUTUBE_TOKEN_PATH=config/youtube_token.json
```

### Python Dependencies (add to `requirements.txt`)

```
mutagen>=1.47.0           # MP3 duration measurement
jsonschema>=4.20.0         # video_spec.json validation
google-api-python-client>=2.100.0
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.2.0
```

### Node Dependencies (`video/remotion/package.json`)

```json
{
  "dependencies": {
    "remotion": "^4.0.0",
    "@remotion/cli": "^4.0.0",
    "@remotion/captions": "^4.0.0",
    "@remotion/transitions": "^4.0.0",
    "@remotion/media": "^4.0.0",
    "@remotion/media-utils": "^4.0.0",
    "@remotion/layout-utils": "^4.0.0",
    "@remotion/fonts": "^4.0.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "zod": "^3.23.0"
  }
}
```

---

## 5. Parallel Task Graph

```
WAVE 0: SCAFFOLDING (all parallel)
  T0.1  Create video/ directory structure
  T0.2  Create video/remotion/ with package.json, tsconfig.json
  T0.3  Create video/schemas/video_spec.schema.json
  T0.4  Create video/config/themes.json
  T0.5  Update .gitignore
  T0.6  Update config/.env.example
  T0.7  Update requirements.txt
  T0.8  Create test fixtures

WAVE 1: CORE TYPES & UTILITIES (depends on Wave 0)
  T1.1  npm install in video/remotion/
  T1.2  Write src/types.ts + src/constants.ts
  T1.3  Write src/load-font.ts (Pretendard)
  T1.4  Write video/scripts/utils/__init__.py
  T1.5  Write video/scripts/utils/spec_validator.py

WAVE 2: PYTHON + REMOTION PARALLEL (depends on Wave 1)
  TRACK A (Python):
    T2.1  slide_to_spec.py
    T2.2  elevenlabs_client.py
    T2.3  alignment_converter.py
  TRACK B (Remotion):
    T2.4  Root.tsx
    T2.5  calculate-metadata.ts
    T2.6  SlideBackground.tsx
    T2.7  SlideNumber.tsx
    T2.8  SlideText.tsx

WAVE 3: INTEGRATION (depends on Wave 2)
  TRACK A (Python):
    T3.1  generate_tts.py (uses T2.2 + T2.3)
  TRACK B (Remotion):
    T3.3  useCaptionPages.ts hook
    T3.4  CaptionOverlay.tsx
    T3.5  IntroSequence.tsx
    T3.6  OutroSequence.tsx
  TRACK C (YouTube - independent):
    T3.7  youtube_auth.py
    T3.8  youtube_upload.py

WAVE 4: COMPOSITION (depends on Wave 3)
  T4.1  SlideScene.tsx (assembles all sub-components)
  T4.2  ThreadVideo.tsx (main composition with TransitionSeries)
  T4.3  render_video.py (full pipeline orchestrator)

WAVE 5: TESTING & POLISH (depends on Wave 4)
  T5.1  E2E test: real .md -> video_spec -> TTS -> MP4
  T5.2  Visual QA in Remotion Studio
  T5.3  YouTube upload dry-run (private)
  T5.4  Tune caption timing, font sizes, animation speeds
  T5.5  Add background music, test volume levels
```

**Critical Path**: T0.2 -> T1.1 -> T2.4 -> T3.4 -> T4.1 -> T4.2 -> T5.1

---

## 6. Atomic Commit Strategy (22 commits)

### Wave 0 (Day 1, first half)
- Commit 1: `feat(video): scaffold directory structure and configuration`
- Commit 2: `feat(video): add video_spec JSON schema and test fixtures`
- Commit 3: `feat(video): add visual theme presets`

### Wave 1 (Day 1, second half)
- Commit 4: `feat(video): initialize Remotion project with dependencies`
- Commit 5: `feat(video): add TypeScript types and constants`
- Commit 6: `feat(video): add Korean font loading (Pretendard)`
- Commit 7: `feat(video): add Python spec validator utility`

### Wave 2 (Day 2)
- Commit 8: `feat(video): add slide_to_spec.py parser`
- Commit 9: `feat(video): add ElevenLabs client with retry logic`
- Commit 10: `feat(video): add alignment converter (chars -> word captions)`
- Commit 11: `feat(video): add Remotion Root and calculateMetadata`
- Commit 12: `feat(video): add SlideBackground, SlideNumber, SlideText components`

### Wave 3 (Day 3)
- Commit 13: `feat(video): add generate_tts.py pipeline`
- Commit 14: `feat(video): add CaptionOverlay with TikTok-style word highlighting`
- Commit 15: `feat(video): add IntroSequence and OutroSequence`
- Commit 16: `feat(video): add YouTube auth and upload scripts`

### Wave 4 (Day 4)
- Commit 17: `feat(video): add SlideScene composition component`
- Commit 18: `feat(video): add ThreadVideo main composition`
- Commit 19: `feat(video): add render_video.py pipeline orchestrator`

### Wave 5 (Day 5)
- Commit 20: `test(video): add end-to-end integration test`
- Commit 21: `fix(video): tune caption timing, font sizes, animation parameters`
- Commit 22: `feat(video): add background music support`

---

## 7. Testing Strategy

### Unit Tests
| Test | What It Verifies | Framework |
|------|------------------|-----------|
| `test_parse_published_markdown` | Correct slide/metadata extraction from .md | pytest |
| `test_build_video_spec` | Generated spec matches JSON schema | pytest + jsonschema |
| `test_chars_to_word_captions` | Korean character alignment -> word captions | pytest |
| `test_chars_to_word_captions_edge` | Handles punctuation, empty strings | pytest |
| `test_spec_validator` | Rejects invalid specs | pytest |
| `test_types` | TypeScript types compile | `tsc --noEmit` |
| `test_calculate_metadata` | Correct frame count from durations | vitest |

### Integration Tests
| Test | What It Verifies |
|------|------------------|
| `test_slide_to_spec_real_file` | Parser works with real published .md |
| `test_elevenlabs_single_slide` | ElevenLabs API returns MP3 + alignment for Korean |
| `test_caption_roundtrip` | Alignment -> converter -> captions JSON -> loads in Remotion |
| `test_remotion_render` | `npx remotion render` completes with fixture data |
| `test_youtube_auth_flow` | OAuth token refresh works |

### Visual QA (Remotion Studio)
1. SlideText: Korean chars render, line breaks match, stagger animation smooth
2. CaptionOverlay: Words highlight in sync (< 200ms drift)
3. SlideScene: All layers composite without overlap
4. ThreadVideo: Transitions smooth, total duration matches audio
5. Intro/Outro: Readable on dark bg, animations complete in time

---

## 8. External Setup Checklist

| Task | Day | Blocks |
|------|-----|--------|
| Create Google Cloud project for YouTube API | Day 1 | YouTube upload |
| Configure OAuth consent screen + request verification | Day 1 | Production (2-4 weeks) |
| Generate OAuth `client_secret.json` | Day 1 | YouTube auth dev |
| Run OAuth flow once -> `token.json` | Day 1 | YouTube upload testing |
| Set up ElevenLabs voice (choose or clone) | Day 1 | TTS generation |
| Test ElevenLabs with Korean text sample | Day 1 | Quality validation |
| Download Pretendard font `.woff2` | Day 1 | Font rendering |
| Find/create ambient background music loop | Day 2 | Background audio |

---

## 9. Korean-Specific Constants (Research-Amended)

| Constant | Value | Rationale |
|----------|-------|-----------|
| TTS `speed` | `0.9` | Korean TTS runs fast; slightly slower = more natural |
| TTS `stability` | `0.55` | Higher stability for consistent Korean pronunciation |
| TTS `language_code` | `"ko"` | Forces Korean text normalization (numbers/dates in Korean) |
| `CAPTION_SWITCH_MS` | `900` | Korean speech is denser than English |
| Max subtitle chars | `10` per line | Korean characters are wider than Latin |
| Use `normalized_alignment` | when `apply_language_text_normalization=true` | Correct timestamps after number normalization |

---

## 10. Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Korean TTS quality from ElevenLabs | High | Test multiple voices + Multilingual v2 before committing |
| ElevenLabs char alignment accuracy for Korean | High | Test converter extensively with Korean morphology |
| Google app verification delay (2-4 weeks) | Medium | Use unverified app for own channel immediately |
| Remotion render time for 2-3 min video | Low | Local ~30-60s. Acceptable for 5/week |
| ElevenLabs 100 min/month quota | Medium | ~60 min/month estimated usage. Fits within 100 min |

---

## 11. Cost Analysis

### Per-Video Cost

| Component | Cost |
|-----------|------|
| ElevenLabs TTS (~2.5 min audio) | ~$0.55 (from $22/mo for 100min) |
| Remotion render (local) | $0 |
| YouTube API | $0 |
| **Total per video** | **~$0.55** |

### Monthly Cost (20 videos)

| Item | Cost |
|------|------|
| ElevenLabs Creator | $22 |
| Remotion license | $0 (personal) or $12.50/mo ($150/yr if commercial) |
| YouTube API | $0 |
| **Total monthly** | **$22 - $34.50** |

> **Remotion License Note**: Individual/personal use is free. If the YouTube channel generates revenue (ads, sponsorships), the Remotion Company License ($150/year) may be required. Check https://remotion.dev/license for current terms.

---

## 12. Definition of Done

The pipeline is "done" when:

1. `python video/scripts/render_video.py content/published/{slug}.md` produces a valid MP4
2. The MP4 plays correctly: intro -> 7 slides with synced audio + captions -> outro
3. Captions highlight words in sync with speech (< 200ms drift)
4. Korean text is readable and properly formatted
5. `python video/scripts/youtube_upload.py` successfully uploads as private
6. Human can review in YouTube Studio and change to public

---

## 13. Open Questions (Pre-Implementation)

1. **Voice choice**: Use existing ElevenLabs voice ID or create cloned voice?
2. **Background music**: Have an ambient loop track or need to source one?
