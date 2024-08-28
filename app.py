from flask import Flask , blueprints , render_template ,redirect ,url_for , request , jsonify , json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

@app.route('/')
def index():
    return 'start app ..'

data = [{'id': 1, 'username': 'jj okocha'}, {'id': 2, 'username': 'david ginola'}]
@app.route('/api/getuser', methods=['GET','POST','DELETE' , 'PUT'])
def api_getuser():
   
    if request.method == 'GET':
        user_id = request.args.get('id', default='')
        if user_id:
            user_id = int(user_id)  # Convert to integer for comparison
            # Search for the user by ID
            user = next((item for item in data if item['id'] == user_id), None)
            if user:
                return jsonify(user), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        else:
            # Return all users if no ID is specified
            return jsonify(data), 200

    # Placeholder responses for other methods (POST, DELETE, PUT)
    elif request.method == 'POST':
        # Implement POST logic here
        req = request.get_json()
       # print(req)
        data.append({'id': len(data)+1, 'username': req['username']})
        return jsonify({'message': 'insert success','data':data}), 201
    elif request.method == 'DELETE':
        id = request.args.get('id',type=int)
        # Implement DELETE logic here
        if id or id == 0:
            del data[id]
            return jsonify({'message':f'delete id {id} sucess'}),201
        return jsonify({'message': 'DELETE method not implemented'}), 501
    elif request.method == 'PUT':
        id  = request.args.get('id',default=None,type=int)
        req = request.get_json()
        #print(id)
        if id or id == 0:
            data[id]['username'] = req['username']
        # Implement PUT logic here
           # print(data)
            return jsonify({'message': 'update success','data':data}), 200
        return jsonify({'message': 'fail update'}), 404



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)

