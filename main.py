# project: pubmed_search
# file: main.py
# auth: bosoagalaxy@gmail.com
# desc: search pubmed with specific topic and generate wordcloud and sentiment analysis

import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import nltk
import ssl
'''
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("vader_lexicon")
'''
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

def find_abstract(search_link):
    response = requests.get(search_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    abstract = None

    abstract_tag = soup.find('div', class_ = 'abstract-content selected')
    print(abstract_tag)
    if (abstract_tag != None):
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
                print(len(results))
                break

            title_tag = result.find('a', class_='docsum-title')
            title = title_tag.get_text() if title_tag else "N/A"

            #abstract_tag = result.find('div', class_='abstract')
            abstract_tag = result.find('div', class_='full-view-snippet')
            abstract = abstract_tag.get_text() if abstract_tag else "N/A"

            link_tag = result.find('span', class_='docsum-pmid')
            #link = 'http://www.ncbi.nlm.nih.gov/pubmed/' + link_tag.get_text() +'/'
            link = 'https://pubmed.ncbi.nlm.nih.gov/' + link_tag.get_text() +'/'
            print(link)
            abstract_whole = find_abstract(link)

            if (abstract_whole != None):
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



    # Create a SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()

    # Example new text input
    new_text = text

    # Analyze sentiment of the new text
    sentiment_scores = sid.polarity_scores(new_text)

    # Display sentiment scores
    print("Sentiment Scores:", sentiment_scores)

    # Determine overall sentiment label
    if sentiment_scores['compound'] >= 0.05:
        sentiment_label = 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'

    print("Overall Sentiment:", sentiment_label)

    # Plot the sentiment scores
    labels = ['Negative', 'Neutral', 'Positive']
    values = [sentiment_scores['neg'], sentiment_scores['neu'], sentiment_scores['pos']]

    plt.bar(labels, values, color=['red', 'gray', 'green'])
    plt.title('Sentiment Analysis')
    plt.xlabel('Sentiment')
    plt.ylabel('Score')
    plt.show()

