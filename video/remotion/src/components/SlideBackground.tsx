import React from "react";
import { AbsoluteFill } from "remotion";
import type { Theme } from "../types";

const grainSvg = `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E")`;

export const SlideBackground: React.FC<{
  theme: Theme;
  overrideTheme?: string | null;
}> = ({ theme }) => {
  const [colorStart, colorEnd] = theme.background_gradient;

  return (
    <AbsoluteFill>
      <div
        style={{
          width: "100%",
          height: "100%",
          background: `linear-gradient(180deg, ${colorStart} 0%, ${colorEnd} 100%)`,
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 50% 20%, rgba(57,229,8,0.16), transparent 34%), radial-gradient(circle at 80% 78%, rgba(255,255,255,0.06), transparent 28%)",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: grainSvg,
          backgroundSize: "256px 256px",
          opacity: 0.03,
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
