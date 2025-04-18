# URL Shortener Backend

A Flask-based RESTful API backend for a URL shortener application. The backend uses MongoDB for data storage and includes endpoints for shortening URLs, redirecting to original URLs, and viewing analytics.

## Features

- Shorten long URLs to generate short, unique slugs
- Redirect from shortened URLs to original URLs
- Track click counts and timestamps for each shortened URL
- View analytics for each shortened URL

## Requirements

- Python 3.10+
- MongoDB (local or MongoDB Atlas)

## Installation

1. Clone the repository and navigate to the backend directory:

```bash
cd backend
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on the `.env.example` file:

```bash
cp .env.example .env
```

5. Update the `.env` file with your MongoDB connection URI and other configurations.

## Running the Application

To run the application in development mode:

```bash
flask run
```

Or alternatively:

```bash
python app.py
```

The API will be available at `http://localhost:5000`.

## API Endpoints

### Shorten a URL
- **POST** `/api/shorten`
  - Request body: `{ "url": "https://example.com/long-url" }`
  - Response: `{ "slug": "abc123", "shortUrl": "http://localhost:5000/abc123" }`

### Redirect to Original URL
- **GET** `/<slug>`
  - Redirects to the original URL associated with the slug
  - Increments click count and updates last clicked timestamp

### Get All URLs (Admin)
- **GET** `/api/urls`
  - Returns a list of all shortened URLs with their details

### Get URL Analytics
- **GET** `/api/analytics/<slug>`
  - Returns analytics for a specific URL: `{ "clickCount": 10, "createdAt": "2023-01-01T12:00:00", "lastClickedAt": "2023-01-02T15:30:00" }`

## Deployment

### MongoDB Atlas

1. Create a MongoDB Atlas account
2. Create a new cluster
3. Create a database user
4. Whitelist your IP address
5. Get the connection URI and update the `.env` file

### Deploying to a Cloud Platform

#### Heroku

1. Install Heroku CLI
2. Login to Heroku: `heroku login`
3. Create a new Heroku app: `heroku create your-app-name`
4. Add the MongoDB URI to Heroku config: `heroku config:set MONGO_URI=your_mongodb_uri`
5. Push to Heroku: `git push heroku main`

#### Render

1. Create a new Web Service on Render
2. Connect your repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `gunicorn "app:create_app()" --bind 0.0.0.0:$PORT`
5. Add environment variables including MONGO_URI

## Docker (Optional)

If you have Docker installed, you can run the application using Docker:

```bash
docker build -t url-shortener .
docker run -p 5000:5000 --env-file .env url-shortener
```

Or using Docker Compose:

```bash
docker-compose up
``` 