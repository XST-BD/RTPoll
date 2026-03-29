# Deployment Guide

This backend is deployed using:
- API: Render
- Database: Neon (Postgres)
- Cache: Upstash (Redis)
- Queue: CloudAMQP (RabbitMQ)

## Environment Variables

ENVIRONMENT=PROD 
FRONTEND_URL=
DATABASE_URL=
REDIS_URL=
RABBITMQ_URL=
SECRET_KEY=
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIN_PORT_SSL=
MAIN_PORT_TLS=
MAIL_SERVER=

These are injected via .env file or host environment.


## Docker Compose Services

### backend
Runs FastAPI application.

### celery-worker
Processes background jobs from RabbitMQ.

### celery-beat
Schedules periodic tasks.

### Start Services
docker compose up -d --build

### Stop Services
docker compose down

### View Logs
docker compose logs -f


## Common Issues

- Mail not sending
  → Check env variables and check if smtp usable in server

- Worker not processing tasks
  → Check RabbitMQ URL

- Tasks delayed
  → Check Celery Beat is running

- Backend cannot connect to Redis
  → Verify Upstash credentials

- Containers restart repeatedly
  → Check docker logs


## Notes

- All services run as Docker containers
- backend/docker-compose.yml and backend/Dockerfile is used for deployment
- External services are managed separately
- No local database or Redis in production


## Health Check

` GET /health `
Returns:
` {"status": "ok"} `