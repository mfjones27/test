from utils.api import search
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fields = ['city', 'bedrooms', 'bathrooms', 'home_type', 'listing_type', 'max_price']
        form_data = {field: request.form.get(field) for field in fields}
        search(form_data)
        #return redirect(url_for('results', form_data=form_data))

    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html', results=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)