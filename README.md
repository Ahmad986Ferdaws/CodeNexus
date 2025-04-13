🚀 Overview
CodeNexus is a modern web application for developers to share, discover, and collaborate on code snippets and interactive tutorials. Built with Python (FastAPI) and Vue.js, it provides a platform for developers to showcase their code, learn from others, and build a portfolio of programming knowledge.
✨ Features

Code Snippet Repository: Create, share, and discover code snippets with syntax highlighting
Interactive Tutorials: Build step-by-step programming tutorials with executable code examples
User Profiles: Showcase your coding expertise and track your learning progress
Search & Discovery: Find code by language, tags, or keywords
Social Interactions: Comment, like, and fork code snippets
Analytics Dashboard: Track popularity and performance of your shared code

🛠️ Tech Stack
Backend

Framework: FastAPI (Python 3.10+)
Database: PostgreSQL with SQLAlchemy ORM
Authentication: JWT with OAuth2 support
Task Queue: Celery with Redis
Testing: Pytest

Frontend

Framework: Vue.js 3 with Composition API
UI Components: PrimeVue
State Management: Pinia
Code Editor: Monaco Editor (VS Code's editor)
Styling: TailwindCSS

DevOps

Containerization: Docker and Docker Compose
CI/CD: GitHub Actions
Deployment: AWS/Heroku/DigitalOcean ready

📋 Prerequisites

Python 3.10+
Node.js 16+
PostgreSQL 13+
Redis 6+
Docker & Docker Compose (optional, for containerized setup)

📁 Project Structure
codenexus/
├── backend/                 # FastAPI application
│   ├── app/                 # Application code
│   │   ├── api/             # API endpoints
│   │   ├── core/            # Core functionality
│   │   ├── db/              # Database setup
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── ...
│   ├── alembic/             # Database migrations
│   └── tests/               # Test suite
├── frontend/                # Vue.js application
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── pages/           # Page components
│   │   ├── stores/          # Pinia stores
│   │   └── ...
└── docker/                  # Docker configuration
📚 API Documentation
When the backend is running, you can access:

Swagger UI: http://localhost:8000/docs
OpenAPI Spec: http://localhost:8000/api/v1/openapi.json

🧪 Testing
Backend Tests
bashcd backend
pytest                 # Run all tests
pytest -xvs            # Run with verbose output
pytest --cov=app tests # Run with coverage report
Frontend Tests
bashcd frontend
npm run test           # Run all tests
npm run test:unit      # Run unit tests only
npm run test:e2e       # Run end-to-end tests
📝 License
This project is licensed under the MIT License.
