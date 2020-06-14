from flask import Flask, request, render_template
import joblib
import numpy as np
import re
from utils import stopwords

app = Flask(__name__)

def preprocess_news(val):
    val = ''.join(re.findall('[A-Za-z\s]', val))
    val = val.lower()
    val = [word for word in val.split() if word not in stopwords]
    val = ' '.join(val)
    return val

@app.route('/', methods = ['POST', 'GET'])
def home():
	if request.method == 'POST':
		clf = joblib.load('newsy_model.pkl')
		vec = joblib.load('newsy_vec.pkl')
		demapper = {1 : 'Business', 2 : 'Technology', 3 : 'Science', 4 : 'Sports',
				5 : 'Entertainment', 6 : 'Health'}
		msg = request.form['input']
		msg = preprocess_news(msg)
		msg = demapper[np.argmax(clf.predict_proba(vec.transform([msg]).toarray())) + 1]
		return render_template('predict.html', prediction_msg = msg)
	return render_template('main.html')

if __name__ == '__main__':
	clf = joblib.load('newsy_model.pkl')
	vec = joblib.load('newsy_vec.pkl')
	app.run(host='0.0.0.0')
