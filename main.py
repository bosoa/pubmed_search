# project: pubmed_search
# file: main.py
# auth: bosoagalaxy@gmail.com
# desc: search pubmed with specific topic and generate wordcloud

import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def find_abstract(search_link):
    response = requests.get(search_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    abstract_tag = soup.find('div', class_ = 'abstract-content selected')
    abstract = abstract_tag.get_text()

    return abstract


def search_pubmed(keyword, max_results=10):
    base_url = "https://pubmed.ncbi.nlm.nih.gov"
    search_url = f"{base_url}/?term={keyword.replace(' ', '+')}"
    email = 'jihwanpark@dankook.ac.kr'

    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []

        for result in soup.find_all('article', class_='full-docsum'):
            if len(results) >= max_results:
                break

            title_tag = result.find('a', class_='docsum-title')
            title = title_tag.get_text() if title_tag else "N/A"

            #abstract_tag = result.find('div', class_='abstract')
            abstract_tag = result.find('div', class_='full-view-snippet')
            abstract = abstract_tag.get_text() if abstract_tag else "N/A"

            link_tag = result.find('span', class_='docsum-pmid')
            link = 'http://www.ncbi.nlm.nih.gov/pubmed/' + link_tag.get_text() +'/'

            abstract_whole = find_abstract(link)

            results.append({'title': title, 'abstract': abstract_whole, 'link': link})


        return results
    else:
        print("Failed to retrieve search results.")
        return []

if __name__ == "__main__":
    keyword = input("Enter a keyword to search on PubMed: ")
    max_results = int(input("Enter the maximum number of results to retrieve: "))

    search_results = search_pubmed(keyword, max_results)
    whole_abstract = ''

    print(f"Found {len(search_results)} results for '{keyword}':\n")
    for idx, result in enumerate(search_results, start=1):
        print(f"Result {idx}:\nTitle: {result['title']}\nAbstract: {result['abstract']}\nLink: {result['link']}\n")
        whole_abstract = whole_abstract + ' ' + result['abstract']

    # Generate the word cloud
    #text = search_results[0]['abstract']
    text = whole_abstract
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
