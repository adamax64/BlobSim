When you change a backend dto, always run the `generate_openapi.py` script to update `web-ui/openapi.json`. On the frontend run `npm run generate-api` to re-generate the api and dto types on the frontend.

On the frontend when you add a new text to the UI, always add it to the translation files and use the translations via intl.
