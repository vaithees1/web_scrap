from flask import Flask, request, jsonify
from scraper import scrape_website
from database import Content, get_db
from rag_model import answer_query
from sqlalchemy.orm import Session

app = Flask(__name__)

@app.route('/load', methods=['POST'])
def load_content():
    url = request.json.get('url')
    content = scrape_website(url)
    
    db: Session = next(get_db())
    db_content = Content(url=url, text=content)
    db.add(db_content)
    db.commit()
    
    return jsonify({"message": "Content loaded successfully."})

@app.route('/query', methods=['POST'])
def query_content():
    query = request.json.get('query')
    
    db: Session = next(get_db())
    contents = db.query(Content).all()
    contexts = [content.text for content in contents]
    
    answers = answer_query(query, contexts)
    
    return jsonify({"answers": answers})

if __name__ == '__main__':
    app.run(debug=True)
