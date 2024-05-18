import json
from app import create_app, db
from models import Data

app = create_app()

with open('jsondata.json', encoding='utf-8') as f:
    data = json.load(f)

with app.app_context():
    db.create_all()
    
    for item in data:
        new_data = Data(
            end_year=item.get('end_year'),
            intensity=item.get('intensity'),
            sector=item.get('sector'),
            topic=item.get('topic'),
            insight=item.get('insight'),
            url=item.get('url'),
            region=item.get('region'),
            start_year=item.get('start_year'),
            impact=item.get('impact'),
            added=item.get('added'),
            published=item.get('published'),
            country=item.get('country'),
            relevance=item.get('relevance'),
            pestle=item.get('pestle'),
            source=item.get('source'),
            title=item.get('title'),
            likelihood=item.get('likelihood')
        )
        db.session.add(new_data)
    
    db.session.commit()
