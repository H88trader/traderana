# This is a python package for analyzing trades

## Download and install python for windows

- Remember to add python to path
- Disable path length limit
- Plenty tutorial online, e.g. https://youtu.be/uDbDIhR76H4

## Install sublime for windows (optional)

- One of the tutorial online https://youtu.be/gsOnPiSmR_w


## Install git for windows (optional)

- One of the tutorial online https://youtu.be/2j7fD92g-gE

## Install traderana

- Install for users 

   - Run "python -m pip install git+https://github.com/H88trader/traderana.git" in CMD

- Install for developers
   
   - Go to https://github.com/H88trader/traderana
   - In Code, choose "Download Zip"
   - Unzip the file to your prefered directory, I place in D:\myLib\traderana
   - Install all requirement, "pip install -r requirements.txt" 
   - Set enviroment for traderana

       - Search in the search bar: environment variables
       - Choose Advanced
       - Choose Enviroment Variables
       - Add D:\myLib\traderana to PYTHONPATH for user.

## Import trades

- Create a template directory in imports

- In template directory, create 4 directories

   - import_close_trades_jointly
   - import_close_trades_separately
   - import_open_trades_jointly
   - import_open_trades_separately

- Copy imports directory everyday 

- Import our trades into 4 subdirectories by Trades_Broker_0.xlsx

- Run track.py to import trades and analyze trades