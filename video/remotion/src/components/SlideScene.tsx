import React from "react";
import { AbsoluteFill, staticFile } from "remotion";
import { Audio } from "@remotion/media";
import type { SlideData, Theme } from "../types";
import { SlideBackground } from "./SlideBackground";
import { SlideNumber } from "./SlideNumber";
import { SlideText } from "./SlideText";

export const SlideScene: React.FC<{
  slide: SlideData;
  theme: Theme;
  audioBasePath: string;
}> = ({ slide, theme, audioBasePath }) => {
  return (
    <AbsoluteFill>
      <SlideBackground theme={theme} overrideTheme={slide.theme_override} />
      <SlideNumber
        current={slide.slide_number}
        total={slide.total_slides}
        theme={theme}
      />
      <SlideText text={slide.text} theme={theme} />
      <Audio src={staticFile(`${audioBasePath}/${slide.audio_file}`)} />
    </AbsoluteFill>
  );
};
