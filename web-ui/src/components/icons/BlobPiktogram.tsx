import { BlobIconProps } from "./BlobIcon";

export function BlobPiktogram({ size, color }: BlobIconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 130 95"
      version="1.1"
      id="svg5">
      <defs
        id="defs2" />
      <g
        id="layer1">
        <g
          id="g12632">
          <path
            id="path56"
            fill={color}
            fillOpacity="1"
            fillRule="nonzero"
            stroke={color}
            strokeWidth="0.982221"
            d="m 129.5089,59.689952 c 0,27.20034 -28.7716,34.818936 -64.263171,34.818937 -35.491565,0 -64.7546185,-7.618596 -64.7546185,-34.818937 C 0.49111025,32.48961 29.754163,0.4911092 65.245729,0.49110935 100.7373,0.49111061 129.5089,32.489611 129.5089,59.689952 Z" />
          <ellipse
            fill="#ffffff"
            fillOpacity="1"
            stroke="#ffffff"
            strokeWidth="5"
            strokeMiterlimit="4"
            strokeDasharray="none"
            strokeOpacity="1"
            id="path2446"
            cx="45"
            cy="35"
            rx="4.4549451"
            ry="9.4549446" />
          <ellipse
            fill="#ffffff"
            fillOpacity="1"
            stroke="#ffffff"
            strokeWidth="5"
            strokeMiterlimit="4"
            strokeDasharray="none"
            strokeOpacity="1"
            id="path2446-7"
            cx="85"
            cy="35"
            rx="4.4549451"
            ry="9.4549446" />
        </g>
      </g>
    </svg>
  );
}