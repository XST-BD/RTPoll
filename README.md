<div align="center">
  <h1>RTPoll</h1>

  <p>A real-time polling platform that allows users to create and share polls via public links, and and track live results through an interactive interface and insightful visual graph.</p>

  <a href="https://rtpoll.pages.dev/">
    <img src="https://img.shields.io/badge/Visit_Live_Site_%E2%9E%A4-818CF8?style=for-the-badge"/>
  </a>
</div>

<h2>Table of Contents</h2>

- [Features](#features)
- [Usages](#usages)
- [Tech Stack](#tech-stack)
  - [Frontend](#frontend)
  - [Backend](#backend)
- [Project Setup \& Installation](#project-setup--installation)
  - [Prerequisites](#prerequisites)
  - [Clone Repository](#clone-repository)
  - [Frontend Setup](#frontend-setup)
  - [Backend Setup](#backend-setup)
    - [Environment](#environment)
    - [Reverse Proxy (Nginx)](#reverse-proxy-nginx)
    - [Start server](#start-server)
    - [Notes](#notes)
- [Project Documentation](#project-documentation)
- [Authors](#authors)

## Features

- **User Authentication System** - Registration, login, logout, forgot password, email change, password reset, email verification and account deletion.
- **Poll Creation** - Create a poll with a question, options, expiration date and whether to make the result public or not.
- **Poll Sharing** - Share a poll via a public link.
- **Real-Time results** - View poll results in real-time.
- **Poll Deletion** - Delete polls.

## Usages

- **Create a poll:**
  - Enter a question.
  - Add options.
  - Set expiration date.
  - Choose whether to make the result public or not.
  - Click on "Create Poll" button.
  - Poll is created and you are redirected to the poll page.

- **Share a poll:**
  - Click on the share icon on the poll page to copy the link.
  - Share the link with people you want to participate in the poll.
  - People can access the poll by clicking on the link and can vote.

- **View poll results:**
  - Poll results are displayed in real-time.

- **Delete a poll:**
  - Click on the delete icon on the poll page to delete the poll.

- **User account management:**
  - Go to the settings page to change your account settings.
  - Delete all your polls.
  - Change your email.
  - Change your password.
  - Delete your account.

## Tech Stack

### Frontend

- Nuxt.js
- Tailwind CSS
- Pinia
- FingerprintJS
- ApexCharts
- Iconify

### Backend

- FastAPI
- PostgreSQL
- Redis
- RabbitMQ
- Celery
- JWT

## Project Setup & Installation

### Prerequisites

- [Git](https://git-scm.com/downloads)
- [Node.js (LTS Version Recommended)](https://nodejs.org/en/download/)
- [pnpm](https://pnpm.io/installation)
- [Python](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Clone Repository

1. Clone the repository
   ```bash
   git clone https://github.com/XST-BD/RTPoll.git
   ```
2. Navigate to the project directory
   ```bash
   cd RTPoll
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   pnpm install
   pnpm approve-builds
   ```
3. Set up the environment variables in frontend/.env file:
   ```
   API_URL="http://localhost:8000/api/v0"
   WS_URL="ws://localhost:8000/api/v0/ws"
   ```
4. Start the development server:
   ```bash
   pnpm dev
   ```
5. Open http://localhost:3000 in your browser.

**For Production Build**

1. Build the application:
   ```bash
   pnpm build
   ```
2. Preview the production build locally:
   ```bash
   pnpm preview
   ```
3. Open http://localhost:3000 in your browser.

### Backend Setup

#### Environment

- Create backend/.env and use proper env variables.
- See docs/deployment.md for details

#### Reverse Proxy (Nginx)

- Setup SSL certificates in nginx/certs/
  1. `cd nginx && mkdir -p certs`
  2. `openssl req -x509 -nodes -days 365  -newkey rsa:2048  -keyout privkey.pem -out fullchain.pem`

#### Start server

1. Complete prerequisites
2. `docker compose up -- build`

#### Notes

This is a self-signed certificate, not for deployment
For more details check docs/

## [Project Documentation](https://github.com/XST-BD/RTPoll/tree/main/docs)

- [Frontend](https://github.com/XST-BD/RTPoll/tree/main/docs/frontend.md)
- [Backend](https://github.com/XST-BD/RTPoll/tree/main/docs/api.md)
- [Deployment](https://github.com/XST-BD/RTPoll/tree/main/docs/deployment.md)
- [Architecture](https://github.com/XST-BD/RTPoll/tree/main/docs/architecture.md)

## Authors

- **[Atia Farha](https://github.com/atia-farha)** - Frontend Developer
- **[S.M Sadat](https://github.com/smsadat1)** - Backend Developer
