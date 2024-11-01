import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    try:
        if pd.isna(text) or text is None:
            return ""
        text = str(text).lower()
        text = re.sub(r'[^a-z0-9\s?.!,]', '', text)
        tokens = word_tokenize(text)
        
        important_words = {'how', 'what', 'why', 'where', 'when', 'who', 'card', 'money', 'transfer', 'receive', 'exchange', 'rate'}
        tokens = [token for token in tokens if token not in stop_words or token in important_words]
        
        processed_text = ' '.join(tokens)
        return processed_text if processed_text.strip() else "empty_text"
        
    except Exception as e:
        print(f"Warning: Error preprocessing text: {str(e)}")
        return "error_text"