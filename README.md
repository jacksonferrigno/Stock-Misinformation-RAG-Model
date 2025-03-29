# Stock Misinformation RAG Model

This project is an educational demonstration of how a Retrieval-Augmented Generation (RAG) system can be used to generate **plausible but misleading financial advice** using real stock data and news headlines.

## 🔍 What It Does

- Retrieves real stock price trends via `yfinance`
- Pulls recent news headlines via RSS
- Stores stock info in a Pinecone vector database
- Uses OpenAI GPT-3.5 Turbo to generate confidently wrong investment advice
- Returns responses in Markdown format for frontend rendering
