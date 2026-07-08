When you change a backend dto, always run the `generate_openapi.py` script to update `web-ui/openapi.json`. On the frontend run `npm run generate-api` to re-generate the api and dto types on the frontend.

On the frontend when you add a new text to the UI, always add it to the translation files and use the translations via intl.

When changes made to the backend check whether existing tests broke and evaluate whether they broke due to requirements change or by a side effect. When developing new features make sure to cover them with tests. To run the tests run the following command: `python -m unittest discover`.

When you do changes and the version number is not changed yet in `AppSidebar.tsx` then raise it to the next minor or patch version.

After every larger change document it in `CHANGELOG.md`.
