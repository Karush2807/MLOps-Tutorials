from flask import Flask, render_template, request

'''
isne ek instance bnaya flask class ka, jo hai: wsgi application

'''
app=Flask(__name__)


@app.route('/')
def welcome():
    return "hellooooooooooooooooo"

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method=='POST':
        name=request.form['name']
        return f"hello {name}"
    return render_template('form.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method=='POST':
        name=request.form['name']
        return f"hello {name}"
    return render_template('form.html')




if __name__=='__main__':
    app.run(debug=True)
