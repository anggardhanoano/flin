# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies using pnpm
RUN npm install -g pnpm && pnpm install

# Copy the rest of the code
COPY . .

# Build the app
RUN pnpm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Install serve for static file serving
RUN npm install -g serve

# Copy the built application from the builder stage
COPY --from=builder /app/dist ./dist

# Expose port
EXPOSE 5173

# Serve the static files
CMD ["serve", "-s", "dist", "-l", "5173", "--no-clipboard"]