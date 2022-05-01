from flask import Flask
from flask.templating import render_template

app=Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

import json

from flask import Flask, request, jsonify,render_template

from flask_mongoengine import MongoEngine

import requests
 

app = Flask(__name__)
app.config['MONGODB_SETTINGS']={
    'db':'IOT',
    'host':'localhost',
    'port':27017
}




db = MongoEngine()

db.init_app(app)
 
class device(db.Document):

    device_name = db.StringField()

    price = db.StringField()

    quantity=db.IntField()

    def to_json(self):

        return {"device_name": self.device_name,

                "price": self.price,

                "quantity":self.quantity}
 

@app.route('/', methods=['GET'])

def query_records():

    device_name = request.args.get('device_name')
    c = device.objects(device_name=device_name)
    if not c:

        return jsonify({'error': 'data not found'})
    else:

        return jsonify(c.to_json())
 

@app.route('/', methods=['POST'])
def create_record():
   

    record = json.loads(request.data)
    c = device(device_name=record['device_name'],

                price=record['price'],

                quantity=record['quantity'])

    c.save()

    return jsonify(c.to_json())
 

@app.route('/', methods=['PUT'])
def update_record():

    record = json.loads(request.data)
    c = device.objects(device_name=record['device_name']).first()
    if not c:

        return jsonify({'error': 'data not found'})
    else:

        c.update(price=record['price'])

        c.update(quantity=record['quantity'])
    c = device.objects(device_name=record['device_name']).first()

    return jsonify(c.to_json())
 

@app.route('/', methods=['DELETE'])
def delete_record():

    record = json.loads(request.data)
    c = device.objects(device_name=record['device_name']).first()
    if not c:

        return jsonify({'error': 'data not found'})
    else:
        c.delete()

    return jsonify(c.to_json())
 

@app.route('/add',methods=['GET','POST'])
def add():

    if request.method=="GET":

        return render_template("add.html")
    else:

        x={

        "device_name":request.form['device_name'],

        "price":request.form['price'],

        "quantity":int(request.form['quantity'])

        }

        x=json.dumps(x)

        response = requests.post(url="http://127.0.0.1:5000/",data=x)

        return response.text
 

@app.route('/find',methods=['GET','POST'])
def find():

    if request.method=="GET":

        return render_template("find.html")
    else:

        device_name=request.form['device_name']

        response = requests.get(url="http://127.0.0.1:5000/",params={"device_name":device_name})

        return response.json()
 

@app.route('/delete',methods=['GET','POST'])
def delete():

    if request.method=="GET":

        return render_template("del.html")
    else:

        x={

        "device_name":request.form['device_name'],
        

        }

        x=json.dumps(x)

        response = requests.delete(url="http://127.0.0.1:5000/",data=x)

        return response.text
 

@app.route('/update',methods=['GET','POST'])
def update():

    if request.method=="GET":

        return render_template("update.html")
    else:

        x={

        "device_name":request.form['device_name'],

        "price":request.form['price'],

        "quantity":int(request.form['quantity'])

        }

        x=json.dumps(x)

        response = requests.put(url="http://127.0.0.1:5000/",data=x)

        return response.text
 
if __name__ == "__main__":

    app.run(debug=True)


if __name__=='__main__':
    app.run(debug=True)