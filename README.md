# FastAPI Project

## Overview
This project is a FastAPI-based backend application that provides RESTful APIs for managing products and customers, with authentication and role-based access control. It uses MongoDB as the database and includes logging middleware for request tracking.

## Features
- **Product Management**: Create, update, retrieve, and delete products.
- **Customer Management**: Register users, login for different roles (customer, admin, store).
- **Authentication**: JWT-based authentication for secure access.
- **Role-Based Access Control**: Different endpoints for admin, store, and user roles.
- **Logging Middleware**: Logs all incoming requests and responses with timing.
- **Exception Handling**: Custom exception handlers for 404, 400, and 500 errors.

## Project Structure
```
├── main.py                # FastAPI app entry point
├── auth.py                # JWT authentication logic
├── exceptions.py          # Custom exception classes
├── dependencies.py        # Dependency functions (e.g., role checks)
├── middlewares/
│   └── logging.py         # Logging middleware
├── models/
│   ├── product.py         # Product Pydantic models
│   └── customer.py        # Customer Pydantic models
├── routes/
│   ├── product.py         # Product API routes
│   └── customer.py        # Customer API routes
├── database/
│   └── mongo.py           # MongoDB connection setup
├── schemas/
│   └── product_schema.py  # Additional product schemas
├── crud/                  # (CRUD logic placeholder)
└── ...
```

## Setup Instructions
1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd fastapi_project
   ```
2. **Create a virtual environment and activate it**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
   Install the following packages (inferred from the codebase):
   ```bash
   pip install fastapi uvicorn motor python-dotenv pydantic[jwt] python-jose
   ```
   - `fastapi`: Web framework
   - `uvicorn`: ASGI server
   - `motor`: Async MongoDB driver
   - `python-dotenv`: For loading environment variables
   - `pydantic`: Data validation
   - `python-jose`: JWT handling

4. **Set up environment variables**
   Create a `.env` file in the root directory with at least:
   ```env
   MONGO_URI=mongodb://localhost:27017
   SECRET_KEY=your_secret_key
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## API Overview
### Product Endpoints (`/product`)
- `POST /product/` (admin, store): Create a new product
- `PATCH /product/{product_id}` (admin, store): Update a product
- `GET /product/` (admin, user): List all products
- `DELETE /product/{product_id}` (admin): Delete a product

### Customer Endpoints (`/customer`)
- `POST /customer/user`: Register a new user
- `POST /customer/login/customer`: Login as customer
- `POST /customer/login/admin`: Login as admin
- `POST /customer/login/store`: Login as store

### Home
- `GET /`: Home route

## Authentication
- JWT tokens are used for authentication.
- Include the token in the `Authorization` header as `Bearer <token>`.
- Roles supported: `user`, `admin`, `store`.

## Logging
All requests and responses are logged with method, path, body, status, and processing time.

## Database
- MongoDB is used for storing products and customers.
- Connection URI is set via the `MONGO_URI` environment variable.

## License
This project is for educational/demo purposes. 