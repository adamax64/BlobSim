export interface BlobIconProps {
  size: number;
  color: string;
}

export function DeadBlobIcon({ size, color }: BlobIconProps) {
  return (
    <svg width={size} height={size} viewBox="0 0 130 95" version="1.1" id="svg5" xmlns="http://www.w3.org/2000/svg">
      <g id="layer1">
        <g id="g12632">
          <path
            id="path56"
            fill={color}
            stroke="#000000"
            strokeWidth={1}
            d="m 129.5089,59.689952 c 0,27.20034 -28.7716,34.818936 -64.263171,34.818937 -35.491565,0 -64.7546185,-7.618596 -64.7546185,-34.818937 C 0.49111025,32.48961 29.754163,0.4911092 65.245729,0.49110935 100.7373,0.49111061 129.5089,32.489611 129.5089,59.689952 Z"
          />
          <path
            fill="none"
            stroke="#000000"
            strokeWidth="1px"
            strokeLinecap="butt"
            strokeLinejoin="miter"
            strokeOpacity="1"
            d="M 38,28 52,42"
            id="path1039"
          />
          <path
            fill="none"
            stroke="#000000"
            strokeWidth="1px"
            strokeLinecap="butt"
            strokeLinejoin="miter"
            strokeOpacity="1"
            d="M 38,42 52,28"
            id="path1039-7"
          />
          <path
            fill="none"
            stroke="#000000"
            strokeWidth="1px"
            strokeLinecap="butt"
            strokeLinejoin="miter"
            strokeOpacity="1"
            d="M 78,28 92,42"
            id="path1039-6"
          />
          <path
            fill="none"
            stroke="#000000"
            strokeWidth="1px"
            strokeLinecap="butt"
            strokeLinejoin="miter"
            strokeOpacity="1"
            d="M 78,42 92,28"
            id="path1039-6-2"
          />
        </g>
      </g>
    </svg>
  );
}
