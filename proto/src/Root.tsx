import React from 'react';
import {Composition} from 'remotion';
import {Scene} from './Scene';

export const FPS = 30;
export const DURATION = Math.round(23.6 * FPS);

export const Root: React.FC = () => (
  <Composition id="EastIndia" component={Scene} durationInFrames={DURATION} fps={FPS} width={1920} height={1080} />
);
