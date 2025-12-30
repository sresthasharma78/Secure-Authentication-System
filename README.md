🔐 Secure Authentication System

A secure and production-style authentication system built using **Flask**, **JWT**, **bcrypt**, and **MySQL**, following real-world security best practices.
🚀 Features
- User registration with **secure password hashing** (bcrypt)
- User login with **JWT-based authentication**
- Token expiration handling
- Protected routes using JWT verification
- Environment-based configuration for secrets
- Simple frontend for Register, Login, and Dashboard
 
🛠 Tech Stack
- **Backend:** Flask (Python)
- **Authentication:** JWT, bcrypt
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript
- **Security:** python-dotenv, flask-cors

🔒 Security Highlights
- Passwords are **never stored in plain text**
- JWT tokens used instead of server-side sessions
- Secrets managed using '.env' (not pushed to GitHub)
- Protected API routes using token middleware

📁 Project Structure
Secure-Authentication-System/
│
├── app.py
├── database.py
├── frontend/
│ ├── register.html
│ ├── login.html
│ └── dashboard.html
├── requirements.txt
├── .gitignore
└── README.md

▶️ How to Run Locally

1️⃣ Clone the repository

```
git clone https://github.com/sresthasharma78/Secure-Authentication-System.git
cd Secure-Authentication-System
```

2️⃣ Create and activate virtual environment

 python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Create .env file

Create a .env file in the project root and add:

SECRET_KEY=your_secret_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_database_password
DB_NAME=secure_auth

5️⃣ Run the application

python app.py
Backend will run at : http://127.0.0.1:5000
Open frontend/register.html in your browser to use the application.

📌 Future Enhancements
-Refresh token implementation
-Role-based access control
-OAuth login (Google / GitHub)
-Deployment on cloud platforms

👩‍💻 Author
Srestha Sharma

