import { SvgIcon, SvgIconProps } from '@mui/material';

const SunnyRainy = (props: SvgIconProps) => {
  return (
    <SvgIcon {...props}>
      <svg focusable="false" aria-hidden="true" viewBox="0 0 24 24">
        {/* Sun rays, peeking out above/right of the cloud */}
        <path d="M17 3v-2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" fill="none" />
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
          d="M558-84q-15 8-30.5 2.5T504-102l-60-120q-8-15-2.5-30.5T462-276q15-8 30.5-2.5T516-258l60 120q8 15 2.5 30.5T558-84Zm240 0q-15 8-30.5 2.5T744-102l-60-120q-8-15-2.5-30.5T702-276q15-8 30.5-2.5T756-258l60 120q8 15 2.5 30.5T798-84Zm-480 0q-15 8-30.5 2.5T264-102l-60-120q-8-15-2.5-30.5T222-276q15-8 30.5-2.5T276-258l60 120q8 15 2.5 30.5T318-84Zm-18-236q-91 0-155.5-64.5T80-540q0-83 55-145t136-73q32-57 87.5-89.5T480-880q90 0 156.5 57.5T717-679q69 6 116 57t47 122q0 75-52.5 127.5T700-320H300Z"
          fill="currentColor"
          transform="translate(1.9 4) scale(0.7) scale(0.025) translate(0 960)"
        />
      </svg>
    </SvgIcon>
  );
};

export default SunnyRainy;
