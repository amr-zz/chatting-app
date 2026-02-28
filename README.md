## 🗣️ Echo - Real-Time Chat Application

A scalable real-time chat application built with **Django, WebSockets,
Redis, JWT Authentication, and Daphne**, featuring a pure vanilla
JavaScript frontend.

----------------------------------------------------------------------


![Comp 1_00000](https://github.com/user-attachments/assets/5b28ea93-fef9-4100-a191-728bf330dc54)


----------------------------------------------------------------------
## 🚀 Overview

Echo enables real-time communication using WebSockets powered by
**Django Channels** and **Redis** as the channel layer backend.

The frontend is built with pure HTML, CSS, and vanilla JavaScript - no
frontend frameworks required.


----------------------------------------------------------------------


## 🏗️ Tech Stack

### 🔹 Backend

-   Python 3.x
-   Django
-   Django REST Framework
-   Django Channels
-   Redis (Channel Layer)
-   Daphne (ASGI Server)
-   JWT Authentication
-   SQLite (configurable)

### 🔹 Frontend

-   HTML5
-   CSS3
-   Vanilla JavaScript

### 🔹 Infrastructure (Optional)

-   Docker
-   Nginx

----------------------------------------------------------------------

### 🔁 Authentication Flow Explanation

1.  User authenticates using JWT.
2.  Client connects via WebSocket.
3.  Daphne handles ASGI connections.
4.  Django Channels routes WebSocket events.
5.  Redis broadcasts messages.
6.  Messages are delivered to connected users in real time.

----------------------------------------------------------------------

## 🔐 Authentication

Echo uses **JWT (JSON Web Tokens)** for secure authentication.

### Authentication Flow

1.  User registers/logs in via REST API.
2.  Server returns access and refresh tokens.
3.  Client attaches JWT token to WebSocket connection.
4.  Server validates token before allowing connection.

----------------------------------------------------------------------


## 📡 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|------------|--------------|
| POST | /api/users/login | Login user and return JWT token | ❌ |
| POST | /api/users/register/ | Register new user | ❌ |
| POST | /api/users/logout/ | Logout from user and Invalidate JWT Token | ✅ |
| POST | /api/users/refresh/ | Refresh the access Token | ✅ |
| POST | /api/auth/reset/ | Send Password reset email | ❌ |
| GET | /api/auth/accounts/password/reset/verify/?code=<code> | Verify the reset password code | ❌ |
| POST | /api/auth/password/reset/verified | Replace the old password with the new password | ❌ |
| GET | /api/conversations/ | Get all user conversations | ✅ |
| POST | /api/conversations/create/ | Create new conversation | ✅ |
| GET | /api/conversations/{id}/ | Get single conversation details | ✅ |
| PATCH | /api/conversations/update/{id}/ | Update conversation | ✅ |
| DELETE | /api/conversations/delete/{id}/ | Delete conversation | ✅ |
| GET | /api/conversations/messages/{id}/ | Get conversation messages | ✅ |
| POST | /api/conversations/join/{id}/ | Join a Conversation | ✅ |
| POST | /api/conversations/message/create/{conversation_id}/ | Send a message to a conversation | ✅ |
| PATCH | /api/conversations/messages/update/{id}/ | Edit a message | ✅ |
| DELETE | /api/conversations/messages/delete/{id}/ | Delete a message | ✅ |
| WS | /ws/chat/{conversation_id}/{conversation_name}/?token={access_token} | WebSocket connection for real-time chat | ✅ |



----------------------------------------------------------------------


## 🔒 Security Considerations

-   JWT expiration & refresh
-   Secure WebSocket connections (wss:// in production)
-   Input validation & sanitization

----------------------------------------------------------------------

# 🗄️ Database Schema

This project uses a relational database structure built with Django ORM.


## 📌 Entity Relationship Overview

- A **User** can create many conversations.
- A **Conversation** can have many members.
- A **Conversation** can have many messages.
- A **Message** belongs to one conversation.
- A **Message** is sent by one user.


# 👤 Users Table

### Model: `MyUser`
Extends `EmailAbstractUser`

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| id | BigAutoField | PK | Primary Key |
| username | CharField(150) | Unique, Required | Used for login |
| email | EmailField | Required | User email |
| full_name | CharField(80) | Optional | Full name |
| profile_image | ImageField | Default provided | Profile picture |
| is_active | Boolean | Default=True | Account status |
| is_staff | Boolean | Default=False | Admin access |
| date_joined | DateTime | Auto | Registration date |

### 🔑 Authentication
- `USERNAME_FIELD = "username"`
- Email is required
- Managed by `EmailUserManager`


# 💬 Conversations Table

### Model: `Conversation`

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| id | BigAutoField | PK | Primary Key |
| conversation_name | CharField(256) | Required | Name of the conversation |
| conversation_description | TextField | Required | Description |
| conversation_created_by | ForeignKey(User) | DO_NOTHING | Creator of conversation |
| members | ManyToMany(User) | Related Name: members | Conversation participants |
| created_at | DateTimeField | auto_now_add=True | Creation timestamp |
| emoji | TextField(20) | Required | Conversation emoji |
| color | TextField(30) | Required | UI color identifier |



### 🔗 Relationships

- **One-to-Many**
  - One user ➝ many created conversations
- **Many-to-Many**
  - Conversation ↔ Users (members)

Django automatically creates an intermediate table:
conversation_members  With:

| Field | Type |
|-------|------|
| id | PK |
| conversation_id | FK |
| myuser_id | FK |



# 📨 Messages Table

### Model: `Message`

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| id | BigAutoField | PK | Primary Key |
| conversation | ForeignKey(Conversation) | CASCADE | Related conversation |
| message_content | CharField(1024) | Required | Message text |
| message_sender | ForeignKey(User) | CASCADE | Sender |
| message_sent_at | DateTimeField | auto_now_add=True | Sent timestamp |

---

### 🔗 Relationships

- One Conversation ➝ Many Messages
- One User ➝ Many Messages



----------------------------------------------------------------------

## 🛠 Installation

### 1️⃣ Clone Repository

    git clone https://github.com/amr-zz/chatting-app.git
    cd chatting-app

### 2️⃣ Create Virtual Environment

    python -m venv venv
    source venv/bin/activate

### 3️⃣ Install Dependencies

    pip install -r requirements.txt


### 4️⃣ Apply Migrations

    python manage.py migrate

### 5️⃣ Create Superuser (Optional)

    python manage.py createsuperuser

### 6️⃣ Configure the Installed Apps

    INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'channels',
    'chat',
    'authemail',
    'frontend'
    ]

----------------------------------------------------------------------

## 🧠 Redis Channel Layer Configuration

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }

----------------------------------------------------------------------

### ✅ Finally, Run the server!

    python manage.py runserver

----------------------------------------------------------------------

## 📄 License

Copyright (c) 2026 Amr Mohamed

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
