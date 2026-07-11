const MacheteAndTravelbag = () => {
  return (
    <>
      <g id="machete" transform="rotate(-42, 38, 65)">
        <rect
          stroke="#000000"
          strokeWidth={1}
          id="machete-handle-1"
          width="6"
          height="12"
          x="25"
          y="70"
          fill="#a05a2c"
        />
        <rect
          stroke="#000000"
          strokeWidth={1}
          id="machete-handle-2"
          width="10"
          height="3"
          x="23"
          y="67"
          fill="#a05a2c"
        />
        <path
          stroke="#000000"
          strokeLinecap="butt"
          strokeLinejoin="miter"
          strokeOpacity={1}
          d="M 31,67 V 22 q -8,0 -8,6 l 2,39 z"
          id="machete-blade-1"
          fill="#b3b3b3"
          strokeWidth="1"
        />
        <path
          stroke="#000000"
          strokeLinecap="butt"
          strokeLinejoin="miter"
          strokeOpacity={1}
          d="M 31,67 V 27 q -4,0 -4,3 l 1,37 z"
          id="machete-blade-2"
          fill="#999999"
          strokeWidth="1"
        />
      </g>
      <g id="travelbag-stick" transform="rotate(45, 92, 64)">
        <rect stroke="#000000" strokeWidth={1} id="stick" width="2" height="64" x="100" y="20" fill="#a05a2c" />
        <g id="travelbag" transform="rotate(45, 101,28)">
          <path
            fill="#ffe6d5"
            stroke="#000000"
            strokeLinecap="butt"
            strokeLinejoin="miter"
            strokeOpacity={1}
            d="M 94,25 114,34 c 12,2 12,-14 0,-12 L 94,31 Z"
            id="travelbag-bag"
          />
          <circle fill="#ffe6d5" stroke="#000000" strokeWidth={1} id="travelbag-knot" cx="101" cy="28" r="2" />
        </g>
      </g>
    </>
  );
};

export default MacheteAndTravelbag;
