import React, { useState, useEffect, useCallback } from "react";
import {
  AbsoluteFill,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  delayRender,
  continueRender,
  cancelRender,
  spring,
} from "remotion";
import type { Theme, CaptionWord } from "../types";
import { useCaptionPages, type CaptionPage as CaptionPageData } from "../hooks/useCaptionPages";

const CaptionPageView: React.FC<{
  page: CaptionPageData;
  theme: Theme;
  currentMs: number;
  frameFromPageStart: number;
  fps: number;
}> = ({ page, theme, currentMs, frameFromPageStart, fps }) => {
  const absoluteMs = currentMs;
  const activeTokenIndex = Math.max(
    0,
    page.tokens.findIndex((token) => token.startMs <= absoluteMs && token.endMs > absoluteMs)
  );
  const progress = page.tokens.length > 1 ? activeTokenIndex / (page.tokens.length - 1) : 1;

  const entrance = spring({
    frame: Math.max(0, frameFromPageStart),
    fps,
    config: { damping: 200 },
    durationInFrames: 5,
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 92,
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 0,
          textAlign: "center",
          opacity: entrance,
          transform: `scale(${0.95 + entrance * 0.05})`,
          padding: "10px 0",
        }}
      >
        <div
          style={{
            width: 220,
            height: 8,
            borderRadius: 999,
            background: "rgba(255,255,255,0.12)",
            overflow: "hidden",
            boxShadow: "0 8px 24px rgba(0,0,0,0.22)",
          }}
        >
          <div
            style={{
              width: `${Math.max(progress, 0.08) * 100}%`,
              height: "100%",
              background: theme.caption_highlight_color,
              borderRadius: 999,
            }}
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const CaptionOverlay: React.FC<{
  captionsFile: string;
  theme: Theme;
}> = ({ captionsFile, theme }) => {
  const [captions, setCaptions] = useState<CaptionWord[]>([]);
  const [handle] = useState(() => delayRender("Loading captions"));
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fetchCaptions = useCallback(async () => {
    try {
      const res = await fetch(staticFile(captionsFile));
      const data: CaptionWord[] = await res.json();
      setCaptions(data);
      continueRender(handle);
    } catch (err) {
      cancelRender(err);
    }
  }, [captionsFile, handle]);

  useEffect(() => {
    fetchCaptions();
  }, [fetchCaptions]);

  const { pages } = useCaptionPages(captions);

  const currentMs = (frame / fps) * 1000;
  const activePageIndex = pages.findIndex((page, index) => {
    const nextPage = pages[index + 1];
    return currentMs >= page.startMs && (!nextPage || currentMs < nextPage.startMs);
  });

  if (activePageIndex === -1) {
    return <AbsoluteFill />;
  }

  const activePage = pages[activePageIndex];
  const activePageStartFrame = Math.round((activePage.startMs / 1000) * fps);

  return (
    <AbsoluteFill>
      <CaptionPageView
        page={activePage}
        theme={theme}
        currentMs={currentMs}
        frameFromPageStart={frame - activePageStartFrame}
        fps={fps}
      />
    </AbsoluteFill>
  );
};
