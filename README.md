# L4IT Backend

This project demonstrates a simple authentication and blog system using FastAPI, SQLAlchemy, JWT, and file uploads.

## Features
- Register and login with email and password (email must end with @l4it.net)
- JWT-based authentication
- Blog CRUD (create, read, update, delete)
- Only the creator of a blog can update or delete it
- Only authenticated users can access their own blogs via `/blog/user/{user_id}`
- Image upload for blogs (jpg, png, gif, webp)
- CORS enabled for frontend integration

## Setup

1. **Clone the repository** (if not already):
   ```sh
   git clone <repo-url>
   cd <repo-folder>
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in your project root:
   ```env
   MYSQL_USER=youruser
   MYSQL_PASSWORD=yourpassword
   MYSQL_DB=yourdb
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run the application:**
   ```sh
   uvicorn app.main:app --reload
   ```

6. **API Docs:**
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

## Authentication
- Register: `POST /auth/register`
- Login: `POST /auth/login` (returns `access_token`)
- For protected endpoints, add header:
  ```
  Authorization: Bearer <access_token>
  ```

## Blog Endpoints
- `POST /blog/` — Create a blog (requires token)
- `GET /blog/` — List all blogs
- `GET /blog/{blog_id}` — Get a single blog
- `PUT /blog/{blog_id}` — Update a blog (requires token, only by creator)
- `DELETE /blog/{blog_id}` — Delete a blog (requires token, only by creator)
- `GET /blog/user/{user_id}` — Get all blogs by a user (requires token, only for self)

### Blog Create/Update Example (Postman)
- **Method:** POST or PUT
- **URL:** `http://localhost:8000/blog/` or `http://localhost:8000/blog/{blog_id}`
- **Body:** `form-data`
  - `heading` (text)
  - `short_description` (text)
  - `content` (text)
  - `meta_title` (text, optional)
  - `meta_description` (text, optional)
  - `image` (file, optional, jpg/png/gif/webp)
- **Headers:**
  - `Authorization: Bearer <access_token>`

### Image Access
- Uploaded images are available at: `http://localhost:8000/static/uploads/<filename>`
- The API returns the full image URL for use in your frontend.

---

**Note:** This uses MySQL for demo purposes. For production, use a robust database and secure your secret keys. 
