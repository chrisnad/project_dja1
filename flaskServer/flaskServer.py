from flask import Flask, Response
from flask_cors import CORS, cross_origin
import fb_zhening

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/script', methods=['GET'])
@cross_origin()
def config():
    print "debut"
    fb_zhening.function()
    print 'Fin'
    resp = Response('toto')
    print 'toto'
    return resp

@app.route('/test', methods=['GET'])
@cross_origin()
def a():
    print "HI"
    return "Hello, cross-origin-world!"

if __name__ == "__main__":
  app.run(host='0.0.0.0')