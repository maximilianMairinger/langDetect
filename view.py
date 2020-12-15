from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
import controller




def parseResultToHTML(res):
  html = ""
  html += "<b>" + str(res["baseValue"]) + " " + res["baseCurrency"] + "</b> entsprechen"
  html += "<ul>"

  values = res["values"]
  rates = res["rates"]
  for currency in values:
    value = values[currency]
    rate = rates[currency]

    html += "<li><b>" + str(round(value, 2)) + " " + currency +  "</b> (Kurs: " + str(round(rate, 2)) + ")</li>"

  html += "</ul>"
  html += "Stand: " + res["date"]
  

  return html


class Window(QtWidgets.QWidget):
  """
  The main window of the application
  """
  def __init__(self, controller):
    """
    Constructs the main window of this application. Attach all needed event liusteners
    """
    super().__init__()
    self.controller = controller
    uic.loadUi("view.ui", self)


    self.fromInput.setValidator(QRegExpValidator(QRegExp("^[A-Z,a-z]{1,3}$")))
    self.toInput.setValidator(QRegExpValidator(QRegExp("^([A-Z,a-z]{1,3})(,([A-Z,a-z]{1,3})){0,1000}$")))



    def reset():
      """
      Reset all inputs and the HTML field
      """
      self.clearHTML()
      self.clearInputs()

    self.resetButton.clicked.connect(reset)

    def askForCurrencyChange():
      """
      Ask for calculation
      """

      value = float(self.betragInput.text())
      fromCurrency = self.fromInput.text()
      toCurrency = self.toInput.text()
      live = self.liveCheckbox.isChecked()

      self.controller.askForCurrencyChange(value, fromCurrency, toCurrency, live)
      

    self.goButton.clicked.connect(askForCurrencyChange)

  def setStatus(self, status):
    self.statusLabel.setText(status)

  def clearHTML(self):
    """
    Clear HTML field
    """
    self.browser.setHtml("")


  def clearInputs(self):
    """
    Clear all inputs
    """
    self.betragInput.setValue(0)
    self.fromInput.setText("")
    self.toInput.setText("")
    self.liveCheckbox.setChecked(False)
    self.statusLabel.setText("Reset")

  def showResult(self, res):
    """
    Show the result as html in the middle field
    """
    self.browser.setHtml(parseResultToHTML(res))


