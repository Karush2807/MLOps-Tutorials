from flask import Flask

'''
isne ek instance bnaya flask class ka, jo hai: wsgi application

'''
app=Flask(__name__)

@app.route('/')
def welcome():
    return 'welcome to my palace aka kamra!!'



if __name__=='__main__':
    app.run(debug=True)
