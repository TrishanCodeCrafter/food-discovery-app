from flask import Flask
from database import init_db  # Database setup
from routes import api_blueprint  # Importing routes

# Initialize Flask App
app = Flask(__name__, template_folder="templates")

# Configure database (Example: SQLite)
app.config.from_pyfile('config.py')
# Initialize database tables
init_db()

# Register API routes from routes.py
app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    app.run(debug=True)  # Start the Flask server
