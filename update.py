name: Update Portfolio Prices

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

# ŠI DALIS SUTEIKIA ROBOTUI TEISĘ ĮRAŠYTI PAKEITIMUS
permissions:
  contents: write

jobs:
  update-portfolio:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install yfinance

      - name: Run update script
        run: python update.py

      - name: Commit and push changes
        run: |
          git config --global user.name "Portfolio Bot"
          git config --global user.email "bot@github.com"
          git add portfolio.json
          git diff-index --quiet HEAD || git commit -m "Auto-update prices [skip ci]"
          git push
