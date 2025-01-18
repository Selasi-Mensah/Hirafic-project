# Hirafic Project

Hirafic is a web application that connects clients with artisans. The project consists of a backend server built with Flask and a frontend client built with React.

## Technologies Used

### Backend
- **Languages**: Python
- **Frameworks**: Flask, Flask-SQLAlchemy
- **Caching**: Redis
- **Code Quality**: pycodestyle
### Frontend
- **Libraries**: React
- **HTTP Client**: Axios
> **Note:** Database must be updated to use PostgreSQL
### Database
- **Database Management System**: PostgreSQL
### Authentication
- **Method**: JWT (JSON Web Tokens)

### Deployment
- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Application Server**: Gunicorn
### Additional Technologies
- **Documentation**: Swagger UI
> **Note:** The documentation part may be removed later if not implemented
- **Version Control**: Git
- **Testing**: pytest

## Motivation

The Hirafic project was created to bridge the gap between clients and artisans by providing a seamless platform for booking and managing services. The goal is to empower local artisans by giving them a digital presence and making it easier for clients to find and book their services.

## Future Enhancements

- **Rating and Review System**: Allow clients to rate and review artisans.
- **Advanced Search**: Implement advanced search filters to help clients find artisans based on specific criteria.
- **Payment Integration**: Integrate payment gateways for secure online transactions.
- **Calendar Integration**: Sync bookings with popular calendar applications like Google Calendar and Outlook.
- **System Support**: Provide customer support to assist users with any issues or inquiries.
- **Reporting Feature**: Allow users to report inappropriate behavior or issues such as non-payment or failure to deliver services.
- **Multilingual Support**: Add support for multiple languages to cater to a broader audience.
- **AI Recommendations**: Use machine learning to recommend artisans to clients based on their preferences and booking history.
- **Mobile Application**: Develop a mobile app for both Android and iOS platforms.

## Challenges

- **Authentication**: Implementing JWT for stateless authentication presented challenges, especially with newer versions that had issues related to verifying the `sub` claim.
- **Scalability**: Ensuring the application could handle an increasing number of users and bookings required adhering to best practices for database design.
- **Performance**: To enhance performance, we optimized queries and database interactions, avoided the use of database listeners, and kept future growth in mind.
- **Security**: Protecting user data and ensuring secure transactions was a top priority.
- **Integration**: Seamlessly integrating various third-party services and APIs required cross-platform compatibility and the use of CORS.

## Contributors

