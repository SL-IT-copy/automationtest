import React from "react";
import { AbsoluteFill, Series, staticFile } from "remotion";
import { Audio } from "@remotion/media";
import type { VideoSpec, Theme } from "../types";
import { FPS } from "../constants";
import { IntroSequence } from "../components/IntroSequence";
import { SlideScene } from "../components/SlideScene";
import { OutroSequence } from "../components/OutroSequence";
import "../load-font";

const THEMES: Record<string, Theme> = {
  dark: {
    background_gradient: ["#0a0a0a", "#1a1a2e"],
    text_color: "#FFFFFF",
    accent_color: "#39E508",
    caption_highlight_color: "#39E508",
    caption_base_color: "#FFFFFF",
    slide_number_color: "#666666",
    font_family: "Pretendard Variable",
    intro_bg: "#000000",
    outro_bg: "#0a0a0a",
  },
  midnight_blue: {
    background_gradient: ["#0f0c29", "#302b63"],
    text_color: "#E0E0FF",
    accent_color: "#00D4FF",
    caption_highlight_color: "#00D4FF",
    caption_base_color: "#E0E0FF",
    slide_number_color: "#4a4a7a",
    font_family: "Pretendard Variable",
    intro_bg: "#0f0c29",
    outro_bg: "#0f0c29",
  },
};

const DEFAULT_SLIDE_DURATION_MS = 5000;

export const ThreadVideo: React.FC<VideoSpec> = (props) => {
  const { slides, intro, outro, settings, id } = props;
  const theme = THEMES[settings.theme] ?? THEMES.dark;
  const introFrames = Math.ceil(intro.duration_seconds * FPS);
  const outroFrames = Math.ceil(outro.duration_seconds * FPS);

  return (
    <AbsoluteFill style={{ backgroundColor: theme.background_gradient[0] }}>
      <Audio
        src={staticFile(`audio/music/${settings.background_music}`)}
        volume={settings.background_music_volume}
        loop
      />
      <Series>
        <Series.Sequence durationInFrames={introFrames}>
          <IntroSequence
            handle={intro.handle}
            logoText={intro.logo_text}
            theme={theme}
          />
        </Series.Sequence>
        {slides.map((slide) => {
          const durationMs = slide.duration_ms ?? DEFAULT_SLIDE_DURATION_MS;
          const durationFrames = Math.ceil((durationMs / 1000) * FPS);

          return (
            <Series.Sequence
              key={`slide-${slide.slide_number}`}
              durationInFrames={durationFrames}
            >
              <SlideScene
                slide={slide}
                theme={theme}
                audioBasePath={`audio/${id}`}
              />
            </Series.Sequence>
          );
        })}
        <Series.Sequence durationInFrames={outroFrames}>
          <OutroSequence
            ctaText={outro.cta_text}
            handle={outro.handle}
            theme={theme}
          />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};
