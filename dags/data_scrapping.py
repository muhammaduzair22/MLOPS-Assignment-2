import requests
from bs4 import BeautifulSoup
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Function to extract links from dawn.com
def extract_dawn_links():
    url = 'https://www.dawn.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

# Function to extract titles and descriptions from dawn.com articles
def extract_dawn_articles():
    url = 'https://www.dawn.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    for article in soup.find_all('article'):
        title_tag = article.find('h2')
        if title_tag:
            title = title_tag.text.strip()
        else:
            title = "No title available"
        
        description_tag = article.find('p', class_='story_content')
        if description_tag:
            description = description_tag.text.strip()
        else:
            description = "No description available"
            
        articles.append({'title': title, 'description': description})
    return articles

# Function to extract links from bbc.com
def extract_bbc_links():
    url = 'https://www.bbc.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

# Function to extract titles and descriptions from bbc.com articles
def extract_bbc_articles():
    url = 'https://www.bbc.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    for article in soup.find_all('article'):
        title_tag = article.find('h2')
        if title_tag:
            title = title_tag.text.strip()
        else:
            title = "No title available"
        
        description_tag = article.find('p')
        if description_tag:
            description = description_tag.text.strip()
        else:
            description = "No description available"
            
        articles.append({'title': title, 'description': description})
    return articles

# Function for data preprocessing
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    preprocessed_text = ' '.join(lemmatized_tokens)
    return preprocessed_text

# Save data to CSV file
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in data:
            writer.writerow(article)

if __name__ == "__main__":
    # Extract data
    dawn_articles = extract_dawn_articles()
    bbc_articles = extract_bbc_articles()

    # Combine articles from both sources
    all_articles = dawn_articles + bbc_articles

    # Apply preprocessing to all articles
    for article in all_articles:
        article['description'] = preprocess_text(article['description'])

    # Save preprocessed data to CSV
    save_to_csv(all_articles, 'final_preprocessed_articles.csv')
