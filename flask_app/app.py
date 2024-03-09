from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

app = Flask(__name__)

# Database connection
DATABASE_URL = "postgresql://myuser:mypassword@postgres_db:5432/mydatabase"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@app.route('/')
def home():
    return jsonify({"message":'hi'})

@app.route('/apartments')
def get_customers():
    session = Session()
    apartments = session.execute(text("SELECT * FROM apartments_for_sale")).fetchall()
    session.close()
    return jsonify([ {name: row._mapping[name] for name in ['name', 'locality', 'price']} \
                    for row in apartments])


if __name__ == '__main__':
    app.run()
