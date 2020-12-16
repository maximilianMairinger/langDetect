from flask import Flask, request, jsonify
from langdetect import detect_langs, detect
from iso639 import languages

app = Flask(__name__)

@app.route('/')
def root():
  """
  Query the server what the language a given text has
  lg can be given as get parameter. To detect the language its value has
  """
  # Reads parameter lg
  inp = request.args.get("lg")
  if inp == None: 
    return "Please enter a name under /?lg=\"\""

  # Calculate response
  l = detect_langs(inp)[0]
  lang = l.lang
  prob = l.prob


  # Format response
  return jsonify({
    "short": lang,
    "language": languages.get(alpha2=lang).name,
    "reliable": prob > .8,
    "prob": prob,
  })

if __name__ == '__main__':
  app.run(debug=False)


