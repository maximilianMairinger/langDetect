from PyQt5 import QtWidgets, uic
import sys
from view import *
from modell import *


rateStrategieDictionary: dict[str, GetRateStrategy] = {
  "api": GetRateWithApi(),
  "offline": GetRateOffline()
}


class Controller:
  def __init__(self):
    """
    Starts the application
    """

    # Start the application
    app = QtWidgets.QApplication(sys.argv)
    self.view = Window(self)
    self.view.show()
    sys.exit(app.exec_())

    

  def reset(self):
    """
    Reset all inputs and the HTML field
    """
    self.view.clearHTML()
    self.view.clearInputs()

  def askForCurrencyChange(self, value, fromCurrency, toCurrency, live):
    """
    Ask for calculation
    """
    # Set status to abfragen... and clear output
    self.view.setStatus("Abfragen...")
    self.view.clearHTML()
    
    # Request
    ret = self.calculateValueInNewCurrency(value, fromCurrency, toCurrency, live)

    # If request went ok, set status to erfolgreich, otherwise print error
    if ret["ok"]:
      self.view.showResult(ret["res"])
      self.view.setStatus("Erflogreich")
    else: 
      try:
        if len(ret["msg"]) == 1:
          s = str(ret["msg"][0])
        else:
          s = str(ret["msg"])
      except Exception as e:
        str(ret["msg"])
        
      self.view.setStatus(s)

  def calculateValueInNewCurrency(self, value, fromCurrency, toCurrency, live):
    """
    Calculate the value of a quantety of a currency in other currencies
    Currency should be given in 3 letter form (e.g: EUR, USD)

    :value: How much of this currency should be calculated
    :fromCurrency: What is the currency you want to calculate from. Currency should be given in 3 letter form (e.g: EUR, USD)
    :toCurrency: What is the currency you want to calculate to. This can be a comma seperated string or a list. Currency should be given in 3 letter form (e.g: EUR, USD)
    :live: If true, use live data from the web
    :return: {ok: True, res: {...}} when everything went well. And {ok: False, msg: string} when something went wrong
    """

    # ---------- #
    # Parse args #
    # ---------- #

    # Parse live. Live may be a boolean or
    # a string (thus interpreated as via)
    if isinstance(live, str):
      via = live
    elif isinstance(live, bool):
      if live:
        via = "api"
      else: 
        via = "offline"
    else:
      via = "api"

    # Get strategy
    strategy = rateStrategieDictionary[via]

    # Parse toCurrency
    # Can be a string split with "," or a list or strings
    if isinstance(toCurrency, str):
      toCurrency = toCurrency.split(",")
    else:
      if not isinstance(toCurrency, list):
        toCurrency = [str(toCurrency)]
      else:
        for i in range(len(toCurrency)):
          toCurrency[i] = str(toCurrency[i])



    # Upper case everything
    for i in range(len(toCurrency)):
      toCurrency[i] = toCurrency[i].upper()


    fromCurrency = fromCurrency.upper()

    # Call swapcurrency and parse result
    try:
      res = swapCurrency(value, fromCurrency, toCurrency, strategy)  

      # All went well
      return {
        "ok": True,
        "res": res
      }
    except Exception as e:
      print(e)
      # Something went wrong
      # e.args is the message
      return {
        "ok": False,
        "msg": e.args
      }
    
  

Controller()