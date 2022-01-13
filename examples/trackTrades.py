import os
import datetime
from traderana import importTrades
from traderana import analyzeTrades

if __name__ == "__main__":

	dataDir = '.'

	#Import one day trades
	#date    = datetime.datetime.strptime('2021-12-29', '%Y-%m-%d').date()
	#date    = datetime.datetime.today().date()
	#dirname = "{}/imports/{}".format(dataDir, date.strftime('%Y-%m-%d') )
	#import_all_trades_from_one_dir(dirname, dataDir)

	#Import all trades
	importTrades.import_all_trades_from_all_dir(dataDir)

	#Analyze trades
	dateBegin = datetime.datetime.strptime('2010-01-01', '%Y-%m-%d').date()
	dateEnd   = datetime.datetime.strptime('2030-01-09', '%Y-%m-%d').date()
	analyzeTrades.analyze_all_trades_and_strategies(dataDir, dateBegin, dateEnd)

	os.system("pause")
	