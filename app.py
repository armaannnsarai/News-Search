from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///topics.db' 
db = SQLAlchemy(app)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/save_topic', methods=['POST'])
def save_topic():
    topic_name = request.form['topic']
    new_topic = Topic(name=topic_name)
    db.session.add(new_topic)
    db.session.commit()
    return redirect(url_for('news', topic=topic_name))

@app.route('/news')
def news():
    topic = request.args.get('topic')
    news_data = fetch_news(topic)
    return render_template('news.html', topic=topic, news_data=news_data)

def fetch_news(topic):
    api_key = 'apikey'
    url = f'https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}'
    print(url)
    response = requests.get(url)
    return response.json().get('articles', [])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
