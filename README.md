# Full-Stack Review Platform API (Backend)

## 📌 Submission Links

- **GitHub Repository (Frontend):** [https://github.com/iasraful/review-frontend](https://github.com/iasraful/review-frontend)
- **Live Frontend URL (Next.js):** [https://review-frontend-pi.vercel.app/](https://review-frontend-pi.vercel.app/)
- **GitHub Repository (Backend):** [https://github.com/iasraful/review-API](https://github.com/iasraful/review-API)
- **Live Backend API URL (FastAPI):** [https://review-api-d06r.onrender.com/](https://review-api-d06r.onrender.com/)
- **API Documentation (Swagger/OpenAPI):** [https://review-api-d06r.onrender.com/docs](https://review-api-d06r.onrender.com/docs)

---

## 🚀 Setup Instructions (Backend)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/iasraful/review-API.git
   cd review-API
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   # On Windows:
   source env/Scripts/activate
   # On Mac/Linux:
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Update `DATABASE_URL` with your local PostgreSQL credentials.
   ```bash
   cp .env.example .env
   ```

5. **Run the application:**
   ```bash
   fastapi dev app/main.py
   # OR
   uvicorn app.main:app --reload
   ```

The API will be available at `http://127.0.0.1:8000`.

---

## 🗄️ Database Migration / Schema

This project uses SQLAlchemy as the ORM. The database tables are automatically created on startup using `Base.metadata.create_all(bind=engine)` in `app/main.py`. 

### Schema Definition

**1. Users Table (`users`)**
- `id` (Integer, Primary Key)
- `name` (String, Indexed)
- `email` (String, Unique, Indexed)
- `created_at` (DateTime, default: current time)

**2. Products Table (`products`)**
- `id` (Integer, Primary Key)
- `title` (String, Indexed)
- `description` (String)
- `image_url` (String, nullable)
- `created_at` (DateTime, default: current time)

**3. Reviews Table (`reviews`)**
- `id` (Integer, Primary Key)
- `product_id` (Integer, Foreign Key to `products.id`)
- `user_id` (Integer, Foreign Key to `users.id`)
- `rating` (Integer)
- `comment` (String)
- `created_at` (DateTime, default: current time)

### How to Apply Migrations
If you drop your local database, simply restarting the FastAPI server will recreate all tables from the SQLAlchemy models. 
*(For production scale, a tool like Alembic would be integrated for schema migrations).*
