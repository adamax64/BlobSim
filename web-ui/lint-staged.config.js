export default {
  // ESLint only needs to check the staged files.
  'src/**/*.{ts,tsx}': [
    'eslint --max-warnings=0',
    // tsc needs full project context to type-check correctly, so ignore the
    // staged filenames lint-staged would otherwise append and always run a
    // full project check instead.
    () => 'pnpm run typecheck',
  ],
};
