## Backend setup and installations

## Prerequisites

### Setup
- Python installed
- Latest docker and docker compose installed

### Environment
- Create backend/.env and use proper env variables. 
- See docs/deployment.md for details

### Reverse Proxy (Nginx)
- Setup SSL certificates in nginx/certs/
    1. `cd nginx && mkdir -p certs`
    2. `openssl req -x509 -nodes -days 365  -newkey rsa:2048  -keyout privkey.pem -out fullchain.pem`

### Start server
1. Complete prerequisites
2. `docker compose up -- build`

### Notes
This is a self-signed certificate, not for deployment
For more details check docs/

