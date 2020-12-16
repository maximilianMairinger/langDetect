import requests
import json
import copy



def query(inp: str): 
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


