import requests
from bs4 import BeautifulSoup
import csv

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
        # Check if <h2> tag exists within the article
        title_tag = article.find('a')
        if title_tag:
            title = title_tag.text.strip()
        else:
            title = "No title available"
        
        # Check if <p> tag exists within the article for description
        description_tag = article.find('p', class_='story__content')
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
        # Check if <h3> tag exists within the article
        title_tag = article.find('h2')
        if title_tag:
            title = title_tag.text.strip()
        else:
            title = "No title available"
        
        # Check if <p> tag exists within the article
        description_tag = article.find('p')
        if description_tag:
            description = description_tag.text.strip()
        else:
            description = "No description available"
            
        articles.append({'title': title, 'description': description})
    return articles


if __name__ == "__main__":
    dawn_links = extract_dawn_links()
    print("Dawn.com Links:", dawn_links)

    dawn_articles = extract_dawn_articles()
    print("Dawn.com Articles:", dawn_articles)

    bbc_links = extract_bbc_links()
    print("BBC.com Links:", bbc_links)

    bbc_articles = extract_bbc_articles()
    print("BBC.com Articles:", bbc_articles)

# Function to save data to a CSV file
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in data:
            writer.writerow(article)

# Save Dawn.com articles to CSV
save_to_csv(dawn_articles, 'dawn_articles.csv')

# Save BBC.com articles to CSV
save_to_csv(bbc_articles, 'bbc_articles.csv')