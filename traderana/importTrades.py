import os
import errno
import glob
import shutil
import datetime
import pandas as pd
import openpyxl

#====================================#
# All functions support the programs #
#====================================#
#Remove a file silently
def silentremoveFile(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

#Remove a directory silently
def silentremoveDir(dirname):
    try:
        shutil.rmtree(dirname)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

#=================================================#
# All functions read trades from broker csv files #
#=================================================#
def read_das_multiTrades(f):

		#Read file from csv file
		multiTrades = pd.read_csv(f)

		#Get multiTrades DataTime
		multiTrades['DateTime'] = multiTrades['Date'] + ' ' + multiTrades['Time']
		multiTrades['DateTime'] = pd.to_datetime( multiTrades['DateTime'] )

		#Change Side to S or B
		multiTrades['Side'] = multiTrades['Side'].str[0:1]

		#Change Sell side Qty number to negative
		multiTrades['sideNum'] = 1
		multiTrades.loc[ multiTrades['Side'] == 'S', 'sideNum' ] = -1
		multiTrades['Qty']  = multiTrades['Qty'] * multiTrades['sideNum']

		#Clean multiTrades
		multiTrades = multiTrades[['DateTime', 'Symb', 'Side', 'Price', 'Qty', 'Route', 'EcnFee', 'Commission', 'LocFee', 'Strategy']]

		return multiTrades

def read_tos_multiTrades(f):

		multiTrades = pd.read_csv(f)

		#Change columns name
		multiTrades = multiTrades.rename(columns={"Exec Time": "DateTime", "Symbol":"Symb"})

		#Change Exec Time to DateTime
		multiTrades['DateTime'] = pd.to_datetime( multiTrades['DateTime'] )

		#Change Side to S or B
		multiTrades['Side'] = multiTrades['Side'].str[0:1]

		#Change Side to S or B
		multiTrades['Route'] = 'TOS'

		#Change Side to S or B
		multiTrades['EcnFee'] = 0.0

		#Clean multiTrades
		multiTrades = multiTrades[['DateTime', 'Symb', 'Side', 'Price', 'Qty', 'Route', 'EcnFee', 'Commission', 'LocFee', 'Strategy']]

		return multiTrades

#=============================================================================#
# All functions that split trades by symb, strategy into open and close trades#
#=============================================================================#
def split_multiTrades_by_symb_strategy(multiTrades):

		#Group by Symb and Strategy
		gb = multiTrades.groupby(['Symb', 'Strategy'])

		#Split it and create new dataframe for each group
		splitTrades = [gb.get_group(x).reset_index(drop=True) for x in gb.groups] 

		return splitTrades

def split_multiTrades_to_singleTrades(multiTrades):

		#Sort multiTrades DataTime
		multiTrades = multiTrades.sort_values('DateTime', ascending=True).reset_index(drop=True)

		#Set cumsum of Qty number
		multiTrades['CQty'] = multiTrades['Qty'].cumsum()

		#Split MultiTrades in to singleTrades, which is stored into closeTrades and openTrades.
		closeTrades = []
		openTrades  = []

		ii = 0
		breakIndex  = multiTrades.index[ multiTrades['CQty'] == 0 ].to_list() 
		multiTrades = multiTrades.drop(columns=['CQty'])
		if ( len(breakIndex) != 0 ):

			#Split multiTrades by breakIndex
			for bi in breakIndex:
					closeTrades.append( multiTrades.iloc[ii:bi+1] ) 
					ii = bi+1

			#If last breakIndex is not the end of multiTrades, it is an openTrade
			if ( breakIndex[-1] != multiTrades.shape[0]-1):
				openTrades.append( multiTrades.iloc[breakIndex[-1]+1:] )

		else:

			#If no break index, full trade is a openTrades
			openTrades.append( multiTrades )

		return closeTrades, openTrades

def check_split_trades(closeTrades, openTrades):

		for ct in closeTrades:
				tradeStrategy =  ct['Strategy'].unique()
				if( len(tradeStrategy) != 1 ):
					print("Error!!! tradeStrategy is not unique", tradeStrategy)
					exit()

		for ot in openTrades:
				tradeStrategy =  ot['Strategy'].unique()
				if( len(tradeStrategy) != 1 ):
					print("Error!!! tradeStrategy is not unique", tradeStrategy)
					exit()

def split_MultiTrades(multiTrades):

		if multiTrades.empty:
				return [],[]

		splitTrades = split_multiTrades_by_symb_strategy(multiTrades)

		closeTrades = []
		openTrades  = []

		for st in splitTrades:

				ct, ot = split_multiTrades_to_singleTrades(st)
				closeTrades.extend( ct )
				openTrades.extend( ot )

		check_split_trades(closeTrades, openTrades)	
		
		return closeTrades, openTrades

#=========================================================#
# All functions that write open and close trades into dir #
#=========================================================#
def write_one_close_trade_to_dir(ct, dirname):

		os.makedirs(dirname, exist_ok=True)

		filename = '{}/closeTrades.csv'.format(dirname)

		if( os.path.exists(filename) ):

			oldTrades = pd.read_csv(filename)
			oldTrades['DateTime'] = pd.to_datetime( oldTrades['DateTime'] )

			ct['Number'] = oldTrades['Number'].max() + 1 
			ct = ct[['Number', 'DateTime', 'Symb', 'Side', 'Price', 'Qty', 'Route', 'EcnFee', 'Commission', 'LocFee', 'Strategy']]
			ct = ct.append(oldTrades)
			ct = ct.sort_values(by=['Number', 'DateTime'], ascending=[False, True])			

			ct.to_csv(filename, index=False) 

		else:

			ct['Number'] = 1
			ct = ct[['Number', 'DateTime', 'Symb', 'Side', 'Price', 'Qty', 'Route', 'EcnFee', 'Commission', 'LocFee', 'Strategy']]
			ct.to_csv(filename, index=False) 

def write_one_close_trade(ct, dataDir):

				#Write to All-strategies directory
		dirname  = "{}/strategy/All-strategies".format( dataDir )
		write_one_close_trade_to_dir(ct, dirname)

		#Write to the trade Strategy directory
		dirname =  "{}/strategy/{}".format( dataDir, ct['Strategy'].unique()[0] )
		write_one_close_trade_to_dir(ct, dirname)

def write_one_open_trade_to_dir(ot, dirname):

		os.makedirs(dirname, exist_ok=True)

		filename = '{}/openTrades.csv'.format(dirname)
		if( os.path.exists(filename) ):

			oldTrades = pd.read_csv(filename)
			oldTrades['DateTime'] = pd.to_datetime( oldTrades['DateTime'] )

			ot = ot.append(oldTrades)
			ot = ot.sort_values(by=['Symb', 'DateTime'], ascending=[True, True])			
			ot.to_csv(filename, index=False) 

		else:

			ot.to_csv(filename, index=False) 

def write_one_open_trade(ot, dataDir):

		#Write to All-strategies directory
		dirname  = "{}/strategy/All-strategies".format( dataDir ) 
		write_one_open_trade_to_dir(ot, dirname)

		#Write to the trade Strategy directory
		dirname = "{}/strategy/{}".format( dataDir, ot['Strategy'].unique()[0] )
		write_one_open_trade_to_dir(ot, dirname)

#===========================================================================#
# All functions that average trades into oneline and write into excel files #
#===========================================================================#
def create_empty_avg_trades():

		empty_trade  = {
								     'beginDate' : [ "" ],
								     'endDate'   : [ "" ],
								     'Symb'      : [ "" ],
								     'buyShare'  : [ "" ],
								     'sellShare' : [ "" ],
								     'buyFee'    : [ "" ],
								     'sellFee'   : [ "" ],
								     'locFee'    : [ "" ],
								     'buyFlow'   : [ "" ],
								     'sellFlow'  : [ "" ],
								     'buyPrice'  : [ "" ],
								     'sellPrice' : [ "" ],
								     'pnl'       : [ "" ],
								     'pnlPer'    : [ "" ],
								     'strategy'  : [ "" ],
                    }

		return pd.DataFrame( empty_trade )

def write_avg_open_close_trades_to_excel(dirname, avgCloseTrades, avgOpenTrades):

		filename =  dirname + "/avgTrades.xlsx"
	
		writer = pd.ExcelWriter(filename, engine='openpyxl')
	
		if avgCloseTrades.shape[0] == 0:
			avgCloseTrades = create_empty_avg_trades()
		avgCloseTrades.to_excel(writer, "closeTrades", index=False)

		if avgOpenTrades.shape[0] == 0:
			avgOpenTrades  = create_empty_avg_trades()
		avgOpenTrades.to_excel(writer, "openTrades", index=False)
	
		writer.save()

def get_avg_from_one_trade(oneTrade):

		oneTrade  = oneTrade.sort_values('DateTime', ascending=True).reset_index(drop=True)
		buyTrade  = oneTrade[ oneTrade['Qty']>0 ]
		sellTrade = oneTrade[ oneTrade['Qty']<0 ]

		beginDate = oneTrade['DateTime'].tolist()[0]
		endDate   = oneTrade['DateTime'].tolist()[-1]
		Symb      = oneTrade['Symb'].tolist()[0]
		buyShare  = buyTrade['Qty'].sum()
		sellShare = -sellTrade['Qty'].sum()
		buyFee    = buyTrade['EcnFee'].sum()  + buyTrade['Commission'].sum()
		sellFee   = sellTrade['EcnFee'].sum() + sellTrade['Commission'].sum() 
		locFee    = sellTrade['LocFee'].sum()
		buyFlow   = ( buyTrade['Price']*buyTrade['Qty'] ).sum() 
		sellFlow  = -( sellTrade['Price']*sellTrade['Qty'] ).sum() 
		buyPrice  = 0.0
		if(buyShare>0):
			buyPrice  = buyFlow  / buyShare
		sellPrice = 0.0
		if(sellShare>0):
			sellPrice = sellFlow / sellShare
		pnl       = sellFlow - buyFlow - buyFee - sellFee - locFee

		if( oneTrade['Side'].tolist()[0] == 'B' ):
				# Long percentage of a trade
				pnlPer = pnl/buyFlow
		else:
				# Short percentage of a trade
				pnlPer = pnl/sellFlow

		strategy  = oneTrade['Strategy'].tolist()[0]

		avgTrade = {
								'beginDate'           :  [	beginDate  ],
								'endDate'             :  [	endDate    ],
								'Symb'                :  [  Symb       ],
								'buyShare'            :  [	buyShare   ],
								'sellShare'           :  [	sellShare  ],
								'buyFee'              :  [	buyFee     ],
								'sellFee'             :  [	sellFee    ],
								'locFee'              :  [	locFee     ],
								'buyFlow'             :  [	buyFlow    ],
								'sellFlow'            :  [	sellFlow   ],
								'buyPrice'            :  [	buyPrice   ],
								'sellPrice'           :  [	sellPrice  ],
								'pnl'                 :  [	pnl        ],
								'pnlPer'              :  [	pnlPer     ],
								'strategy'            :  [  strategy   ],
			        	}

		avgTrade = pd.DataFrame( avgTrade )

		return avgTrade

def write_open_close_trades_to_avg_trades_excel(dirname):

		avgClose      = pd.DataFrame()			
		closefilename = dirname+"/closeTrades.csv"
		if( os.path.exists(closefilename) ):
			closeTrades  = pd.read_csv(closefilename)
			closeTrades['DateTime'] = pd.to_datetime( closeTrades['DateTime'] )

			gb = closeTrades.groupby(['Number'])
			allTrades = [gb.get_group(x).reset_index(drop=True) for x in gb.groups] 

			for oneTrade in allTrades:
				oneAvg   = get_avg_from_one_trade(oneTrade)
				avgClose = avgClose.append(oneAvg, ignore_index=True)

			avgClose  = avgClose.sort_values(by=['beginDate', 'Symb'] , ascending=[False, True]).reset_index(drop=True)

		avgOpen      = pd.DataFrame()
		openfilename = dirname+"/openTrades.csv"
		if( os.path.exists(openfilename) ):
			openTrades  = pd.read_csv(openfilename)
			openTrades['DateTime'] = pd.to_datetime( openTrades['DateTime'] )

			gb = openTrades.groupby(['Symb', 'Strategy'])
			allTrades = [gb.get_group(x).reset_index(drop=True) for x in gb.groups] 

			for oneTrade in allTrades:
				oneAvg  = get_avg_from_one_trade(oneTrade)
				avgOpen = avgOpen.append(oneAvg, ignore_index=True)

			avgOpen  = avgOpen.sort_values(by=['beginDate', 'Symb'] , ascending=[False, True]).reset_index(drop=True)
		
		write_avg_open_close_trades_to_excel(dirname, avgClose, avgOpen)	

def write_all_open_close_trades_to_excel(dataDir):

	workDir = "{}/strategy/*/".format( dataDir )
	all_dirname = [ f[:-1] for f in glob.glob(workDir) ]

	for dirname in all_dirname:
			write_open_close_trades_to_avg_trades_excel(dirname)


#===================================================#
# All functions that import trades to csv and excel #
#===================================================#
def import_close_trades_separately( dirname, dataDir ):

		closeTrades = []
		openTrades  = []

		tosfilename = "{}/import_close_trades_separately/Trades_Tos_*.csv".format( dirname )
		for f in glob.glob(tosfilename):

			multiTrades = read_tos_multiTrades(f)

			cts, ots = split_MultiTrades(multiTrades)

			closeTrades.extend( cts )
			openTrades.extend( ots )

		dasfilename = "{}/import_close_trades_separately/Trades_Das_*.csv".format( dirname )
		for f in glob.glob(dasfilename):

			multiTrades = read_das_multiTrades(f)

			cts, ots = split_MultiTrades(multiTrades)

			closeTrades.extend( cts )
			openTrades.extend( ots )

		if( len(openTrades)!=0 ):
			print("Error, this imports should not contain any open trades")
			print(openTrades)
			exit()

		for ct in closeTrades:
				write_one_close_trade(ct, dataDir)

def import_close_trades_jointly( dirname, dataDir ):

		multiTrades = pd.DataFrame()

		tosfilename = "{}/import_close_trades_jointly/Trades_Tos_*.csv".format( dirname )
		for f in glob.glob(tosfilename):
			multiTrades = multiTrades.append(read_tos_multiTrades(f))

		dasfilename = "{}/import_close_trades_jointly/Trades_Das_*.csv".format( dirname )
		for f in glob.glob(dasfilename):
			multiTrades = multiTrades.append(read_das_multiTrades(f))

		closeTrades, openTrades = split_MultiTrades(multiTrades)

		if( len(openTrades)!=0 ):
			print("Error, this imports should not contain any open trades")
			print(opentrades)
			exit()

		for ct in closeTrades:
				write_one_close_trade(ct, dataDir)

def import_open_trades_separately( dirname, dataDir ):

		tosfilename = "{}/import_open_trades_separately/Trades_Tos_*.csv".format( dirname )
		for f in glob.glob(tosfilename):

			multiTrades = pd.DataFrame()
	
			openfilename = "{}/strategy/All-strategies/openTrades.csv".format(dataDir)
			if( os.path.exists(openfilename) ):
				openTrades  = pd.read_csv(openfilename)
				openTrades['DateTime'] = pd.to_datetime( openTrades['DateTime'] )
				multiTrades = multiTrades.append(openTrades)
				for filename in glob.glob( "{}/strategy/*/openTrades.csv".format(dataDir) ):
					os.remove(filename)

			multiTrades= multiTrades.append( read_tos_multiTrades(f) )

			closeTrades, openTrades = split_MultiTrades(multiTrades)

			for ct in closeTrades:
					write_one_close_trade(ct, dataDir)
	
			for ot in openTrades:
					write_one_open_trade(ot, dataDir)

		dasfilename = "{}/import_open_trades_separately/Trades_Das_*.csv".format( dirname )
		for f in glob.glob(dasfilename):

			multiTrades = pd.DataFrame()

			openfilename = "{}/strategy/All-strategies/openTrades.csv".format(dataDir)
			if( os.path.exists(openfilename) ):
				openTrades  = pd.read_csv(openfilename)
				openTrades['DateTime'] = pd.to_datetime( openTrades['DateTime'] )
				multiTrades = multiTrades.append(openTrades)
				for filename in glob.glob( "{}/strategy/*/openTrades.csv".format(dataDir) ):
					os.remove(filename)
	
			multiTrades = multiTrades.append( read_das_multiTrades(f) )

			closeTrades, openTrades = split_MultiTrades(multiTrades)

			for ct in closeTrades:
					write_one_close_trade(ct, dataDir)
	
			for ot in openTrades:
					write_one_open_trade(ot, dataDir)

def import_open_trades_jointly( dirname, dataDir ):

		multiTrades = pd.DataFrame()

		openfilename = "{}/strategy/All-strategies/openTrades.csv".format(dataDir)
		if( os.path.exists(openfilename) ):
			opentrades  = pd.read_csv(openfilename)
			opentrades['DateTime'] = pd.to_datetime( opentrades['DateTime'] )
			multiTrades = multiTrades.append( opentrades )
			for filename in glob.glob( "{}/strategy/*/openTrades.csv".format(dataDir) ):
				os.remove(filename)		

		tosfilename = "{}/import_open_trades_jointly/Trades_Tos_*.csv".format( dirname )
		for f in glob.glob(tosfilename):
			multiTrades = multiTrades.append(read_tos_multiTrades(f))

		dasfilename = "{}/import_open_trades_jointly/Trades_Das_*.csv".format( dirname )
		for f in glob.glob(dasfilename):
			multiTrades = multiTrades.append(read_das_multiTrades(f))

		closeTrades, openTrades = split_MultiTrades(multiTrades)

		for ct in closeTrades:
				write_one_close_trade(ct, dataDir)

		for ot in openTrades:
				write_one_open_trade(ot, dataDir)


#====================================================#
# All functions that will be called by main function #
#====================================================#
def import_all_trades_from_one_dir(dirname, dataDir):

	print("Importing trades from directory {}".format(dirname))

	import_close_trades_separately( dirname, dataDir )
	import_close_trades_jointly( dirname, dataDir )
	import_open_trades_separately( dirname, dataDir )
	import_open_trades_jointly( dirname, dataDir )	

	write_all_open_close_trades_to_excel(dataDir)


def import_all_trades_from_all_dir(dataDir):

	#Remove current trades
	workDir     = "{}/strategy/*/".format( dataDir )
	all_dirname = [ f[:-1] for f in glob.glob(workDir) ]

	for dirname in all_dirname:
		silentremoveFile(dirname+"/closeTrades.csv")		
		silentremoveFile(dirname+"/openTrades.csv")		
		silentremoveDir(dirname+'/analyseTrades')
		silentremoveDir(dirname+'/analyseStrategies')

	#Get all list except "imports/imports_template/"
	workDir     = "{}/imports/*/".format( dataDir )
	excludeDir  = "{}/imports\\template\\".format( dataDir )
	all_dirname = [ f[:-1] for f in glob.glob(workDir) if f != excludeDir]

	for dirname in all_dirname:

		import_all_trades_from_one_dir(dirname, dataDir)
