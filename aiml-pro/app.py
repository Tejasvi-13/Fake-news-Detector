from flask import Flask, render_template, request
import re
from textblob import TextBlob
import nltk
nltk.download('punkt')

app = Flask(__name__)

def analyze_news(text):
    """Analyze text for fake news indicators"""
    analysis = {
        'length': len(text),
        'word_count': len(text.split()),
        'sentiment': None,
        'clickbait': False,
        'all_caps': False,
        'excessive_punctuation': False
    }
    
    # Sentiment analysis
    blob = TextBlob(text)
    analysis['sentiment'] = blob.sentiment.polarity
    
    # Fake news indicators
    analysis['clickbait'] = any(word in text.lower() for word in 
                              ['shocking', 'unbelievable', 'must see', 'you won\'t believe'])
    analysis['all_caps'] = len(re.findall(r'\b[A-Z]{3,}\b', text)) > 3
    analysis['excessive_punctuation'] = text.count('!') + text.count('?') > 5
    
    # Calculate fake probability (simplified)
    fake_score = 0
    if analysis['clickbait']: fake_score += 30
    if analysis['all_caps']: fake_score += 20
    if analysis['excessive_punctuation']: fake_score += 20
    if analysis['sentiment'] < -0.5: fake_score += 30
    
    analysis['fake_probability'] = min(fake_score, 100)
    
    return analysis

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    news_text = request.form.get('news_text', '')
    if not news_text.strip():
        return render_template('index.html', error="Please enter some text")
    
    analysis = analyze_news(news_text)
    return render_template('result.html', 
                         text=news_text,
                         analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)