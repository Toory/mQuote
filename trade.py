'''
Credit for the Cookie Crumb fuctions goes to bradlucas
https://github.com/bradlucas/get-yahoo-quotes-python/blob/master/get-yahoo-quotes.py
'''
import re
import sys
import time
import datetime
import requests
import argparse, textwrap

class Trade():
	
	def __init__(self,choose,helper=None,tempStart='',tempEnd=''):
		with open("stocks.txt","r+") as f:
			stocks = f.read().splitlines()  #splitlines to get line by line output from file
		f.close()
		counter = 0

		if choose == 1:
			start_date,end_date = self.daily()
		elif choose == 2:
			start_date,end_date = self.fromDate(tempStart,tempEnd)
		else:
			print('Wrong input, exiting...')
			exit(-1)
		#get the cookie and crumb for one stock, then uses the same cookie and crumb for all iterations
		cookie, crumb = self.get_cookie_crumb('ENI.MI')
		for stock in stocks:
			self.show(stock,helper)
			self.download_quotes(stock,counter,cookie,crumb,start_date,end_date)
			counter += 1
		if helper != None:
			# emits data to the GUI through a signal
			helper.send_signal.emit('[+] Done!')
			helper.finished.emit()

	def daily(self):
		start_date = self.get_now_epoch()
		tempEnd = str(datetime.date.today() + datetime.timedelta(days=1)) #get date format YYYY-MM-DD
		year,month,day = tempEnd.split('-')
		end_date = int(datetime.datetime(int(year),int(month),int(day)).timestamp())
		#print(time.strftime('%Y-%m-%d', time.localtime(start_date)), start_date)
		#print(time.strftime('%Y-%m-%d', time.localtime(end_date)), end_date)
		return start_date,end_date

	def fromDate(self,tempStart,tempEnd):
		print(tempStart,tempEnd)
		day,month,year = tempStart.split('/')
		start_date = int(datetime.datetime(int(year),int(month),int(day)).timestamp())
		day,month,year = tempEnd.split('/')
		end_date = int(datetime.datetime(int(year),int(month),int(day)).timestamp())
		return start_date,end_date

	def split_crumb_store(self,v):
		return v.split(':')[2].strip('"')

	def find_crumb_store(self,lines):
		# Looking for
		# ,"CrumbStore":{"crumb":"9q.A4D1c.b9
		for l in lines:
			if re.findall(r'CrumbStore', l):
				return l
		print("Did not find CrumbStore")

	def get_cookie_value(self,r):
		return {'B': r.cookies['B']}

	def get_page_data(self,symbol):
		url = "https://finance.yahoo.com/quote/%s/?p=%s" % (symbol, symbol)
		r = requests.get(url)
		cookie = self.get_cookie_value(r)
		# Code to replace possible \u002F value
		# ,"CrumbStore":{"crumb":"FWP\u002F5EFll3U"
		# FWP\u002F5EFll3U
		lines = r.content.decode('unicode-escape').strip(). replace('}', '\n')
		return cookie, lines.split('\n')

	def get_cookie_crumb(self,symbol):
		cookie, lines = self.get_page_data(symbol)
		crumb = self.split_crumb_store(self.find_crumb_store(lines))
		return cookie, crumb

	def get_data(self,symbol, start_date, end_date, cookie, crumb, counter):
		date = self.getformattedtoday()
		filename = '%s.txt' % (date)
		if (counter == 0):
			f = open(filename, 'a')
			firstline = '<ticker>,<name>,<date>,<per>,<open>,<high>,<low>,<close>,<vol>,<o/i>\n'
			f.write(firstline)
			f.close()
		url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s" % (symbol, start_date, end_date, crumb)
		response = requests.get(url, cookies=cookie)
		with open (filename, 'a') as f:
			for line in response.iter_lines():
				if (line[0] != 68):
					#f.write(line)
					#if response line has all 7 pieces of information
					if len(line.split(str.encode(','))) == 7:
						Date,Open,High,Low,Close,Adj_Close,Volume = line.split(str.encode(','))
						#checks that the result of Open is not null (to avoid parsing empty data)
						if Open.decode("utf-8") != 'null':
							year,month,day = Date.decode("utf-8").split("-")
							#writes stock data with the standard metastock import
							lineToWrite = symbol  + ',????,' + month + '/' + day + '/' + year  + ',D,' + Open.decode("utf-8")  + ',' + High.decode("utf-8")  + ',' + Low.decode("utf-8")  + ',' + Close.decode("utf-8")  + ',' + Volume.decode("utf-8")  + ',0\n'
							f.write(lineToWrite)
							print(lineToWrite)
		f.close()

	def get_now_epoch(self):
		# @see https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/#post5244109
		return int(time.time())

	def download_quotes(self,symbol,counter, cookie, crumb,start_date,end_date):
		self.get_data(symbol, start_date, end_date, cookie, crumb, counter)

	def getformattedtoday(self):
		return datetime.datetime.today().strftime('%Y%m%d')

	def show(self,symbol,helper):
		print("[+] Downloading %s !" % symbol)
		#string = f"[+] Downloading {symbol} from {time.strftime('%Y/%m/%d', time.localtime(start_date))} to {time.strftime('%Y/%m/%d', time.localtime(end_date))}!"
		if helper != None:
			# emits data to the GUI through a signal
			string = f"[+] Downloading {symbol}!"
			helper.send_signal.emit(string)
		return

if __name__ == '__main__':
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-d', '--daily',help='Get daily stocks', action='store_true')
	group.add_argument('-p', '--period',action='store', nargs=2,metavar=('startDate', 'endDate'),help=textwrap.dedent('''\
	Get stocks from a specified period
	Usage: python %(prog)s -p dd/mm/yyyy dd/mm/yyyy'''))
	args = parser.parse_args()

	if args.daily:
		Trade(1)
	elif args.period:
		startDate,endDate = args.period
		Trade(2,tempStart=startDate,tempEnd=endDate)
	else:
		parser.print_help()
