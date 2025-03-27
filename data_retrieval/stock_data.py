import yfinance as yf
from datetime import datetime, timedelta
import feedparser

def get_stock_summary(ticker):
    try:
        # get ticker instance configured
        stock = yf.Ticker(ticker)
        # get 7 day period
        hist = stock.history(period="7d")
        
        if hist.empty:
            return {"error": "No historical data found"}
        
        # get closing prices 
        closes = hist['Close'].tolist()
        dates = hist.index.strftime('%Y-%m-%d').tolist()
        
        if len(closes)<2:
            return {"error": "Not enough information"}
        
        # get trend
        pct_change = ((closes[-1]-closes[0])/closes[0]) *100
        trend =(
            "upward" if pct_change >1 else
            "downward" if pct_change <-1 else
            "flat"
        )
        return  {
            "ticker": ticker.upper(),
            "date_range": f"{dates[0]} to {dates[-1]}",
            "percent_change": round(pct_change, 2),
            "trend": trend,
            "closing_prices": list(zip(dates, map(lambda x: round(x, 2), closes)))
        }
    except Exception as e:
        return {"error": str(e)}
    
def get_stock_headlines(ticker, max_results=5):
    # get the url headline
    rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    # get the headlines--- if any
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        return ["No headlines found"]
    headlines = []
    
    for entry in feed.entries[:max_results]:
        # get headline profile
        published = entry.get("published", "Unkown date")
        title= entry.get("title", "No title")
        source =  entry.get("source", {}).get("title", "Yahoo Finance")
        headlines.append(f"{published}- {title} ({source})")
        
    return headlines

    
