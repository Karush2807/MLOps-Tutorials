from flask import Flask, render_template

'''
isne ek instance bnaya flask class ka, jo hai: wsgi application

'''
app=Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')



if __name__=='__main__':
    app.run(debug=True)
