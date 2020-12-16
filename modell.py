import requests
import json
import copy



def query(inp: str): 
  """
  Query the server what the language a given text has

  :inp: Text to be language detected
  :return: in form of {"reliable": boolean, "language": string, "short": string, "prob": number}
  :raise: When the network request errors, or the server has an internal error. The error message will be sent
  """
  if inp == "":
    raise Exception("Input cannot be empty")
  url = "http://127.0.0.1:5000/?lg=" + json.dumps(inp)
  res = requests.get(url).json()
  if "error" in res:
    # Raises an exception if an error occurred during the api request
    raise Exception(res["error"])
  else:
    return res













# TEST modell

# print(query("Hallo mein Name ist Max."))
# print(query("Hello my name is Max."))


