# First, let's create the core AI/ML components for ocean hazard detection and social media analytics

# 1. Import necessary libraries
import pandas as pd
import numpy as np
import nltk
import re
import json
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import datetime

# Download NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

print("Libraries imported successfully!")