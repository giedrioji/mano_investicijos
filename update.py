import json
import urllib.request

def get_yahoo_data(ticker):
    """Atsisiunčia duomenis iš Yahoo Finance API"""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            return res_data['chart']['result'][0]['meta']['regularMarketPrice']
    except Exception as e:
        print(f"Klaida gauti duomenis įmonės {ticker}: {e}")
        return None

# 1. Užkrauname tavo portfolio.json
with open('portfolio.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Gauname naujausią EUR/USD kursą (kiek dolerių kainuoja vienas euras)
# Kadangi JAV akcijos yra USD, o tavo bazė EUR, kainą dalinsime iš šio skaičiaus
eur_usd_rate = get_yahoo_data("EURUSD=X")
if not eur_usd_rate:
    eur_usd_rate = 1.08  # Atsarginis kursas, jei API nesuveiktų
print(f"Dabartinis EUR/USD kursas: {eur_usd_rate}")

# 3. Einame per visas pozicijas ir atnaujiname kainas
for p in data['positions']:
    ticker = p.get('yahoo')
    if ticker:
        raw_price = get_yahoo_data(ticker)
        if raw_price:
            # Jei akcija yra JAV biržoje (neturi galūnės .DE arba .PA), konvertuojame į EUR
            if ".DE" not in ticker and ".PA" not in ticker:
                price_in_eur = raw_price / eur_usd_rate
                print(f"{ticker}: JAV kaina ${raw_price:.2f} -> Konvertuota į EUR: {price_in_eur:.2f} €")
            else:
                price_in_eur = raw_price
                print(f"{ticker}: Europos kaina: {price_in_eur:.2f} €")
            
            # Įrašome naują kainą eurais
            p['currentPrice'] = round(price_in_eur, 2)

# 4. Atnaujiname paskutinio patikrinimo datą
from datetime import datetime
data['meta']['lastUpdated'] = datetime.now().strftime('%Y-%m-%d')

# 5. Išsaugome atnaujintus duomenis atgal į failą
with open('portfolio.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Visi duomenys sėkmingai atnaujinti!")
