import type { CalculateMetadataFunction } from "remotion";
import type { VideoSpec } from "./types";
import { FPS } from "./constants";

const DEFAULT_SLIDE_DURATION_MS = 5000;

export const calculateMetadata: CalculateMetadataFunction<VideoSpec> = async ({
  props,
}) => {
  const { slides, intro, outro, settings } = props;

  const slideDurations = slides.map(
    (slide) => (slide.duration_ms ?? DEFAULT_SLIDE_DURATION_MS) / 1000
  );

  const totalSlideFrames = slideDurations.reduce(
    (sum, dur) => sum + Math.ceil(dur * FPS),
    0
  );

  const introFrames = Math.ceil(intro.duration_seconds * FPS);
  const outroFrames = Math.ceil(outro.duration_seconds * FPS);
  const transitionOverlap =
    (slides.length + 1) * settings.transition_duration_frames;

  const totalFrames = Math.max(
    introFrames + totalSlideFrames + outroFrames - transitionOverlap,
    FPS
  );

  return {
    durationInFrames: totalFrames,
    fps: FPS,
    width: settings.width,
    height: settings.height,
    props,
  };
};
