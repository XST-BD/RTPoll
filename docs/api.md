# API Docs

## Swagger (detailed api guidline)
https://localhost:8000/docs

## Auth
JWT-based authentication.

## Flows

### Authentication
    1. API creates and sends refresh_token with access token during login
    2. Frontend calls /auth/refresh in fixed interval to get newer access tokens
    3. Refresh token is deleted during logout in /auth/logout

### Registration
    1. POST /auth/register
    2. Email verification sent
    3. POST /auth/verify-email
    4. Redirected to login in frontend
    5. POST /auth/login

### Voting
- User votes on a poll
- If already voted → previous vote updated

### Workers Processing
- Cache to DB sync operation is handled via Celery

## Notes
- One vote per user per poll