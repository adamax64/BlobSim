import { SvgIcon, SvgIconProps } from '@mui/material';

const SunnyCloudy = (props: SvgIconProps) => {
  return (
    <SvgIcon {...props}>
      <svg focusable="false" aria-hidden="true" viewBox="0 0 24 24">
        {/* Sun rays, peeking out above/right of the cloud */}
        <path
          d="M17 3v-2"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          fill="none"
        />
        <path
          d="M17 3v-2"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          fill="none"
          transform="rotate(45 17 7.5)"
        />
        <path
          d="M17 3v-2"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          fill="none"
          transform="rotate(90 17 7.5)"
        />
        <path
          d="M17 3v-2"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          fill="none"
          transform="rotate(135 17 7.5)"
        />
        <path
          d="M17 3v-2"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          fill="none"
          transform="rotate(180 17 7.5)"
        />
        <path
          d="M17 3v-2"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          fill="none"
          transform="rotate(225 17 7.5)"
        />
        <path
          d="M17 3v-2"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          fill="none"
          transform="rotate(270 17 7.5)"
        />
        <path
          d="M17 3v-2"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          fill="none"
          transform="rotate(315 17 7.5)"
        />
        {/* Sun disc, partially occluded by the cloud in front of it */}
        <circle cx="17" cy="7.5" r="3.2" fill="currentColor" />
        {/* Cloud, drawn on top so it overlaps and covers the lower half of the sun; scaled down slightly so more of the sun peeks out */}
        <path
          d="M19.36 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.64-4.96"
          fill="currentColor"
          transform="translate(1.9 4) scale(0.7)"
        />
      </svg>
    </SvgIcon>
  )
};

export default SunnyCloudy;
