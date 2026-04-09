import { z } from "zod";

// ── Zod Schemas (for Remotion prop validation) ──────────────────

export const ThemeSchema = z.object({
  background_gradient: z.tuple([z.string(), z.string()]),
  text_color: z.string(),
  accent_color: z.string(),
  caption_highlight_color: z.string(),
  caption_base_color: z.string(),
  slide_number_color: z.string(),
  font_family: z.string(),
  intro_bg: z.string(),
  outro_bg: z.string(),
});

export const SlideDataSchema = z.object({
  slide_number: z.number().int().min(1),
  total_slides: z.number().int().min(1),
  text: z.string(),
  audio_file: z.string(),
  captions_file: z.string(),
  duration_ms: z.number().nullable(),
  theme_override: z.string().nullable(),
});

export const VideoSpecSchema = z.object({
  id: z.string(),
  title: z.string(),
  created_at: z.string(),
  settings: z.object({
    width: z.number().int().default(1080),
    height: z.number().int().default(1920),
    fps: z.number().int().default(30),
    theme: z.string().default("dark"),
    background_music: z.string(),
    background_music_volume: z.number().min(0).max(1).default(0.08),
    transition_duration_frames: z.number().int().default(15),
  }),
  intro: z.object({
    duration_seconds: z.number(),
    handle: z.string(),
    logo_text: z.string(),
  }),
  outro: z.object({
    duration_seconds: z.number(),
    cta_text: z.string(),
    handle: z.string(),
  }),
  slides: z.array(SlideDataSchema).min(1),
  youtube: z.object({
    title: z.string().max(100),
    description: z.string().max(5000),
    tags: z.array(z.string()),
    category_id: z.string().default("28"),
    default_language: z.string().default("ko"),
    playlist_id: z.string().nullable(),
    contains_synthetic_media: z.boolean().default(true),
  }),
});

// ── TypeScript Types (inferred from Zod) ────────────────────────

export type Theme = z.infer<typeof ThemeSchema>;
export type SlideData = z.infer<typeof SlideDataSchema>;
export type VideoSpec = z.infer<typeof VideoSpecSchema>;

// ── Caption Types (matches @remotion/captions Caption type) ─────

export interface CaptionWord {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
}
