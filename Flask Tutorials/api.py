# put and delete -- HTTP Verbs
# working with api's-- JSON

#to do list (add, remove, update, delete task)

from flask import Flask, jsonify, request

app=Flask(__name__)

##Initial Data in my to do list
items = [
    {"id": 1, "name": "Item 1", "description": "This is item 1"},
    {"id": 2, "name": "Item 2", "description": "This is item 2"}
]


@app.route('/')
def landing_page():
    return "WELCOME TO TO_DO LIST"

##get: retrive all the items
@app.route('/get_items', methods=['GET'])
def get_items():
    return jsonify(items)

##get: based on some id, retrieve data
@app.route('/get_item_id/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item=next((item for item in items if item['id']==item_id), None)
    if item is None:
        return jsonify({'404: item not found'})
    return jsonify(item)

##post: creating a new iteam/task
@app.route('/create_item', methods=['POST'])
def create_item():
    if not request.json or not 'name' in request.json:
        return jsonify({"eror: item not found"})
    new_item={
        "id": items[-1]["id"] + 1 if items else 1, 
        "name":request.json['name'], 
        "description":request.json['description']
    }
    items.append(new_item)
    return jsonify(new_item)

##put: update an existing item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item=next((item for item in items if item['id']==item_id), None)
    if item is None:
        return jsonify({'404: item not found'})
    item['name']=request.json.get('name', item['name'])
    item["description"]=request.json.get('description', item['description'])
    return jsonify(item)

##DELETE: delete an item
@app.route('/del_item/<int:item_id>')
def del_item(item_id):
    global items
    items=[item for item in items if item['id']!=item_id]
    return jsonify({"result": "item deleted"})




if __name__=='__main__':
    app.run()




