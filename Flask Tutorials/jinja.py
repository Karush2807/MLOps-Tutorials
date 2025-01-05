#building url dynamically
#variable naming rule
## jinja 2 template engine

from flask import Flask, render_template, request

'''
isne ek instance bnaya flask class ka, jo hai: wsgi application

'''



'''

{{ }} expression to print output in html

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

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method=='POST':
        name=request.form['name']
        return f"hello {name}"
    return render_template('form.html')

# variable rule
@app.route('/success_res/<int:score>')
def success(score):
    res=""
    if score>=50:
        res="PASS"
    else:
        res="FAIL"

    exp={'score': score, 'result':res}

    return render_template('result.html', result=exp)




if __name__=='__main__':
    app.run(debug=True)
