#import packages
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import appdirs as ad
import pandas as pd
import numpy as np
import math
from pathlib import Path
import requests
import feedparser
import seaborn as sns
from bs4 import BeautifulSoup
import riskfolio as rp
import streamlit as st
import sqlite3
import yfinance as yf
from textblob import TextBlob  # Import TextBlob for sentiment analysis
from datetime import date, timedelta, datetime

ad.user_cache_dir = lambda *args: "/tmp"

# CSS Styles
def inject_css():
    st.markdown("""
    <style>
        /* General Page Styling */
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f6fa;
            color: #333;
            margin: 0;
            padding: 0;
        }

        /* Header Section */
        .header {
            background-color: #1f4e79;
            padding: 10px 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }

        .header h1 {
            color: white;
            font-size: 36px;
            margin: 0;
        }

        /* Ticker Section */
        .ticker-section {
            background-color: #ffffff;
            padding: 15px 20px;
            border-bottom: 1px solid #e3e3e3;
        }

        .ticker-section h2 {
            font-size: 20px;
            margin: 0;
            font-weight: bold;
            color: #1a73e8;
        }

        .ticker-section .metrics {
            display: flex;
            align-items: center;
            margin-top: 10px;
            gap: 10px;
        }

        .ticker-section .price {
            font-size: 32px;
            font-weight: bold;
            color: #d32f2f;
        }

        /* Chart Section */
        .chart-container {
            padding: 20px;
            background-color: #ffffff;
            margin: 20px auto;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .chart-container .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .chart-container .chart-header h3 {
            font-size: 18px;
            font-weight: bold;
        }

        .chart-container canvas {
            width: 100%;
            height: 300px;
        }

        /* Footer Section */
        .footer {
            background-color: #1d1f22;
            color: white;
            text-align: center;
            padding: 10px 0;
            font-size: 12px;
        }

        /* Highlight Colors */
        .highlight-positive {
            color: #388e3c; /* Green for positive changes */
        }

        .highlight-neutral {
            color: #616161; /* Grey for neutral changes */
        }

        .highlight-negative {
            color: #d32f2f; /* Red for negative changes */
        }

        /* News Cards */
        .news-card {
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }

        .news-card h4 {
            margin: 0;
            font-size: 18px;
            color: #333;
        }

        .news-card p {
            margin: 5px 0;
        }

        .news-card a {
            color: #1a73e8;
            text-decoration: none;
        }

        .news-card a:hover {
            text-decoration: underline;
        }
    </style>
    """, unsafe_allow_html=True)

# Inject CSS
inject_css()

# Set up the page
st.set_page_config(
    page_title="Investments App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define header
def render_header(title):
    st.markdown(f"""
    <div class="header">
        <h1>{title}</h1>
    </div>
    """, unsafe_allow_html=True)

# Define footer
def render_footer():
    st.markdown("""
    ---
    <div class="footer">
        <small>© 2024 International University of Japan. All rights reserved.</small>
    </div>
    """, unsafe_allow_html=True)

# Render Header
render_header("S&P 500 Features Analysis")

# Create Tabs
tabs = st.tabs(["🏠 Home", "🔎 Fundamental Analysis", "📈 Technical Analysis", "🚩 Risk Portfolio", "⚖️ Comparison", "🌐 News", "📧 Contacts"])

# Example Content for News Tab with Sentiment Analysis
with tabs[5]:
    st.header("📡 News")
    st.write("Stay updated with the latest news on your selected stock.")

    def extract_news_from_google_rss(ticker):
        """Fetch news articles for a given stock ticker using Google News RSS."""
        url = f"https://news.google.com/rss/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        news_articles = []
        for entry in feed.entries[:10]:  # Limit to the latest 10 articles
            published_date = datetime(*entry.published_parsed[:6])  # Convert to datetime
            news_articles.append({"title": entry.title, "url": entry.link, "date": published_date})
        return news_articles

    def analyze_sentiment(text):
        """Analyze the sentiment of the text using TextBlob."""
        analysis = TextBlob(text)
        sentiment = analysis.sentiment.polarity
        if sentiment > 0:
            return "Positive", sentiment
        elif sentiment < 0:
            return "Negative", sentiment
        else:
            return "Neutral", sentiment

    ticker_symbol_news = st.text_input("Enter stock ticker (e.g., AAPL, MSFT):", key="ticker_news")

    if ticker_symbol_news:
        try:
            # Fetch news for the given ticker
            news = extract_news_from_google_rss(ticker_symbol_news)
            if news:
                st.subheader(f"📰 Latest News for {ticker_symbol_news.upper()}")
                for article in news:
                    sentiment, score = analyze_sentiment(article['title'])
                    color_class = (
                        "highlight-positive" if sentiment == "Positive"
                        else "highlight-negative" if sentiment == "Negative"
                        else "highlight-neutral"
                    )
                    st.markdown(
                        f"""
                        <div class="news-card">
                            <h4>{article['title']}</h4>
                            <p><em>Published on: {article['date'].strftime('%Y-%m-%d %H:%M:%S')}</em></p>
                            <p><strong>Sentiment:</strong> <span class="{color_class}">{sentiment}</span></p>
                            <a href="{article['url']}" target="_blank">Read more</a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.warning("No news articles found for this ticker.")
        except Exception as e:
            st.error(f"An error occurred while fetching news: {e}")
    else:
        st.info("Enter a stock ticker above to fetch the latest news.")

# Footer
render_footer()
