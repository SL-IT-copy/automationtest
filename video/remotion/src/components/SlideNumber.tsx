import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import type { Theme } from "../types";
import { SLIDE_NUMBER_FONT_SIZE } from "../constants";
import { PRETENDARD_FONT_FAMILY } from "../load-font";

export const SlideNumber: React.FC<{
  current: number;
  total: number;
  theme: Theme;
}> = ({ current, total, theme }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 60,
        right: 60,
        fontSize: SLIDE_NUMBER_FONT_SIZE - 2,
        fontFamily: PRETENDARD_FONT_FAMILY,
        fontVariantNumeric: "tabular-nums",
        color: theme.slide_number_color,
        opacity,
        fontWeight: 700,
        letterSpacing: "0.05em",
        padding: "10px 16px",
        borderRadius: 999,
        border: "1px solid rgba(255,255,255,0.08)",
        background: "rgba(255,255,255,0.04)",
        backdropFilter: "blur(8px)",
      }}
    >
      {current}/{total}
    </div>
  );
};
