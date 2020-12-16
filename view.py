from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
import controller




def parseResultToHTML(res):
  html = ""
  for attr, value in res.items():
    html += (attr + ": " + "<b>" + str(value) + "</b><br>")

  return html


class Window(QtWidgets.QWidget):
  """
  The main window of the application
  
  :controller: The controller
  """
  def __init__(self, controller):
    """
    Constructs the main window of this application. Attach all needed event liusteners
    """
    super().__init__()
    self.controller = controller
    uic.loadUi("view.ui", self)




    def reset():
      """
      Reset all inputs and the HTML field
      """
      self.clearHTML()
      self.clearInputs()

    self.resetButton.clicked.connect(reset)

    def askForLanguageDetect():
      """
      Ask for calculation
      """

      value = self.inputField.toPlainText()
      self.controller.askForLanguageDetect(value)
      

    self.goButton.clicked.connect(askForLanguageDetect)



  def clearHTML(self):
    """
    Clear HTML field
    """
    self.browser.setHtml("")


  def clearInputs(self):
    """
    Clear all inputs
    """
    value = self.inputField.setPlainText("")

  def showResult(self, res):
    """
    Show the result as html in the middle field
    """
    del res["short"]
    self.browser.setHtml(parseResultToHTML(res))

  def showError(self, message):
    """
    Show the result as html in the middle field
    """
    self.browser.setHtml("Error: " + str(message))



