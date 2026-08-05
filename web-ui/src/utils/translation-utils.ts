import { TranslationsDto } from '../../generated';

const DEFAULT_LANGUAGE = 'en';

/** Resolve the text for the given language, falling back to the default language, then the first entry. */
export const getLocalizedText = (translations: TranslationsDto[] | undefined | null, language: string): string => {
  if (!translations || translations.length === 0) {
    return '';
  }
  return (
    translations.find((translation) => translation.language === language)?.text ??
    translations.find((translation) => translation.language === DEFAULT_LANGUAGE)?.text ??
    translations[0].text
  );
};
