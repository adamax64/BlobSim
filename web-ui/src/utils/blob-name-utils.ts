export const getShortName = (name: string): string => {
  const nameParts = name.split(' ');
  if (nameParts.length <= 1) return name;

  const firstName = nameParts[0];
  const lastName = nameParts[nameParts.length - 1];
  return `${firstName[0]}. ${lastName}`;
};
