                                                                                                       
                                                                                                       
                                         API Reliability & Access Control Service

A backend infrastructure service responsible for authentication, authorization, rate limiting, and audit logging for protecting internal and external APIs.
This project models a real-world platform/security layer that enforces identity, permissions, and request policies before traffic reaches application services.



ABOUT
Modern distributed systems require a dedicated control layer to handle access enforcement, abuse prevention, and traceability. 
This service was designed to simulate such a layer, commonly found in production environments as part of an API gateway or platform security stack.

Core responsibilities:
1. Identity verification via JWT authentication
2. Role-based access control (RBAC)
3. Abuse mitigation through Redis-backed rate limiting
4. Security audit logging
5. Centralized error handling and request validation


ARCHITECTURE
This service operates as a policy enforcement point, ensuring only authorized, rate-compliant, and traceable requests reach backend systems.

Client Request -> API Reliability & Access Control Service -> Protected Downstream Services


TECHNOLOGY STACK
1. Backend Framework
      FastAPI (Python, async-first)
      Uvicorn (ASGI server)
2. Persistence
   PostgreSQL (primary relational datastore)
   SQLAlchemy 2.0 (ORM)
   Alembic (schema migrations)

3. Security
   JWT-based authentication (access + refresh tokens)
   bcrypt password hashing
   Role-Based Access Control (RBAC)

4. Caching & Traffic Control
   Redis (rate limiting & token tracking)

5. DevOps
   Docker & Docker Compose
   GitHub Actions (CI pipeline)

6. Testing
   Pytest
   HTTPX (async API testing)

AUTHENTICATON DESIGN :
The system uses a short-lived access token + rotating refresh token model.
Flow:
1. User authenticates with credentials
2. Server issues:
    Access token (short-lived)
    Refresh token (stored and rotatable)
3. Access token is required for protected endpoints
4. Expired access tokens can be renewed using a valid refresh token
5. Refresh tokens are rotated and can be revoked to limit session abuse
6. This design mirrors real-world stateless authentication strategies used in scalable systems.


Authorization (RBAC)
Authorization is enforced using role-based guards.
1. Users can have multiple roles
2. Roles map to permission scopes
3. Access checks are performed at the request layer before business logic execution
4. Unauthorized access results in 403 Forbidden.

Rate Limiting Strategy
To protect services from abuse and ensure fair resource usage:
1. Limits enforced per user and per IP
2. Counters stored in Redis for low-latency, high-throughput checks
3. Exceeded limits return HTTP 429 Too Many Requests
Redis is used to avoid database contention and allow fast expiration-based counters.

Audit Logging
All security-sensitive actions are recorded, including:
1. Authentication events
2 Token refresh and revocation
3. Authorization failures
4. Administrative actions
Each audit entry captures:
1. Actor identity
2. Action performed
3. Timestamp
4. Source IP
This provides traceability similar to compliance and monitoring systems in production environments.

ERROR HANDLING AND API STANDARDS
1. Centralized exception handling
2. Consistent JSON error responses
3. No internal stack traces exposed
4. Proper HTTP semantics (401, 403, 429, etc.)
5. Versioned API routes (/v1)


LOCAL DEVELOPMEN
Requirements
1. Docker
2. Docker Compose
Run the system
 - docker-compose up --build
Services started:
. API Server
. PostgreSQL
. Redis
API available at:
 - http://localhost:8000

TESTING
Automated tests cover:
- Authentication and token lifecycle
- Authorization enforcement
- Rate limiting behavior
Run tests locally:
 - pytest


FUTURE IMPROVEMENTS
. Distributed rate limiting across instances
. Metrics and monitoring integration
. Token introspection endpoint
. Policy-based permission system

AUTHOR
Built to explore backend architecture, API security, and platform engineering concepts through a production-style service.
