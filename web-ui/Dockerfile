# Stage 1: Build with Node.js and Java
FROM node:latest as build

# Install Java (for openapi-generator)
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y openjdk-17-jre-headless && \
    rm -rf /var/lib/apt/lists/*

# Enable Corepack (pnpm) and install OpenAPI Generator CLI globally
RUN corepack enable && corepack prepare pnpm@latest --activate
RUN pnpm add -g @openapitools/openapi-generator-cli

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile

# Copy the rest of the app
COPY . .

# Generate API client
RUN pnpm run generate-api

# Build the React app
RUN pnpm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built files from previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy custom Nginx config (optional, for SPA routing)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]
