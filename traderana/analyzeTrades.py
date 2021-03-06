import os
import glob
import datetime
import pandas as pd
import matplotlib.pyplot as plt

def analyze_trades_of_one_strategy_by_price(dirname, dateBegin, dateEnd):

		#Get Price Range
		priceRange = [ 0.0, 1.0, 2.0, 3.0, 5.0, 10.0, 15.0, 20.0, float('inf') ]

		#Read Trades
		filename =  dirname + "/avgTrades.xlsx"
		trades   = pd.read_excel(filename, sheet_name='closeTrades')		
		trades['date'] = pd.to_datetime(trades['beginDate']).dt.date
		trades  = trades[ (trades['date'] >= dateBegin) & (trades['date'] <= dateEnd) ].reset_index(drop=True) 
		if( trades.shape[0] == 0 ): return 

		#Split trades by price
		pR   = []
		bPnl = []
		bNum = []
		sPnl = []
		sNum = []
		lenRange = len(priceRange)
		for i in range(lenRange-1):
				ps = priceRange[i]
				pe = priceRange[i+1]

				pR.append( "{}-{}".format(ps, pe) )

				bPnl.append( trades[ (trades['buyPrice'] >=ps) & (trades['buyPrice'] <=pe) ]['pnl'].sum() )
				bNum.append( trades[ (trades['buyPrice'] >=ps) & (trades['buyPrice'] <=pe) ].shape[0] )

				sPnl.append( trades[ (trades['sellPrice']>=ps) & (trades['sellPrice']<=pe) ]['pnl'].sum() )
				sNum.append( trades[ (trades['sellPrice']>=ps) & (trades['sellPrice']<=pe) ].shape[0] )
		
		#Get analyse 
		analyse =  {
								 "priceRange" : pR,
                 "buyPnl"     : bPnl,
                 "buyNum"     : bNum,
                 "sellPnl"    : sPnl, 
                 "sellNum"    : sNum, 
	             }
		analyse = pd.DataFrame(analyse)
		analyse = analyse.iloc[::-1]

		#Create directory
		tradesDirname = dirname+"/analyseTrades"
		os.makedirs(tradesDirname, exist_ok=True)

		#Plot PNL by buy price
		fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 12))
		analyse.plot(ax=axes[1], kind='barh', x='priceRange', y='buyPnl', rot=0, subplots=True,sharey=True)
		analyse.plot(ax=axes[0], kind='barh', x='priceRange', y='buyNum', rot=0, subplots=True,sharey=True)
		plt.savefig(tradesDirname+"/pnlBuyPrice.png", bbox_inches='tight')
		plt.close(fig)

		#Plot PNL by sell price
		fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 12))
		analyse.plot(ax=axes[1], kind='barh', x='priceRange', y='sellPnl', rot=0, subplots=True,sharey=True)
		analyse.plot(ax=axes[0], kind='barh', x='priceRange', y='sellNum', rot=0, subplots=True,sharey=True)
		plt.savefig(tradesDirname+"/pnlSellPrice.png", bbox_inches='tight')
		plt.close(fig)

def analyze_trades_of_one_strategy_by_time(dirname, dateBegin, dateEnd):

		#Get Time Range
		timeRange = [ datetime.time(4,00,0), datetime.time(7,00,0), datetime.time(8,00,0), datetime.time(9,00,0),
		              datetime.time(9,30,0), datetime.time(11,0,0), datetime.time(14,0,0), datetime.time(16,0,0), 
		              datetime.time(20,0,0) 
		            ]

		#Read Trades
		filename       =  dirname + "/avgTrades.xlsx"
		trades         = pd.read_excel(filename, sheet_name='closeTrades')
		trades['date'] = pd.to_datetime(trades['beginDate']).dt.date
		trades  = trades[ (trades['date'] >= dateBegin) & (trades['date'] <= dateEnd) ].reset_index(drop=True) 
		if( trades.shape[0] == 0 ): return 		
		trades['time'] = pd.to_datetime( trades['beginDate'] ).dt.time

		#Split trades by time
		tR   = []
		tPnl = []
		tNum = []
		lenRange = len(timeRange)
		for i in range(lenRange-1):		
				ts = timeRange[i]
				te = timeRange[i+1]

				tR.append( "{}-{}".format( ts.strftime("%H:%M"), te.strftime("%H:%M") ) )
				tPnl.append( trades[ (trades['time'] >=ts) & (trades['time'] <=te) ]['pnl'].sum() )
				tNum.append( trades[ (trades['time'] >=ts) & (trades['time'] <=te) ].shape[0] )

		#Get analyse 
		analyse =  {
								 "timeRange" : tR,
                 "pnl"       : tPnl,
                 "num"       : tNum,
	             }
		analyse = pd.DataFrame(analyse) 
		analyse = analyse.iloc[::-1]

		#Create directory
		tradesDirname = dirname+"/analyseTrades"		
		os.makedirs(tradesDirname, exist_ok=True)

		#Plot PNL by trade time
		fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 12))
		analyse.plot(ax=axes[1], kind='barh', x='timeRange', y='pnl', rot=0, subplots=True,sharey=True)
		analyse.plot(ax=axes[0], kind='barh', x='timeRange', y='num', rot=0, subplots=True,sharey=True)
		plt.savefig(tradesDirname+"/pnlTime.png", bbox_inches='tight')
		plt.close(fig)

