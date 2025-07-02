#!/bin/sh

# Generate env.js from environment variables
cat <<EOF > /usr/share/nginx/html/env.js
window.env = {
  VITE_API_BASE_URL: "${VITE_API_BASE_URL}"
};
EOF

# Start nginx
nginx -g "daemon off;"