- **Duaa Obeid** [GitHub](https://github.com/duaarabie) - [LinkedIn](https://www.linkedin.com/in/duaarabie)
- **Oliver Maketso** [GitHub](https://github.com/OliverMaketso)
- **Selasi Agbenyegah Mensah** [GitHub](https://github.com/Selasi-Mensah)
- **Paul Levites** [GitHub](https://github.com/Paulcode2)

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
    - [Backend](#backend)
    - [Frontend](#frontend)
- [Running the Application](#running-the-application)
    - [Backend](#backend-1)
    - [Frontend](#frontend-1)
    - [Running Both Servers Concurrently](#running-both-servers-concurrently)
- [API Endpoints](#api-endpoints)
    - [Authentication](#authentication)
    - [Booking](#booking)
    - [Artisan](#artisan)
    - [Client](#client)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication and authorization
- Artisan and client profiles
- Booking system for clients to book artisans
- Real-time notifications
- Facilities direct communication
- Search feature by map and specialization
- Responsive design

## Project Structure

Hirafic-project/
├── backend/
│   ├── __init__.py
│   ├── run.py
│   ├── config.py
│   ├── extensions.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── artisan.py
│   │   ├── client.py
│   │   └── booking.py       
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── artisan.py
│   │   ├── client.py
│   │   ├── booking.py
│   │   └── handlers.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_forms/
│   │   │   ├── __init__.py
│   │   │   ├── test_auth.py
│   │   │   ├── test_artisan.py
│   │   │   └── test_client.py
│   │   ├── test_models/
│   │   │   ├── __init__.py
│   │   │   ├── test_base.py
│   │   │   ├── test_user.py
│   │   │   ├── test_artisan.py
│   │   │   ├── test_client.py
│   │   │   └── test_booking.py
│   │   └── test_routes/
│   │   │   ├── __init__.py
│   │   │   ├── test_auth.py
│   │   │   ├── test_artisan.py
│   │   │   ├── test_client.py
│   │   │   └── test_handlers.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── email_service.py
├── Client/
│   ├── public/
│   ├── src/
│   │   ├── index.js
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   │   ├── Card.jsx
│   │   │   │   └── ...
│   │   │   ├── Counter.js
│   │   │   └── ...
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Profile.jsx
│   │   │   └── ...
│   │   ├── reducers/
│   │   │   ├── index.js
│   │   │   ├── counter.js
│   │   │   └── ...
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── store.js
│   │   └── ...
│   ├── package.json
│   ├── package-lock.json
│   └── ...
└── README.md

## Prerequisites

- Python 3.12
- Node.js (v18.3.1 or higher)
- npm or yarn
- Redis server

## Installation

### Backend

1. **Clone the repository**:

```sh
git clone https://github.com/Selasi-Mensah/Hirafic-project
cd Hirafic-project/backend
```

2. **Create a virtual environment and activate it**:

```sh
python3 -m venv myenv
source myenv/bin/activate
```

3. **Install the required Python packages**:

```sh
pip install -r requirements.txt
```

4. **Set up the database**:

```sh
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Frontend

1. **Navigate to the client directory**:

```sh
cd ../Client
```

2. **install the required npm packages**:

```sh
npm install
# Or
yarn install
```

## Running the Application

### Backend

1. **Start the Redis server**:

```sh
redis-server
```

2. **Start the Flask server**:

```sh
flask run
```

### Frontend

1. **Start the React development server**:

```sh
npm run dev
```

### Running Both Servers Concurrently

> **Note:** The following section is a placeholder and may be removed later if not implemented.

```sh
npm install concurrently --save-dev
# or
yarn add concurrently --dev
```

2. **Update the package.json in the Client directory to include the following scripts**:
```json
"scripts": {
    "start": "concurrently \"npm run start-react\" \"npm run start-python\"",
    "start-react": "react-scripts start",
    "start-python": "cd ../backend && source myenv/bin/activate && flask run"
}
```

## API Endpoints

### Authentication

- `GET /register`: Retrieve the needed fields to register.
- `GET /register`: Retrieve the needed field to register.
- `POST /login`: Login a user.
- `GET /login`: Retrieve the needed fields to login.
- `GET /logout`: Logout a user.

### Booking

- `POST /book_artisan`: Book an artisan.
- `GET /bookings`: Retrieve all user's bookings.

### Artisan

- `GET /artisan`: Retrieve logged-in artisan profile information.
- `POST /artisan`: Update logged-in artisan profile information.
- `GET /artisan/<username>`: Retrieve specific artisan profile information by username.
- `POST /artisan/<username>`: Update specific artisan profile information by username.

### Client

- `GET /client`: Retrieve logged-in client profile information.
- `POST /client`: Update logged-in client profile information.
- `GET /client/<username>`: Retrieve specific client profile information by username.
- `POST /client/<username>`: Update specific client profile information by username.
- `GET /client/<username>/nearby_artisan`: Retrieve near artisans for a specific client by username.

### CORS and Preflight Requests
To handle CORS and preflight requests, the API supports the OPTIONS method. This is particularly important for cross-origin requests, where the browser sends a preflight request to determine if the actual request is safe to send.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Explanation

1. **Features**: Lists the main features of the project.
2. **Project Structure**: Provides an overview of the project's directory structure.
3. **Prerequisites**: Lists the software and tools required to run the project.
4. **Installation**: Detailed steps to set up the backend and frontend of the project.
5. **Running the Application**: Instructions to start the backend and frontend servers, including running both servers concurrently.
6. **API Endpoints**: Lists the available API endpoints for authentication, booking, and profile management.
7. **Contributing**: Guidelines for contributing to the project.
8. **License**: Information about the project's license.

### Summary

This `README.md` file provides a comprehensive guide to setting up, running, and contributing to the Hirafic project. It includes detailed instructions and explanations for each step, ensuring that users and contributors can easily understand and work with the project. Adjust the content as needed to fit your specific project details.
