# Tireder

An application designed to track and measure daily stress and tiredness levels.
With a simple interface, Tireder helps you easily log daily feelings to gain insight into your well-being.

## Overview
**Tireder**, your daily tiredness tracker, is an application to help users measure their stress and tiredness levels.
Once registered, users can log in to submit their current feeling and have access to their past records.
Tireder also provides a real-time chatbot to assist users in managing their stress. This project is developed using Python, MongoDB, JSON and Socket.

## Features
1. User Registration and Authentication:
   - Users can create new accounts, log in, and manage profiles 
   - Password-based authentication ensure secure access
2. Tiredness Entry:
   - Enable users to log their current tiredness levels
   - Implement JSON formatting for user’s input, including a rating system and optional notes to log their current tiredness levels.
3. View Past Entries:
   - Allow users to review their past tiredness entries with varied viewing options 
   - Ensure real-time interface updates when a new log are made
4. Real-Time Chatbot Integration:
   - Use the OpenAI API and Socket.io to implement a real-time chat user interface, this feature aims to assist users in managing their stress and tiredness
5. Admin Management:
   - Manage user accounts
   - Monitor user entries for better insight
6. Database Utilization:
   - Implementation of MongoDB for data storage
   - Use of JSON for data formatting

## Structure
```
Tireder/
│
├── server/
│   ├── __init__.py
│   ├── admin.py
│   ├── auth.py
│   ├── chatbot.py
│   ├── models.py
│   ├── utils.py
│   └── views.py
│
├── web_client/
│   ├── static/
│   │   ├── css/
│   │   ├── img/
│   │   └── js/
│   └── templates/
│       ├── admin/
│       │   ├── admin.html
│       │   └── details.html
│       ├── base.html
│       ├── chatbot.html
│       ├── home.html
│       ├── login.html
│       ├── logout.html
│       └── signup.html
│
├── config.py
├── main.py
├── README.md
└── requirements.txt
```

## Getting Started
To run the application, follow the steps below:
1. Clone the repository: `git clone https://github.com/Pumbaaxx/Tireder.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. The `config.py` file contains the necessary configurations for this project. Modify the file to set your MongoDB URI, OpenAI API key, and necessary variables
3. Run the application: `python main.py`
4. Open your browser and go to `http://localhost:5000/`

## References
APIs:
- [MongoDB](https://www.mongodb.com/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Socket.io](https://socket.io/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)
- [OpenAI API](https://beta.openai.com/)

Styling:
- [Bootstrap](https://getbootstrap.com/)
- chatbox: [codepen](https://codepen.io/)
- avatars: [Freepik - Flaticon](https://www.flaticon.com/free-icons/buddy)