def analyze_trades_of_one_strategy_by_weekday(dirname, dateBegin, dateEnd):

		#Get Weekday Range
		weekRange = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday" ]

		#Read Trades
		filename          = dirname + "/avgTrades.xlsx"
		trades            = pd.read_excel(filename, sheet_name='closeTrades')
		trades['date'] = pd.to_datetime(trades['beginDate']).dt.date
		trades  = trades[ (trades['date'] >= dateBegin) & (trades['date'] <= dateEnd) ].reset_index(drop=True) 
		if( trades.shape[0] == 0 ): return 
		trades['weekday'] = pd.to_datetime( trades['beginDate'] ).dt.weekday	

		#Split trades by week
		wPnl = []
		wNum = []
		for i in range(len(weekRange)):
			wPnl.append( trades[ trades['weekday']==i ]['pnl'].sum() )
			wNum.append( trades[ trades['weekday']==i ].shape[0] )

		#Get analyse 
		analyse =  {
								 "weekRange" : weekRange,
                 "pnl"       : wPnl,
                 'num'       : wNum, 
	             }
		analyse = pd.DataFrame(analyse) 
		analyse = analyse.iloc[::-1]

		#Create directory
		tradesDirname = dirname+"/analyseTrades"		
		os.makedirs(tradesDirname, exist_ok=True)

		#Plot PNL by weekday
		fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 12))
		analyse.plot(ax=axes[1], kind='barh', x='weekRange', y='pnl', rot=0, subplots=True,sharey=True)
		analyse.plot(ax=axes[0], kind='barh', x='weekRange', y='num', rot=0, subplots=True,sharey=True)
		plt.savefig(tradesDirname+"/pnlWeekday.png", bbox_inches='tight')
		plt.close(fig)
		
def analyze_trades_of_one_strategy_by_duration(dirname, dateBegin, dateEnd):

		#Get trade duration Range
		durRange = [ 0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 40.0, 60.0, 120.0, 240.0, float('inf') ]

		#Read Trades
		filename          = dirname + "/avgTrades.xlsx"
		trades            = pd.read_excel(filename, sheet_name='closeTrades')
		trades['date'] = pd.to_datetime(trades['beginDate']).dt.date
		trades  = trades[ (trades['date'] >= dateBegin) & (trades['date'] <= dateEnd) ].reset_index(drop=True) 
		if( trades.shape[0] == 0 ): return 
		trades['dur']     = (trades['endDate']-trades['beginDate']).dt.total_seconds()/60.

		#Split trades by duration
		dR   = []
		dPnl = []
		dNum = []
		lenRange = len(durRange)
		for i in range(lenRange-1):
				ds = durRange[i]
				de = durRange[i+1]

				dR.append( "{}-{} min".format(ds, de) )
				dPnl.append( trades[ (trades['dur'] >=ds) & (trades['dur'] <=de) ]['pnl'].sum() )
				dNum.append( trades[ (trades['dur'] >=ds) & (trades['dur'] <=de) ].shape[0] )

		#Get analyse 
		analyse =  {
								 "durRange"  : dR,
                 "pnl"       : dPnl,
                 'num'       : dNum, 
	             }
		analyse = pd.DataFrame(analyse) 
		analyse = analyse.iloc[::-1]

		#Create directory
		tradesDirname = dirname+"/analyseTrades"		
		os.makedirs(tradesDirname, exist_ok=True)

		#Plot PNL by duration
		fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 12))
		analyse.plot(ax=axes[1], kind='barh', x='durRange', y='pnl', rot=0, subplots=True,sharey=True)
		analyse.plot(ax=axes[0], kind='barh', x='durRange', y='num', rot=0, subplots=True,sharey=True)
		plt.savefig(tradesDirname+"/pnlDuration.png", bbox_inches='tight')
		plt.close(fig)

