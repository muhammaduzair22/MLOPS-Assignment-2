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
        title_tag = article.find('h2')
        if title_tag:
            title = title_tag.text.strip()
        else:
            title = "No title available"
        
        # Check if <p> tag exists within the article for description
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
    # Extract data
    dawn_links = extract_dawn_links()
    dawn_articles = extract_dawn_articles()
    bbc_links = extract_bbc_links()
    bbc_articles = extract_bbc_articles()

    # Save Dawn.com articles to CSV
    with open('dawn_articles.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in dawn_articles:
            writer.writerow(article)

    # Save BBC.com articles to CSV
    with open('bbc_articles.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in bbc_articles:
            writer.writerow(article)
