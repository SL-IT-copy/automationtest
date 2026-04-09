import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import type { Theme } from "../types";
import {
  SLIDE_TEXT_STAGGER_FRAMES,
  SLIDE_TEXT_FADE_FRAMES,
  SLIDE_PADDING,
  SLIDE_MAX_TEXT_WIDTH,
} from "../constants";
import { PRETENDARD_FONT_FAMILY } from "../load-font";

export const OutroSequence: React.FC<{
  ctaText: string;
  handle: string;
  theme: Theme;
}> = ({ ctaText, handle, theme }) => {
  const frame = useCurrentFrame();
  const lines = ctaText.split("\n").filter((l) => l.trim() !== "");

  const handlePulse = interpolate(
    frame % 30,
    [0, 15, 30],
    [0.7, 1, 0.7],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.outro_bg,
        justifyContent: "center",
        alignItems: "center",
        padding: SLIDE_PADDING,
      }}
    >
      <div style={{ maxWidth: SLIDE_MAX_TEXT_WIDTH, textAlign: "center" }}>
        {lines.map((line, i) => {
          const delay = i * SLIDE_TEXT_STAGGER_FRAMES;
          const opacity = interpolate(
            frame,
            [delay, delay + SLIDE_TEXT_FADE_FRAMES],
            [0, 1],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          );
          return (
            <p
              key={`outro-${i}`}
              style={{
                fontSize: 38,
                color: theme.text_color,
                fontFamily: PRETENDARD_FONT_FAMILY,
                fontWeight: 500,
                lineHeight: 1.8,
                margin: "6px 0",
                opacity,
              }}
            >
              {line}
            </p>
          );
        })}
      </div>

      <div
        style={{
          position: "absolute",
          bottom: 120,
          textAlign: "center",
        }}
      >
        <div
          style={{
            display: "inline-block",
            borderBottom: `3px solid ${theme.accent_color}`,
            paddingBottom: 6,
          }}
        >
          <span
            style={{
              fontSize: 32,
              fontFamily: PRETENDARD_FONT_FAMILY,
              fontWeight: 600,
              color: theme.accent_color,
              opacity: handlePulse,
            }}
          >
            {handle}
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
