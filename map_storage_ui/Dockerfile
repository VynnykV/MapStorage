# Use a specific version of node to prevent future compatibility issues
FROM node:16-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Ensure that all dependency management files are copied
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./

# Install dependencies based on the lock file present
RUN if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm install; \
    else echo "Lockfile not found, cannot build" && exit 1; \
    fi

FROM node:16-alpine AS builder
WORKDIR /app

# Ensure all files are copied correctly
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build the project
RUN yarn build

FROM node:16-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Setup the node environment for production
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy the built files from the builder stage
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Run the application under the non-privileged user 'nextjs'
USER nextjs
EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
