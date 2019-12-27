from flask import Flask, request, render_template, jsonify, make_response
import json
from model.model import init_db,Bookmodel
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__,
                static_folder="../frontend/dist/static",
                template_folder="../frontend/dist")

app.config.from_object('config.BaseConfig')

cors = CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

#app.pyでflaskアプリを構築してinit_db関数経由でmodel.pyに渡して初期化
init_db(app)
api = Api(app)
book = Bookmodel()

class Bookapp(Resource):
    def get(self):
        result = book.all_list()
        r = make_response(result)
        return r

    def put(self):
        book.update()
        r = make_response(jsonify({"message": "Update Succeeded"}))
        return r

    def delete(self):
        book.delete()
        r = make_response(jsonify({"message": "Delete Succeeded"}))
        return r

    def post(self):
        id = book.add()
        r = make_response(id)
        return r

api.add_resource(Bookapp, '/api/bookapp')

if __name__ == "__main__":
    app.run()