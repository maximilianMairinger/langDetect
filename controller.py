from PyQt5 import QtWidgets, uic
import sys
from view import *
from modell import *



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

  def askForLanguageDetect(self, value):
    """
    Ask for calculation
    """
    # clear output
    self.view.clearHTML()
    
    # Request
    ret = self.queryLanguage(value)

    # parse
    if ret["ok"]: 
      self.view.showResult(ret["res"])
    else: 
      self.view.showError(ret["msg"])

  def queryLanguage(self, value):
    """
    Calculate the value of a quantety of a currency in other currencies
    Currency should be given in 3 letter form (e.g: EUR, USD)

    :value: How much of this currency should be calculated
    :fromCurrency: What is the currency you want to calculate from. Currency should be given in 3 letter form (e.g: EUR, USD)
    :toCurrency: What is the currency you want to calculate to. This can be a comma seperated string or a list. Currency should be given in 3 letter form (e.g: EUR, USD)
    :live: If true, use live data from the web
    :return: {ok: True, res: {...}} when everything went well. And {ok: False, msg: string} when something went wrong
    """

    # Call query and parse result
    try:
      res = query(value)

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