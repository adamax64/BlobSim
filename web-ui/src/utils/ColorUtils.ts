/**
 * Get the contrasting color (black or white) for a given hex color.
 * @param hexcolor The hex color code (e.g., "#FFFFFF").
 * @returns "black" or "white" depending on the brightness of the color.
 */
export function getContrastYIQ(hexcolor: string): 'black' | 'white' {
  hexcolor = hexcolor.replace('#', '');
  const r = parseInt(hexcolor.substring(0, 2), 16);
  const g = parseInt(hexcolor.substring(2, 4), 16);
  const b = parseInt(hexcolor.substring(4, 6), 16);
  const yiq = (r * 299 + g * 587 + b * 114) / 1000;
  return yiq >= 128 ? 'black' : 'white';
}
