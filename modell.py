import requests
import copy
from abc import ABC, abstractmethod


class GetRateStrategy(ABC):
    @abstractmethod
    def getRate(self, fromCurrency: str, toCurrency: list[str]):
      """
      Get rate from currency to currency from live api

      :fromCurrency: the currency the rate is ralative to
      :toCurrency: the currencies (as list) you are intrested in
      :return: Result in form {rates: {[key in string]: float}, base: string, date: string}
      :raise: When something went wrong a generic Exception gets raised, with the explaination as args
      """
      pass

class GetRateWithApi(GetRateStrategy):
  def getRate(self, fromCurrency: str, toCurrency: list[str]):
    """
    Get rate from currency to currency from live api

    :fromCurrency: the currency the rate is ralative to
    :toCurrency: the currencies (as list) you are intrested in
    :return: Result in form {rates: {[key in string]: float}, base: string, date: string}
    :raise: When something went wrong a generic Exception gets raised, with the explaination as args
    """
    print("online")
    # Fix is true if fromCurrency is inside toCurrency, which means it will be added later with a rate of 1
    fix = False
    if fromCurrency in toCurrency:
      fix = True
      toCurrency.remove(fromCurrency)
    # Url to request from server. Example: "https://api.exchangeratesapi.io/latest?base=EUR&symbols=USD"
    url = "https://api.exchangeratesapi.io/latest?base=" + fromCurrency + "&symbols=" + ",".join(toCurrency)
    res = requests.get(url).json()
    if "error" in res:
      # Raises an exception if an error occurred during the api request
      raise Exception(res["error"])
    else:
      if fix:
        toCurrency.append(fromCurrency)
        res["rates"][fromCurrency] = 1.0
      return res




class GetRateOffline(GetRateStrategy):
  def getRate(self, fromCurrency: str, toCurrency: list[str]):
    """
    Get rate from currency to currency from live api

    :fromCurrency: the currency the rate is ralative to
    :toCurrency: the currencies (as list) you are intrested in
    :return: Result in form {rates: {[key in string]: float}, base: string, date: string}
    :raise: When something went wrong a generic Exception gets raised, with the explaination as args
    """
    print("offline")
    try:
      # Get the offline Data and copy it
      res = copy.deepcopy(GetRateOffline.offline)
    
      res["base"] = fromCurrency
      rates = res["rates"]
      fromValue = rates[fromCurrency]
      # Calculate the rate from the offline data
      for key in toCurrency:
        rates[key] = rates[key] / fromValue

      return res
    except Exception as e:
      print(e)
      raise Exception("Unable to find currency")


# The offline data
GetRateOffline.offline = {"rates":{"CAD":1.4959,"HKD":11.2301,"LVL":0.7093,"PHP":66.106,"DKK":7.4405,"HUF":268.18,"CZK":26.258,"AUD":1.5668,"RON":4.1405,"SEK":10.2215,"IDR":13281.14,"INR":66.21,"BRL":2.5309,"RUB":42.6974,"LTL":3.4528,"JPY":132.41,"THB":47.839,"CHF":1.4743,"SGD":2.0133,"PLN":4.0838,"BGN":1.9558,"TRY":2.1084,"CNY":9.8863,"NOK":8.1825,"NZD":1.9573,"ZAR":10.8264,"USD":1.4481,"MXN":18.4995,"EEK":15.6466,"GBP":0.8972,"KRW":1627.4,"MYR":4.8424,"HRK":7.2753},"base":"EUR","date":"2010-01-12"}
if not GetRateOffline.offline["base"] in GetRateOffline.offline["rates"]:
  GetRateOffline.offline["rates"][GetRateOffline.offline["base"]] = 1.0






def swapCurrency(value, fromCurrency, toCurrency, getRateStrategy: GetRateStrategy):
  """
  Calculate the value of a quantety of a currency in other currencies
  Currency should be given in 3 letter form (e.g: EUR, USD)

  :value: How much of this currency should be calculated
  :fromCurrency: What is the currency you want to calculate from. Currency should be given in 3 letter form (e.g: EUR, USD)
  :toCurrency: What is the currency you want to calculate to. This can be a comma seperated string or a list. Currency should be given in 3 letter form (e.g: EUR, USD)
  :via: What calculator should be used to calculate the rate
  :return: Result in form {rates: {[key in string]: float}, values: {[key in string]: float}, base: string, date: string, baseValue: string} where values are the cumputed ammount in the new currencies
  :raise: When something went wrong a generic Exception gets raised, with the explaination as args
  """
  
  # Try to execute calculator
  res = getRateStrategy.getRate(fromCurrency, toCurrency)
  try:
    rates = res["rates"]
    values = {}
    # Calculate new value with given rate
    for key in toCurrency:
      values[key] = rates[key] * value

    # return formatted data
    return {
      "rates": res["rates"],
      "values": values,
      "date": res["date"],
      "baseCurrency": fromCurrency,
      "baseValue": value
    }
  except Exception as e:
    # When something unknown went wrong
    raise Exception("Unknown error")

  
