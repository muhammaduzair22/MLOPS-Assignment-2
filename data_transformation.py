import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Define dawn_articles and bbc_articles variables
dawn_articles = []
bbc_articles = []

# Function for data preprocessing
def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text.lower())
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    # Join tokens back into a string
    preprocessed_text = ' '.join(lemmatized_tokens)
    return preprocessed_text

# Load data from CSV files
def load_from_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({'title': row['title'], 'description': row['description']})
    return data

# Load data from CSV files into dawn_articles and bbc_articles
dawn_articles = load_from_csv('dawn_articles.csv')
bbc_articles = load_from_csv('bbc_articles.csv')

# Apply preprocessing to Dawn.com articles
for article in dawn_articles:
    article['description'] = preprocess_text(article['description'])

# Apply preprocessing to BBC.com articles
for article in bbc_articles:
    article['description'] = preprocess_text(article['description'])

# Save the preprocessed data to new CSV files
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in data:
            writer.writerow(article)

# Save preprocessed Dawn.com articles to CSV
save_to_csv(dawn_articles, 'preprocessed_dawn_articles.csv')

# Save preprocessed BBC.com articles to CSV
save_to_csv(bbc_articles, 'preprocessed_bbc_articles.csv')
