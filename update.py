import json
import yfinance as yf
from datetime import datetime

def update_portfolio():
    try:
        with open('portfolio.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Klaida: portfolio.json failas nerastas!")
        return

    print("Pradedamas kainų atnaujinimas...")

    for position in data['positions']:
        ticker_symbol = position['ticker']
        
        if ticker_symbol.lower() in ['cash', 'pinigai', 'dividendai', 'divai']:
            continue
            
        try:
            print(f"Ieškoma kaina įrankiui: {ticker_symbol}")
            ticker = yf.Ticker(ticker_symbol)
            todays_data = ticker.history(period='1d')
            if not todays_data.empty:
                current_price = todays_data['Close'].iloc[-1]
                position['currentPrice'] = round(float(current_price), 2)
                print(f"Sėkmingai atnaujinta {ticker_symbol}: €{position['currentPrice']}")
            else:
                print(f"Įspėjimas: Nepavyko gauti kainos {ticker_symbol}")
        except Exception as e:
            print(f"Klaida atnaujinant {ticker_symbol}: {e}")

    now = datetime.now()
    data['meta']['lastUpdated'] = now.strftime("%Y-%m-%d %H:%M UTC")

    with open('portfolio.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Portfolio sėkmingai atnaujintas!")

if __name__ == "__main__":
    update_portfolio()
