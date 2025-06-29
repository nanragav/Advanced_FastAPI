# Advanced FastAPI

A robust, production-ready FastAPI application with user authentication, blog management, secure HTTPS serving, and an asynchronous SQLAlchemy database backend.

## Features

- **FastAPI**: High-performance Python web framework for building APIs.
- **User Authentication**: Modular authentication logic (see `auth/`).
- **Blog Management**: Users can create and manage blogs.
- **Asynchronous SQLAlchemy**: Async ORM for scalable database operations.
- **Pydantic Schemas**: For request/response validation.
- **Router Modularization**: All API endpoints are organized using routers.
- **Secure HTTPS**: Runs with SSL/TLS certificates for encrypted connections.
- **Environment Variables**: Uses `.env` for configuration.

## Project Structure

```
.
├── main.py           # FastAPI app entrypoint and HTTPS server
├── models.py         # SQLAlchemy ORM models for User and Blog
├── schemas.py        # Pydantic schemas for API requests
├── database.py       # Database setup and async session management
├── routers/          # API routers (user, blog, etc.)
├── auth/             # Authentication utilities and logic
├── utils/            # Utilities (e.g., time functions)
├── certs/            # SSL/TLS certificates (key.pem, cert.pem)
└── .env              # Environment variables (not tracked in git)
```

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL (or any database supported by SQLAlchemy)
- [pipenv](https://pipenv.pypa.io/en/latest/) or `pip`
- SSL certificates (`cert.pem`, `key.pem` in `certs/` folder)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nanragav/Advanced_FastAPI.git
   cd Advanced_FastAPI
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment setup:**
   - Copy `.env.example` to `.env` and set the `DATABASE_URL` variable:
     ```
     DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
     ```

4. **Setup SSL Certificates:**
   - Place your `cert.pem` and `key.pem` files in the `certs/` directory.

5. **Run database migrations:**
   - (Assume you use Alembic or similar; see `database.py` for Base metadata)

### Running the Application

```bash
python main.py
```

By default, it serves on `https://0.0.0.0:8000/` with SSL.

## API Overview

### User Endpoints

- **Create User**
- **Login User**
- **Delete User**

### Blog Endpoints

- **Create Blog**
- **List Blogs**
- **Delete Blog**
- (See `/routers/` for detailed routes)

### Example Root Endpoint

```json
GET /
{
  "message": "FastAPI is running"
}
```

## Database Models

- **User**: `id`, `name`, `password`, `session_id`, `created_at`, `created_by`
- **Blog**: `id`, `title`, `body`, `user_id`
- Relationships: Users have many Blogs.

## Security

- All API traffic is encrypted via HTTPS (SSL certificates required).
- Passwords are stored securely (implement proper hashing in `auth/`).
- Session management via `session_id`.

## Contributing

1. Fork the repo
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Uvicorn](https://www.uvicorn.org/)

---

**Note:** This project is designed for educational and production-ready use. Be sure to review and implement all required security best practices before deploying.
