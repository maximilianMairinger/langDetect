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
    Calculate what the language a given text has

    :value: Text to be language detected
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
    Query the server what the language a given text has

    :value: Text to be language detected
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
