import json
import pandas as pd
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Load the JSON data
with open('jsondata.json', encoding='utf-8') as f:
    data = json.load(f)

# Convert JSON to DataFrame
df = pd.DataFrame(data)

# Replace empty strings with NaN and convert columns to appropriate types
df.replace('', pd.NA, inplace=True)
df['intensity'] = pd.to_numeric(df['intensity'], errors='coerce')
df['likelihood'] = pd.to_numeric(df['likelihood'], errors='coerce')
df['relevance'] = pd.to_numeric(df['relevance'], errors='coerce')
df['end_year'] = pd.to_numeric(df['end_year'], errors='coerce')
df['start_year'] = pd.to_numeric(df['start_year'], errors='coerce')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/yourdatabase'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intensity = db.Column(db.Float)
    likelihood = db.Column(db.Float)
    relevance = db.Column(db.Float)
    end_year = db.Column(db.Integer)
    start_year = db.Column(db.Integer)
    country = db.Column(db.String(50))
    topic = db.Column(db.String(50))
    region = db.Column(db.String(50))
    city = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'intensity': self.intensity,
            'likelihood': self.likelihood,
            'relevance': self.relevance,
            'end_year': self.end_year,
            'start_year': self.start_year,
            'country': self.country,
            'topic': self.topic,
            'region': self.region,
            'city': self.city,
        }

def init_db():
    db.create_all()
    if Data.query.first() is None:
        for _, row in df.iterrows():
            data_entry = Data(
                intensity=row['intensity'],
                likelihood=row['likelihood'],
                relevance=row['relevance'],
                end_year=row['end_year'],
                start_year=row['start_year'],
                country=row.get('country', None),
                topic=row.get('topic', None),
                region=row.get('region', None),
                city=row.get('city', None)
            )
            db.session.add(data_entry)
        db.session.commit()

@app.route('/api/data')
def get_data():
    filters = request.args.to_dict()
    query = Data.query
    for key, value in filters.items():
        query = query.filter(getattr(Data, key) == value)
    data = query.all()
    return jsonify([item.to_dict() for item in data])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
