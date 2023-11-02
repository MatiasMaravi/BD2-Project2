from flask import Flask
import psycopg2
app = Flask(__name__)
app.config['DATABASE_URI'] = 'postgresql://postgres:40101109@localhost/BaseII'

def get_db():
    db = getattr(app, 'db', None)
    if db is None:
        app.db = db = psycopg2.connect(app.config['DATABASE_URI'])
    return db

@app.teardown_appcontext
def close_db(error):
    if hasattr(app, 'db'):
        app.db.close()


from app import routes