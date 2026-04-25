# Stage 1: Build the Vite project
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy source code and build
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built assets
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the nginx template
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Cloud Run expects the port to be 8080
ENV PORT=8080
EXPOSE 8080

# Nginx alpine image with templates will automatically substitute env vars in /etc/nginx/templates
# into /etc/nginx/conf.d/ before starting
CMD ["nginx", "-g", "daemon off;"]
