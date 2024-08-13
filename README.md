Natural Language Processing
This project involves extracting URLs from an Excel file and conducting a comprehensive text and sentiment analysis on the articles found at those URLs. After retrieving the URLs, each article's content and title are extracted for analysis. The analysis includes calculating several key metrics: Positive Score, Negative Score, Polarity Score, Subjectivity Score, Average Sentence Length, Percentage of Complex Words, Fog Index, Average Number of Words per Sentence, Complex Word Count, Word Count, Syllables per Word, Personal Pronouns, and Average Word Length.

Documentation
(excel file)

Installation <br>
import pandas as pd <br>
import os <br>
import requests <br>
from bs4 import BeautifulSoup<br>
import re<br>
import nltk from nltk.sentiment.vader<br>
import SentimentIntensityAnalyzer<br>
import textstat<br>
from textblob import TextBlob as tb<br>
from nltk.tokenize import word_tokenize, sent_tokenize
