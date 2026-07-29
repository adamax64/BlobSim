type CatEarsProps = {
  color: string;
};

const INNER_EAR_COLOR = '#ffc0cb';

export const CatEars = ({ color }: CatEarsProps) => {
  return (
    <>
      <path
        id="cat-ear-left"
        fill={color}
        stroke="#000000"
        strokeWidth={1}
        strokeLinejoin="round"
        d="M 13,26.5 38,7 18,-16 Z"
      />
      <path
        id="cat-ear-left-inner"
        fill={INNER_EAR_COLOR}
        strokeLinejoin="round"
        d="M 20.25,19 32,10 22,-2 Z"
      />
      <path
        id="cat-ear-right"
        fill={color}
        stroke="#000000"
        strokeWidth={1}
        strokeLinejoin="round"
        d="M 117,26.5 92,7 112,-16 Z"
      />
      <path
        id="cat-ear-right-inner"
        fill={INNER_EAR_COLOR}
        strokeLinejoin="round"
        d="M 109.75,19 98,10 108,-2 Z"
      />
    </>
  );
};
