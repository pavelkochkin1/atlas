# Atlas Frontend

![Atlas Logo](https://your-logo-url.com/logo.png) <!-- Replace with your actual logo URL if available -->

## Table of Contents

- [Atlas Frontend](#atlas-frontend)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Tech Stack](#tech-stack)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Using Docker](#using-docker)
    - [Manual Setup](#manual-setup)
  - [Running the Application](#running-the-application)
    - [Using Docker](#using-docker-1)
    - [Manual Setup](#manual-setup-1)
  - [Project Structure](#project-structure)
  - [Configuration](#configuration)
    - [Docker](#docker)
    - [Nginx](#nginx)
  - [Scripts](#scripts)

## Overview

**Atlas Frontend** is a React-based web application designed to manage and explore data drafts. It provides users with a seamless interface to authenticate, view and confirm data drafts, and interact with a knowledge graph through a chat interface. The application is containerized using Docker and leverages modern web technologies such as TypeScript, Tailwind CSS, and React Router for an efficient and responsive user experience.

## Features

- **User Authentication**: Simple email-based login system.
- **Draft Management**: View, edit, and confirm data drafts with detailed descriptions, industries, teams, and associated fields.
- **Data Exploration**: Engage with a knowledge graph and interact with a chatbot for data insights.
- **Responsive Design**: Built with Tailwind CSS for a mobile-first, responsive user interface.
- **Containerization**: Easily deployable using Docker with a multi-stage build process.

## Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS, React Router
- **Backend API**: Assumed to be running on `localhost:8073` and `localhost:8053`
- **Containerization**: Docker, Nginx
- **Build Tools**: Webpack (via `react-scripts`)

## Prerequisites

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/) if you plan to use Docker for setup.
- **Node.js**: [Install Node.js](https://nodejs.org/) (version 18 or higher recommended) if you prefer manual setup.
- **npm**: Comes with Node.js installation.

## Installation

### Using Docker

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/atlas-frontend.git
   cd atlas-frontend
   ```

2. **Build the Docker Image**

   ```bash
   docker build -t atlas-frontend .
   ```

3. **Run the Docker Container**

   ```bash
   docker run -d -p 80:80 --name atlas-frontend atlas-frontend
   ```

   The application will be accessible at `http://localhost`.

### Manual Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/atlas-frontend.git
   cd atlas-frontend/frontend
   ```

2. **Install Dependencies**

   ```bash
   npm install
   ```

3. **Configure Environment Variables**

   If your application requires environment variables, create a `.env` file in the `frontend` directory and add the necessary configurations. *(Note: The current setup assumes API endpoints are hardcoded. For a more secure setup, consider using environment variables.)*

4. **Build Tailwind CSS**

   Tailwind CSS is already configured. Ensure that `postcss` and `autoprefixer` are properly set up via `postcss.config.js`.

## Running the Application

### Using Docker

After building and running the Docker container as described in the [Installation](#installation) section, access the application at `http://localhost`.

### Manual Setup

1. **Start the Development Server**

   ```bash
   npm start
   ```

   This will start the development server at `http://localhost:3000` (default port). Open this URL in your browser to view the application.

2. **Build for Production**

   To create an optimized production build:

   ```bash
   npm run build
   ```

   The build artifacts will be stored in the `build/` directory.

## Project Structure

```
atlas/
└── frontend/
    ├── Dockerfile
    ├── README.md
    ├── nginx.conf
    ├── package.json
    ├── postcss.config.js
    ├── tailwind.config.js
    ├── tsconfig.json
    ├── public/
    │   └── index.html
    └── src/
        ├── App.tsx
        ├── index.tsx
        ├── index.css
        ├── components/
        │   └── LoadingIndicator.tsx
        └── pages/
            ├── DraftDetailPage.tsx
            ├── DraftsPage.tsx
            ├── ExplorePage.tsx
            └── LoginPage.tsx
```

- **Dockerfile**: Defines the Docker image for the frontend application with a multi-stage build process.
- **nginx.conf**: Nginx configuration to serve the built React application.
- **package.json**: Lists project dependencies and scripts.
- **postcss.config.js**: Configures PostCSS with Tailwind CSS and Autoprefixer.
- **tailwind.config.js**: Tailwind CSS configuration file.
- **tsconfig.json**: TypeScript configuration.
- **public/**: Contains the static `index.html` file.
- **src/**: Source code of the React application.
  - **components/**: Reusable React components.
  - **pages/**: React components representing different pages/routes.

## Configuration

### Docker

The `Dockerfile` sets up a multi-stage build:

1. **Build Stage**:
   - Uses `node:18-alpine` image.
   - Installs dependencies and builds the React application.

2. **Production Stage**:
   - Uses `nginx:stable-alpine` image.
   - Copies the built application to Nginx's serving directory.
   - Configures Nginx using `nginx.conf`.
   - Exposes port `80` and starts Nginx in the foreground.

### Nginx

The `nginx.conf` file is configured to:

- Listen on port `80`.
- Serve static files from `/usr/share/nginx/html`.
- Redirect all routes to `index.html` for client-side routing support.

```nginx
server {
    listen 80;
    server_name localhost;
    location / {
        root   /usr/share/nginx/html;
        try_files $uri /index.html;
    }
}
```

## Scripts

- **`npm start`**: Starts the development server.
- **`npm run build`**: Builds the application for production.
- **`npm test`**: Runs the test suite using React Scripts.

**Docker Commands**:

- **Build Image**: `docker build -t atlas-frontend .`
- **Run Container**: `docker run -d -p 80:80 --name atlas-frontend atlas-frontend`
- **Stop Container**: `docker stop atlas-frontend`
- **Remove Container**: `docker rm atlas-frontend`
- **Remove Image**: `docker rmi atlas-frontend`
