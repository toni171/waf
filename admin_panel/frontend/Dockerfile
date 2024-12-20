# Use the official Node.js image for building
FROM node:16-alpine as build

# Set working directory
WORKDIR /app

# Copy only package.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the React app
RUN npm run build

# Serve the app using a lightweight web server
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html

# Expose the port for the application
EXPOSE 80

# Start NGINX server
CMD ["nginx", "-g", "daemon off;"]
