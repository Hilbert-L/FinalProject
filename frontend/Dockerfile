# Use an official Node.js runtime as the base image
FROM node:14-alpine

# Set the working directory inside the container
WORKDIR /app

# Install create-vite globally
RUN npm install -g create-vite

# Install prettier as a development dependency
RUN npm install --save-dev prettier

# Copy the rest of the project files to the container
COPY package*.json ./
COPY vite.config.ts ./


# Delete the existing node_modules directory (if any)
RUN rm -rf node_modules

# Install project dependencies
RUN npm install

# Expose the port used by the frontend (usually 3000 or as configured in Vite)
EXPOSE 3000

# Start the development server
CMD ["npm", "run", "dev"]
