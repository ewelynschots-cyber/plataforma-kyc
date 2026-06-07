from src.app import app, db
from src.database import db

# app já está importada

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)