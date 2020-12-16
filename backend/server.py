from flask import Flask, request, jsonify
from langdetect import detect_langs, detect
from iso639 import languages

app = Flask(__name__)

@app.route('/')
def root():
  # liest Parameter ein
  inp = request.args.get("lg")
  if inp == None: 
    return "Please enter a name under /?lg=\"\""
  # Gibt response zurueck

  l = detect_langs(inp)[0]
  lang = l.lang
  prob = l.prob


  return jsonify({
    "short": lang,
    "language": languages.get(alpha2=lang).name,
    "reliable": prob > .8,
    "prob": prob,
  })

if __name__ == '__main__':
  app.run(debug=False)


