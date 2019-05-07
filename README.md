<h1 align="center"> mQuote </h1>
<p align="center"> 
  <img src="https://github.com/Toory/mQuote/blob/master/stock.png"  width="120" height="120">
</p>


mQuote is an application that allows you to download daily and historical end-of-day quotes for stocks, index, ETF or mutual funds (using Yahoo Finance).  The data is stored in Metastock format.

## Installation

	git clone 'https://github.com/Toory/mQuote'
	cd mQuote
	pip install -r requirements.txt #Download all dependencies needed
	python mquoteGUI.py

## Usage
<p align="center"> 
  <img src="https://i.imgur.com/cawiGvW.gif">
</p>

The stock's quotes that the application will download need to be written one per line in a file called 'stocks.txt'. 
Only put the Ticker symbol of each stock, if you don't know it you can search the ticker sybol at https://finance.yahoo.com/ . 

**Daily Stocks tab**: Click on 'Get Daily Stocks' to download all quotes from the current day.

**History tab** : Choose a period (Start date and End date) and mQuote will download all quotes for that period of time.

All the data in the output file is stored in Metastock format.
