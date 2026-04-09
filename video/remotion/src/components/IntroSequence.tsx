import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import type { Theme } from "../types";
import { PRETENDARD_FONT_FAMILY } from "../load-font";

export const IntroSequence: React.FC<{
  handle: string;
  logoText: string;
  theme: Theme;
}> = ({ handle, logoText, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoScale = spring({ frame, fps, config: { damping: 12, mass: 0.8, stiffness: 200 } });
  const handleOpacity = interpolate(frame, [5, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.intro_bg,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          fontSize: 72,
          fontFamily: PRETENDARD_FONT_FAMILY,
          fontWeight: 800,
          color: theme.text_color,
          transform: `scale(${logoScale})`,
          letterSpacing: "-0.02em",
        }}
      >
        {logoText}
      </div>
      <div
        style={{
          fontSize: 28,
          fontFamily: PRETENDARD_FONT_FAMILY,
          fontWeight: 400,
          color: theme.accent_color,
          opacity: handleOpacity,
          marginTop: 12,
          letterSpacing: "0.02em",
        }}
      >
        {handle}
      </div>
    </AbsoluteFill>
  );
};
