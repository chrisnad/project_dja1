from flask import Flask, Response, jsonify
from flask_cors import CORS, cross_origin
import fb_zhening

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/script', methods=['GET'])
@cross_origin()
def runScript():
    print "debut"
    fb_zhening.function(nodes, links)
    print 'Fin'
    resp = [{'id':1,'title':'toto'}, {'id':2,'title':'titi'}]
    print 'toto'
    return jsonify({'resp':resp})

if __name__ == "__main__":
  app.run(host='0.0.0.0')