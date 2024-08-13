Natural Language Processing
This project involves extracting URLs from an Excel file and conducting a comprehensive text and sentiment analysis on the articles found at those URLs. After retrieving the URLs, each article's content and title are extracted for analysis. The analysis includes calculating several key metrics: Positive Score, Negative Score, Polarity Score, Subjectivity Score, Average Sentence Length, Percentage of Complex Words, Fog Index, Average Number of Words per Sentence, Complex Word Count, Word Count, Syllables per Word, Personal Pronouns, and Average Word Length.

Documentation
(excel file)

Installation
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import re
import nltk from nltk.sentiment.vader
import SentimentIntensityAnalyzer
import textstat
from textblob import TextBlob as tb
from nltk.tokenize import word_tokenize, sent_tokenize


