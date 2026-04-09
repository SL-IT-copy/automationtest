import { useMemo } from "react";
import type { CaptionWord } from "../types";
import { CAPTION_SWITCH_MS } from "../constants";

export interface CaptionPage {
  startMs: number;
  endMs: number;
  tokens: CaptionWord[];
}

const MAX_TOKENS_PER_PAGE = 6;
const MAX_CHARS_PER_PAGE = 28;

export const useCaptionPages = (captions: CaptionWord[]) => {
  return useMemo(() => {
    if (captions.length === 0) {
      return { pages: [] as CaptionPage[] };
    }

    const pages: CaptionPage[] = [];
    let currentTokens: CaptionWord[] = [];

    const flush = () => {
      if (currentTokens.length === 0) {
        return;
      }

      pages.push({
        startMs: currentTokens[0].startMs,
        endMs: currentTokens[currentTokens.length - 1].endMs,
        tokens: currentTokens,
      });
      currentTokens = [];
    };

    for (const token of captions) {
      if (currentTokens.length === 0) {
        currentTokens.push(token);
        continue;
      }

      const previous = currentTokens[currentTokens.length - 1];
      const gapMs = token.startMs - previous.endMs;
      const charCount = currentTokens.reduce(
        (sum, item) => sum + item.text.trim().length,
        token.text.trim().length
      );

      const shouldStartNewPage =
        gapMs > CAPTION_SWITCH_MS ||
        currentTokens.length >= MAX_TOKENS_PER_PAGE ||
        charCount > MAX_CHARS_PER_PAGE;

      if (shouldStartNewPage) {
        flush();
      }

      currentTokens.push(token);
    }

    flush();

    return { pages };
  }, [captions]);
};
