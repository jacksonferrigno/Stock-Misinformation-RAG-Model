import os
from dotenv import load_dotenv
from pinecone import Pinecone

from data_retrieval.stock_data import get_stock_headlines, get_stock_summary

load_dotenv()

# Load config
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Init Pinecone v6 client
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)


def upsert_stock_data(ticker, texts, namespace=None):
    records = []
    for i, text in enumerate(texts):
        if not isinstance(text,str) or not text.strip():
            continue
        records.append({
            "id": f"{ticker}-{i}",
            "text": text, 
            "metadata": ticker  # Storing ticker as a flat string.
        })
    index.upsert_records(namespace=namespace or "", records=records)

def query_stock_data(query_text, top_k=5, namespace=None):
    query_payload = {
        "inputs": {
            "text": query_text  # Pinecone will embed this text on the fly.
        },
        "top_k": top_k
    }
    results = index.search(namespace=namespace or "", query=query_payload)
    return [hit['fields']['text'] for hit in results['result']['hits']]


if __name__ == "__main__":
    sp100_tickers = [
        "AAPL", "ABBV", "ABT", "ACN", "ADBE", "AIG", "AMD", "AMGN", "AMT", "AMZN",
        "AVGO", "AXP", "BA", "BAC", "BIIB", "BK", "BKNG", "BLK", "BMY", "BRK.B",
        "C", "CAT", "CHTR", "CL", "CMCSA", "COF", "COP", "COST", "CRM", "CSCO",
        "CVS", "CVX", "DHR", "DIS", "DOW", "DUK", "EMR", "EXC", "F", "FDX",
        "FOX", "FOXA", "GD", "GE", "GILD", "GM", "GOOG", "GOOGL", "GS", "HD",
        "HON", "IBM", "INTC", "JNJ", "JPM", "KHC", "KMI", "KO", "LIN", "LLY",
        "LMT", "LOW", "MA", "MCD", "MDLZ", "MDT", "MET", "META", "MMM", "MO",
        "MRK", "MS", "MSFT", "NEE", "NFLX", "NKE", "NVDA", "ORCL", "PEP", "PFE",
        "PG", "PM", "PYPL", "QCOM", "RTX", "SBUX", "SCHW", "SO", "SPG", "T",
        "TGT", "TMO", "TMUS", "TSLA", "TXN", "UNH", "UNP", "USB", "V", "VZ",
        "WBA", "WFC", "WMT", "XOM"
    ]

    for ticker in sp100_tickers:
        print(f"Fetching headlines and summary for {ticker}...")

        headlines = get_stock_headlines(ticker)
        summary_obj = get_stock_summary(ticker)

        summary_text = (
            f"{ticker} had a {summary_obj['trend']} trend from {summary_obj['date_range']} "
            f"with a {summary_obj['percent_change']}% change in price."
            if 'error' not in summary_obj else summary_obj['error']
        )

        combined = [summary_text] + headlines
        upsert_stock_data(ticker, combined, namespace=ticker)

        print(f"Inserted {len(combined)} records for {ticker}.")
