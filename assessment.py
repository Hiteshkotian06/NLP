import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import textstat
from textblob import TextBlob as tb
from nltk.tokenize import word_tokenize, sent_tokenize

input_file = pd.read_excel(
    r"C:\Users\HITESH KOTIAN\OneDrive\Desktop\Blackcoffer\New folder\Input.xlsx"
)

output_file = "Output Data Structure"
os.makedirs(output_file, exist_ok=True)


# To get url and get the content present inside them, use request and BeautifulSoup
def get_url(url):
    url_receive = requests.get(url)
    soup = BeautifulSoup(url_receive.content, "lxml")

    # To extract the title from the url
    title = soup.find("title").get_text()

    # To get the main content as there are many things we just want the article text which starts from the
    # div having class = td-post-content taddiv-type but it is inside a container of class main-content

    main_content = soup.find("div", class_="td-main-content")
    start_point = None

    if main_content:
        start_point = main_content.find("div", class_="td-post-content tagdiv-type")

    end_point = soup.find("h1", class_="wp-block-heading", string="Contact Details")
    article_text = ""

    if start_point:
        # If there are any direct children elements like <h1>,<h2>, <p>, etc., include them in the text
        for child in start_point.children:
            if child.name in ["p", "h1", "h2", "h3", "h4", "ul", "li"]:
                article_text += child.get_text() + "\n"

        # Now it goes on untill the next siblings of the end_point or footer is reached
        for sibling in start_point.find_next_siblings():
            if sibling == end_point:
                break
            if sibling.name in ["p", "h1", "h2", "h3", "h4", "ul", "li"]:
                article_text += sibling.get_text() + "\n"
            elif sibling.name == "footer":
                break
    return title, article_text


# To lower all the text and remove all the punctuations
def process_data(text):
    text = text.lower()
    result = re.sub(r"[^\w\s]", "", text)
    return result


# Text analysis
def sia_scores(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)


def polarity(text):
    return tb(text).sentiment.polarity


def subjectivity(text):
    return tb(text).sentiment.subjectivity


def avg_sent_length(text):
    words = len(word_tokenize(text))
    sent = len(sent_tokenize(text))
    return words / sent if sent > 0 else 0


def perct_complex_words(text):
    words = word_tokenize(text)
    complex_words = [word for word in words if textstat.syllable_count(word) >= 3]
    return len(complex_words) / len(words) * 100 if len(words) > 0 else 0


def fog_index(text):
    return textstat.gunning_fog(text)


def avg_num_word_sent(text):
    words = len(word_tokenize(text))
    sent = len(sent_tokenize(text))
    return words / sent if sent > 0 else 0


def complex_word_count(text):
    words = word_tokenize(text)
    return sum(1 for word in words if textstat.syllable_count(word) >= 3)


def word_count(text):
    return len(word_tokenize(text))


def syllables_per_word(text):
    words = word_tokenize(text)
    return (
        sum(textstat.syllable_count(word) for word in words) / len(words)
        if len(words) > 0
        else 0
    )


def personal_pronoun(text):
    words = word_tokenize(text)
    personal_pronouns = [
        "i",
        "me",
        "we",
        "us",
        "you",
        "he",
        "him",
        "she",
        "her",
        "they",
        "them",
        "myself",
        "ourselves",
        "yourself",
        "yourselves",
        "himself",
        "herself",
        "itself",
        "themselves",
    ]
    return sum(1 for word in words if word in personal_pronouns)


def avg_word_length(text):
    words = word_tokenize(text)
    char_len = sum(len(word) for word in words)
    return char_len / len(words) if len(words) > 0 else 0


# Above i made all the fuctions now need to give the input to all the functions and get the output
# Make a list name data where we will store all the datas and later convert it to excel file
data = []
for index, row in input_file.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]

    try:
        title, article_text = get_url(url)
        article_text = process_data(article_text)

        # To save article file
        file_name = f"assessment_output_file_{url_id}.txt"
        file_path = os.path.join(output_file, file_name)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(title + "\n")
            file.write(article_text)

        #  Here are all the text analysis and columns for our output
        text_analysis = {}
        text_analysis["URL_ID"] = url_id
        text_analysis["URL"] = url
        text_analysis["Positive Score"] = sia_scores(article_text)["pos"]
        text_analysis["Negative Score"] = sia_scores(article_text)["neg"]
        text_analysis["Polarity Score"] = polarity(article_text)
        text_analysis["Subjectivity Score"] = subjectivity(article_text)
        text_analysis["Avg Sentence Length"] = avg_sent_length(article_text)
        text_analysis["Percentage of Complex Words"] = perct_complex_words(article_text)
        text_analysis["Fog Index"] = fog_index(article_text)
        text_analysis["Avg Number of Words Per Sentence"] = avg_num_word_sent(
            article_text
        )
        text_analysis["Complex Word Count"] = complex_word_count(article_text)
        text_analysis["Word Count"] = word_count(article_text)
        text_analysis["Syllable Per Word"] = syllables_per_word(article_text)
        text_analysis["Personal Pronouns"] = personal_pronoun(article_text)
        text_analysis["Avg Word Length"] = avg_word_length(article_text)

        data.append(text_analysis)
        print(f"{url_id} worked fine")

    except Exception as e:
        print(f"{url_id} failed to work: {e}")

# Convert to DataFrame and save to Excel
df = pd.DataFrame(data)
df.to_excel(os.path.join(output_file, "Output Data Structure.xlsx"), index=False)

print(f"Textual analysis results saved to {os.path.join(output_file, 'output.xlsx')}")