def analyze_trades_of_one_strategy_generally(dirname, dateBegin, dateEnd):

		filename =  dirname + "/avgTrades.xlsx"

		trades = pd.read_excel(filename, sheet_name='closeTrades')
		trades['date'] = pd.to_datetime(trades['beginDate']).dt.date
		trades  = trades[ (trades['date'] >= dateBegin) & (trades['date'] <= dateEnd) ].reset_index(drop=True) 

		if trades.shape[0] > 0:

				totalProfit       	  = trades['pnl'].sum()
				maxProfitPerTrade 	  = trades['pnl'].max()
				maxLossPerTrade   	  = trades['pnl'].min()
				maxProfitPerPerTrade  = trades['pnlPer'].max()
				maxLossPerPerTrade    = trades['pnlPer'].min()

				totLocFee 				    = trades['locFee'].sum()
				totBuyFee 				    = trades['buyFee'].sum()
				totSellFee 				    = trades['sellFee'].sum()
				totFee  				      = totLocFee + totBuyFee + totSellFee
				maxBuyFlowPerTrade    = trades['buyFlow'].max()
				maxSellFlowPerTrade   = trades['sellFlow'].max()

				avgPnl     				    = trades['pnl'].mean()
				avgProfit 				    = trades[trades['pnl']>0.0]['pnl'].mean()
				avgLoss   				    = trades[trades['pnl']<0.0]['pnl'].mean()
				pnlRatio   				    = -avgProfit/avgLoss

				avgPnlPer             = trades['pnlPer'].mean()
				avgProfitPer          = trades[trades['pnlPer']>0.0]['pnlPer'].mean()
				avgLossPer            = trades[trades['pnlPer']<0.0]['pnlPer'].mean()
				pnlPerRatio           = -avgProfitPer/avgLossPer

				totTrades 		        = trades.shape[0]
				winTrades 		        = trades[trades['pnlPer']>0.0].shape[0]
				loseTrades		        = trades[trades['pnlPer']<0.0].shape[0]
				winRate   		        = winTrades/totTrades

				num                   = trades.shape[0]

				analyse               =  {
																	"strategy"             : [ dirname[11:]         ],
                                  "totalProfit"       	 : [ totalProfit       	  ],
                                  "maxProfitPerTrade" 	 : [ maxProfitPerTrade 	  ], 
                                  "maxLossPerTrade"   	 : [ maxLossPerTrade   	  ],
                                  "maxProfitPerPerTrade" : [ maxProfitPerPerTrade ],
                                  "maxLossPerPerTrade"   : [ maxLossPerPerTrade   ],
                                  "totLocFee" 				   : [ totLocFee 				    ],
                                  "totBuyFee" 				   : [ totBuyFee 				    ],
                                  "totSellFee" 				   : [ totSellFee 				  ],
                                  "totFee"  				     : [ totFee  				      ],
                                  "maxBuyFlowPerTrade"   : [ maxBuyFlowPerTrade   ],
                                  "maxSellFlowPerTrade"  : [ maxSellFlowPerTrade  ],
                                  "avgPnl"     				   : [ avgPnl     				  ], 
                                  "avgProfit" 				   : [ avgProfit 				    ],
                                  "avgLoss"   				   : [ avgLoss   				    ],
                                  "pnlRatio"   				   : [ pnlRatio   				  ], 
                                  "avgPnlPer"            : [ avgPnlPer            ],
                                  "avgProfitPer"         : [ avgProfitPer         ],
                                  "avgLossPer"           : [ avgLossPer           ],
                                  "pnlPerRatio"          : [ pnlPerRatio          ],
                                  "totTrades" 		       : [ totTrades 		        ],
                                  "winTrades" 		       : [ winTrades 		        ], 
                                  "loseTrades"		       : [ loseTrades		        ],
                                  "winRate"   		       : [ winRate   		        ],
                                  "num"                  : [ num                  ],
	                                }

				analyse               = pd.DataFrame(analyse) 

				#Get analyse of all trades
				tradesDirname = dirname+"/analyseTrades"		
				os.makedirs(tradesDirname, exist_ok=True)

				#Write analyse to file
				analyse.to_csv(tradesDirname+"/analyseTrades.csv", index=False)
	                                
				return analyse

		else:
			
				return pd.DataFrame() 


