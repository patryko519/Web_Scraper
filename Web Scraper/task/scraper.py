import string
import os
import requests
import shutil
from bs4 import BeautifulSoup


def clean_title(title):
    return title.translate(str.maketrans("", "", string.punctuation)).replace(" ", "_")


def save_articles(number_of_pages, article_type):
    for page_number in range(1, number_of_pages + 1):
        nature_url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={page_number}'
        response = requests.get(nature_url)
        try:
            shutil.rmtree(f'Page_{page_number}')
        except FileNotFoundError:
            None
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
            article = soup.find_all('article')
            os.mkdir(f"Page_{page_number}")
            os.chdir(f'./Page_{page_number}')
            for content in article:
                if content.find('span', {'data-test': 'article.type'}).text.strip() == article_type:
                    url_of_article = f"http://nature.com{content.find('a').get('href')}"
                    title_of_article = clean_title(content.find('a').text.strip())
                    print(title_of_article)
                    temp_response = requests.get(url_of_article)
                    temp_soup = BeautifulSoup(temp_response.content, 'html.parser')
                    article_body = temp_soup.find('div', {'class': 'c-article-body'}).text.strip()
                    with open(f"{title_of_article}.txt", "wb") as file:
                        file.write(article_body.encode('UTF-8'))
            os.chdir('../')
        else:
            print(f"\nThe URL returned {response.status_code}!")


page_num = int(input())
art_type = input()
save_articles(page_num, art_type)
