# Sales and Trading App - API Documentation

## Project Overview

The Sales and Trading App is a web-based platform designed to facilitate the buying and selling of financial assets, goods, or services. The system includes real-time trading functionalities, sales tracking, and an analytics dashboard to provide business insights.

## API Endpoints

This document provides a comprehensive list of all endpoints available for testing in the application.

### Authentication Endpoints

1. **User Registration**

   - URL: `/api/users/register/`
   - Method: POST
   - Description: Register a new user
   - Permissions: AllowAny
   - Request Body:
     ```json
     {
       "username": "testuser",
       "email": "test@example.com",
       "password": "securepassword",
       "first_name": "Test",
       "last_name": "User",
       "role": "TRADER"
     }
     ```

2. **User Login**

   - URL: `/api/users/login/`
   - Method: POST
   - Description: Login with username and password
   - Permissions: AllowAny
   - Request Body:
     ```json
     {
       "username": "testuser",
       "password": "securepassword"
     }
     ```

3. **Token Refresh**

   - URL: `/api/users/refresh_token/`
   - Method: POST
   - Description: Refresh access token using refresh token
   - Permissions: AllowAny
   - Request Body:
     ```json
     {
       "refresh": "your_refresh_token"
     }
     ```

4. **Token Info**
   - URL: `/api/users/token_info/`
   - Method: POST
   - Description: Get token expiration information
   - Permissions: AllowAny
   - Request Body:
     ```json
     {
       "token": "your_access_token"
     }
     ```

### User Management Endpoints

5. **User List**

   - URL: `/api/users/`
   - Method: GET
   - Description: List all users
   - Permissions: IsAuthenticated, IsOwnerOrAdmin

6. **User Detail**

   - URL: `/api/users/{id}/`
   - Method: GET
   - Description: Get user details
   - Permissions: IsAuthenticated, IsOwnerOrAdmin

7. **User Update**

   - URL: `/api/users/{id}/`
   - Method: PUT/PATCH
   - Description: Update user details
   - Permissions: IsAuthenticated, IsOwnerOrAdmin

8. **User Delete**
   - URL: `/api/users/{id}/`
   - Method: DELETE
   - Description: Delete a user
   - Permissions: IsAuthenticated, IsOwnerOrAdmin

### Product Management Endpoints

9. **Categories List**

   - URL: `/api/categories/`
   - Method: GET, POST
   - Description: List all categories or create a new category

10. **Category Detail**

    - URL: `/api/categories/{id}/`
    - Method: GET, PUT, PATCH, DELETE
    - Description: Retrieve, update or delete a category

11. **Tags List**

    - URL: `/api/tags/`
    - Method: GET, POST
    - Description: List all tags or create a new tag

12. **Tag Detail**

    - URL: `/api/tags/{id}/`
    - Method: GET, PUT, PATCH, DELETE
    - Description: Retrieve, update or delete a tag

13. **Products List**

    - URL: `/api/products/`
    - Method: GET, POST
    - Description: List all products or create a new product

14. **Product Detail**
    - URL: `/api/products/{id}/`
    - Method: GET, PUT, PATCH, DELETE
    - Description: Retrieve, update or delete a product

### Trading Endpoints

15. **Orders List**

    - URL: `/api/orders/`
    - Method: GET, POST
    - Description: List all trading orders or create a new order

16. **Order Detail**

    - URL: `/api/orders/{id}/`
    - Method: GET, PUT, PATCH, DELETE
    - Description: Retrieve, update or delete a trading order

17. **Order Book List**

    - URL: `/api/orderbook/`
    - Method: GET
    - Description: List all order book entries

18. **Order Book Detail**

    - URL: `/api/orderbook/{id}/`
    - Method: GET
    - Description: Retrieve an order book entry

19. **Notifications List**

    - URL: `/api/notifications/`
    - Method: GET
    - Description: List all trading notifications

20. **Notification Detail**
    - URL: `/api/notifications/{id}/`
    - Method: GET
    - Description: Retrieve a trading notification

