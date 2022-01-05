from traderana import importTrades
from traderana import analyzeTrades

if __name__ == "__main__":

	dataDir = '.'


	#date    = datetime.datetime.strptime('2021-12-29', '%Y-%m-%d').date()
	#date    = datetime.datetime.today().date()
	#dirname = "{}/imports/{}".format(dataDir, date.strftime('%Y-%m-%d') )
	#import_all_trades_from_one_dir(dirname, dataDir)

	importTrades.import_all_trades_from_all_dir(dataDir)

	analyzeTrades.analyze_all_trades_and_strategies(dataDir)