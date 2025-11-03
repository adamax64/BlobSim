import { JSX } from 'react';
import { Crown } from './Crown';

type BlobBaseProps = {
  size: number;
  color: string;
  doSquash: boolean;
  hasCrown: boolean;
  eyeSlot: JSX.Element;
};

export const BlobBase = ({ size, color, eyeSlot, doSquash, hasCrown }: BlobBaseProps) => {
  return (
    <svg width={size} height={size} viewBox="0 0 130 95" version="1.1" id="svg5" xmlns="http://www.w3.org/2000/svg">
      <g id="layer1">
        <g id="g12632">
          <g id="scaleGroup" style={{ transformBox: 'fill-box', transformOrigin: '0% 100%' }}>
            {doSquash && (
              <animateTransform
                attributeName="transform"
                type="scale"
                values="1 1.02; 1 0.96; 1 1.02"
                dur="3s"
                repeatCount="indefinite"
              />
            )}
            <path
              id="path56"
              fill={color}
              stroke="#000000"
              strokeWidth={1}
              d="m 129.5089,59.689952 c 0,27.20034 -28.7716,34.818936 -64.263171,34.818937 -35.491565,0 -64.7546185,-7.618596 -64.7546185,-34.818937 C 0.49111025,32.48961 29.754163,0.4911092 65.245729,0.49110935 100.7373,0.49111061 129.5089,32.489611 129.5089,59.689952 Z"
            />
            {eyeSlot}
          </g>

          {/* Crown is a sibling of the scaled group so it won't be scaled.
              We animate a translate that matches the vertical displacement caused
              by the scale animation so the crown moves with the blob but keeps its size.

              Calculation notes (viewBox y range 0..95, crown reference y ~ 8):
              dy = (sy - 1) * (yc - y_origin).
              For sy: 1.02 -> dy = -1.74, 0.96 -> dy = 3.48, back to -1.74.
          */}
          {hasCrown && (
            <g id="crownGroup">
              {doSquash && (
                <animateTransform
                  attributeName="transform"
                  type="translate"
                  values="0 -1.74; 0 3.48; 0 -1.74"
                  dur="3s"
                  repeatCount="indefinite"
                />
              )}
              <Crown />
            </g>
          )}
        </g>
      </g>
    </svg>
  );
};