### Sales Endpoints

21. **Promotions List**

    - URL: `/api/promotions/`
    - Method: GET, POST
    - Description: List all promotions or create a new promotion

22. **Promotion Detail**

    - URL: `/api/promotions/{id}/`
    - Method: GET, PUT, PATCH, DELETE
    - Description: Retrieve, update or delete a promotion

23. **Sales Orders List**

    - URL: `/api/orders/`
    - Method: GET, POST
    - Description: List all sales orders or create a new sales order
    - Note: This endpoint might conflict with trading orders, check the actual implementation

24. **Sales Order Detail**

    - URL: `/api/orders/{id}/`
    - Method: GET, PUT, PATCH, DELETE
    - Description: Retrieve, update or delete a sales order

25. **Invoices List**

    - URL: `/api/invoices/`
    - Method: GET, POST
    - Description: List all invoices or create a new invoice

26. **Invoice Detail**
    - URL: `/api/invoices/{id}/`
    - Method: GET, PUT, PATCH, DELETE
    - Description: Retrieve, update or delete an invoice

### Analytics Endpoints

27. **Trading Metrics List**

    - URL: `/api/trading-metrics/`
    - Method: GET
    - Description: List all trading metrics

28. **Trading Metric Detail**

    - URL: `/api/trading-metrics/{id}/`
    - Method: GET
    - Description: Retrieve a trading metric

29. **Sales Metrics List**

    - URL: `/api/sales-metrics/`
    - Method: GET
    - Description: List all sales metrics

30. **Sales Metric Detail**

    - URL: `/api/sales-metrics/{id}/`
    - Method: GET
    - Description: Retrieve a sales metric

31. **Product Performance List**

    - URL: `/api/product-performance/`
    - Method: GET
    - Description: List all product performance metrics

32. **Product Performance Detail**
    - URL: `/api/product-performance/{id}/`
    - Method: GET
    - Description: Retrieve a product performance metric

### API Documentation Endpoints

33. **Swagger JSON**

    - URL: `/swagger.json`
    - Method: GET
    - Description: Get Swagger API documentation in JSON format

34. **Swagger YAML**

    - URL: `/swagger.yaml`
    - Method: GET
    - Description: Get Swagger API documentation in YAML format

35. **Swagger UI**

    - URL: `/swagger/`
    - Method: GET
    - Description: Interactive Swagger UI for API documentation

36. **ReDoc UI**
    - URL: `/redoc/`
    - Method: GET
    - Description: ReDoc UI for API documentation

## Testing the API

For testing these endpoints, you can use:

1. **Swagger UI**: Navigate to `/swagger/` to interactively test all endpoints
2. **Postman or similar API testing tools**
3. **curl commands** from the command line

### Authentication Flow

Most endpoints require authentication, so you'll need to:

1. Register a user at `/api/users/register/`
2. Login at `/api/users/login/` to get JWT tokens
3. Use the access token in the Authorization header for subsequent requests:
   ```
   Authorization: Bearer <your_access_token>
   ```

### Example curl Commands

#### Register a new user

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"securepassword","first_name":"Test","last_name":"User","role":"TRADER"}'
```

#### Login

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"securepassword"}'
```

#### Get products with authentication

```bash
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer <your_access_token>"
```

## Technology Stack

- **Backend**: Django, Django Rest Framework, Celery
- **Database**: PostgreSQL
- **Caching**: Redis
- **API Documentation**: Swagger/drf-yasg
- **Authentication**: JWT (JSON Web Tokens)

## Project Structure

The project follows Django's best practices and is structured into the following apps:

- **usersapp**: Handles authentication, profiles, and role management
- **productsapp**: Manages assets, products, and categories
- **tradingapp**: Manages trade execution, orders, and real-time updates
- **salesapp**: Handles sales tracking, payments, and invoices
- **analyticsapp**: Provides reports, dashboards, and insights
