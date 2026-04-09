import React from "react";
import { AbsoluteFill } from "remotion";
import type { Theme } from "../types";
import { SLIDE_PADDING } from "../constants";
import { PRETENDARD_FONT_FAMILY } from "../load-font";

export const SlideText: React.FC<{
  text: string;
  theme: Theme;
}> = ({ text, theme }) => {
  const lines = text.split("\n").filter((l) => l.trim() !== "");

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: SLIDE_PADDING,
      }}
    >
      <div
        style={{
          maxWidth: 780,
          textAlign: "center",
          padding: "44px 40px",
          borderRadius: 32,
          background: "rgba(17, 19, 27, 0.92)",
          border: "1px solid rgba(255,255,255,0.08)",
          boxShadow: "0 24px 70px rgba(0,0,0,0.28)",
        }}
      >
        {lines.map((line, i) => {
          return (
            <p
              key={`${i}-${line.slice(0, 8)}`}
              style={{
                fontSize: 36,
                color: theme.text_color,
                fontFamily: PRETENDARD_FONT_FAMILY,
                fontWeight: 700,
                lineHeight: 1.68,
                margin: "4px 0",
                letterSpacing: "-0.02em",
              }}
            >
              {line}
            </p>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
