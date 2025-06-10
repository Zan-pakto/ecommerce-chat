# E-Commerce Sales Chatbot

A comprehensive sales chatbot system for e-commerce platforms, built with Python Flask backend and modern JavaScript frontend.

## Features

- Interactive chatbot interface for product search and purchase
- User authentication and session management
- Responsive design for all devices
- RESTful API backend
- Mock e-commerce inventory
- Chat history tracking and analysis
- Secure user sessions

## Tech Stack

### Backend
- Python 3.8+
- Flask (Web Framework)
- SQLAlchemy (ORM)
- Flask-Login (Authentication)
- Flask-JWT-Extended (JWT Tokens)
- SQLite (Development Database)

### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5 (UI Framework)

## Project Structure

```
ecommerce-chatbot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── config.py
│   └── run.py
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
├── tests/
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
5. Run the development server:
   ```bash
   flask run
   ```

## API Documentation

### Authentication Endpoints
- POST /api/auth/register - Register new user
- POST /api/auth/login - User login
- POST /api/auth/logout - User logout

### Chatbot Endpoints
- POST /api/chat/message - Send message to chatbot
- GET /api/chat/history - Get chat history
- POST /api/chat/reset - Reset chat session

### Product Endpoints
- GET /api/products - List all products
- GET /api/products/<id> - Get product details
- GET /api/products/search - Search products

## Development Challenges and Solutions

1. **Real-time Chat Updates**
   - Challenge: Implementing real-time updates without WebSocket
   - Solution: Used polling with optimized intervals and caching

2. **Session Management**
   - Challenge: Maintaining chat context across sessions
   - Solution: Implemented JWT-based session management with refresh tokens

3. **Mobile Responsiveness**
   - Challenge: Ensuring consistent UI across devices
   - Solution: Used Bootstrap's grid system and custom media queries

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 