def analyze_trades_of_all_strategies(analyse, dataDir):

	#Get analyse of all strategies
	dirname = "{}/strategy/All-strategies/analyseStrategies".format(dataDir)
	os.makedirs(dirname, exist_ok=True)

	#Write analyseStrategies
	analyse.to_csv(dirname+"/analyseStrategies.csv", index=False)

	#Get totalProfit
	analyse = analyse.sort_values(by='totalProfit', ascending=True)	
	fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 12) )
	analyse.plot(ax=axes[1], kind='barh', x='strategy', y='totalProfit', rot=0, subplots=True,sharey=True,legend=None)
	analyse.plot(ax=axes[0], kind='barh', x='strategy', y='num', rot=0, subplots=True,sharey=True,legend=None)
	plt.savefig(dirname+"/totalProfit.png", bbox_inches='tight')
	plt.close(fig)

	#Get winRate
	analyse = analyse.sort_values(by='winRate', ascending=True)	
	fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 12))
	analyse.plot(ax=axes[1], kind='barh', x='strategy', y='winRate', rot=0, subplots=True,sharey=True,legend=None)
	analyse.plot(ax=axes[0], kind='barh', x='strategy', y='num', rot=0, subplots=True,sharey=True,legend=None)
	plt.savefig(dirname+"/winRate.png", bbox_inches='tight')
	plt.close(fig)

	#Get avgPnlPer
	analyse = analyse.sort_values(by='avgPnlPer', ascending=True)	
	fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 12))
	analyse.plot(ax=axes[1], kind='barh', x='strategy', y='avgPnlPer', rot=0, subplots=True,sharey=True,legend=None)
	analyse.plot(ax=axes[0], kind='barh', x='strategy', y='num', rot=0, subplots=True,sharey=True,legend=None)
	plt.savefig(dirname+"/avgPnlPer.png", bbox_inches='tight')
	plt.close(fig)

	#Get pnlPerRatio
	analyse = analyse.sort_values(by='pnlPerRatio', ascending=True)	
	fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 12))
	analyse.plot(ax=axes[1], kind='barh', x='strategy', y='pnlPerRatio', rot=0, subplots=True,sharey=True,legend=None)
	analyse.plot(ax=axes[0], kind='barh', x='strategy', y='num', rot=0, subplots=True,sharey=True,legend=None)
	plt.savefig(dirname+"/pnlPerRatio.png", bbox_inches='tight')
	plt.close(fig)

	#Get pnlRatio
	analyse = analyse.sort_values(by='pnlRatio', ascending=True)	
	fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 12))
	analyse.plot(ax=axes[1], kind='barh', x='strategy', y='pnlRatio', rot=0, subplots=True,sharey=True,legend=None)
	analyse.plot(ax=axes[0], kind='barh', x='strategy', y='num', rot=0, subplots=True,sharey=True,legend=None)
	plt.savefig(dirname+"/pnlRatio.png", bbox_inches='tight')
	plt.close(fig)


def analyze_all_trades_and_strategies(dataDir, dateBegin, dateEnd):

	#Get all strategy lists
	workDir     = "{}/strategy/*/".format( dataDir )
	all_dirname = [ f[:-1] for f in glob.glob(workDir) ]

	#Get analyse of each trades, write into each directory
	analyse = pd.DataFrame()

	for dirname in all_dirname:

		print( "Analyzing trades in directory {}".format(dirname[11:]) )

		analyze_trades_of_one_strategy_by_price(dirname, dateBegin, dateEnd)

		analyze_trades_of_one_strategy_by_time(dirname, dateBegin, dateEnd)

		analyze_trades_of_one_strategy_by_weekday(dirname, dateBegin, dateEnd)

		analyze_trades_of_one_strategy_by_duration(dirname, dateBegin, dateEnd)

		analyse = analyse.append( analyze_trades_of_one_strategy_generally(dirname, dateBegin, dateEnd) )

	print( "Analyzing trades by comparing different strategies" )
	analyze_trades_of_all_strategies(analyse, dataDir)