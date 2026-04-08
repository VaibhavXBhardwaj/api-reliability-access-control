     # API Reliability & Access Control

![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-TypeScript-61DAFB?style=for-the-badge&logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A production grade API gateway demonstrating authentication, role-based access control (RBAC), rate limiting, token refresh, and audit logging — built with FastAPI and React.

**Live Demo:** https://api-reliability-access-control.vercel.app  
**API Docs:** https://api-reliability-access-control-1.onrender.com/docs

## Features

- **JWT Authentication** — Secure signup/login with access & refresh token flow
- **Role-Based Access Control** — User and Admin roles with protected endpoints
- **Token Refresh** — Automatic access token renewal via refresh tokens
- **Rate Limiting** — Redis-backed request throttling per user
- **Audit Logging** — Every auth event is logged and viewable in the dashboard
- **Health Check Endpoint** — `/health` for uptime monitoring
- **Admin Panel** — Dedicated admin dashboard for user management
- **Dockerized** — Full Docker Compose setup for local development


## Tech Stack

| Layer | Technology |

| Backend | FastAPI, Python 3.12 |
| Frontend | React, TypeScript, Vite |
| Database | PostgreSQL 15 (Neon in production) |
| Cache / Rate Limiting | Redis 7 (Upstash in production) |
| Auth | JWT (python-jose), Passlib, Bcrypt |
| ORM | SQLAlchemy 2.0 |
| Containerization | Docker, Docker Compose |
| Frontend Hosting | Vercel |
| Backend Hosting | Render |

---

## Architecture



![bcde22e1-7edc-4112-942c-98342676e13f](https://github.com/user-attachments/assets/cb7d9760-b99d-4d1d-989d-bdf0bc5b16b7)







---

## API Endpoints

| Method | Endpoint | Description | Auth |

| POST | `/v1/auth/signup` | Register a new user | Public |
| POST | `/v1/auth/login` | Login and get tokens | Public |
| POST | `/v1/auth/refresh` | Refresh access token | Public |
| GET | `/v1/auth/admin-only` | Admin protected route | Admin |
| GET | `/health` | Health check | Public |


## Local Development

### Prerequisites
- Docker & Docker Compose
- Node.js 18+

### 1. Clone the repo
```bash
git clone https://github.com/VaibhavXBhardwaj/api-reliability-access-control.git
cd api-reliability-access-control
```

### 2. Create `.env` file
```env
DATABASE_URL=postgresql://admin:admin@postgres:5432/access_control
JWT_SECRET=supersecretkey123
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
REDIS_URL=redis://redis:6379
```

### 3. Start the backend
```bash
docker-compose up --build
```
Backend runs at: http://localhost:8000  
API Docs: http://localhost:8000/docs

### 4. Start the frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: http://localhost:3000

---

## Project Structure

api-reliability-access-control/
├── app/
│   ├── api/v1/          # API routes
│   ├── auth/            # Auth logic (router, service, schemas)
│   ├── core/            # JWT, config, settings
│   ├── db/              # Database setup, models, session
│   └── main.py          # FastAPI app entry point
├── frontend/
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── context/     # Auth context
│   │   └── pages/       # Login, Signup, Dashboard, Admin
│   └── package.json
├── tests/               # Pytest test suite
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

---

## Running Tests

```bash
docker-compose exec api pytest tests/ -v
```
## Deployment

| Service | Provider |

| Frontend | Vercel |
| Backend | Render |
| PostgreSQL | Neon |
| Redis | Upstash |
| Uptime Monitoring | UptimeRobot |


## License

MIT License — feel free to use this project as a reference or template.


## Author

**Vaibhav Bhardwaj**  
[GitHub](https://github.com/VaibhavXBhardwaj) · [LinkedIn](https://www.linkedin.com/in/vaibhavbhardwaj2810/)
