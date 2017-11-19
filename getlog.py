from flask import Flask
from elasticsearch import Elasticsearch
from flask import jsonify
#import json

app = Flask(__name__)


@app.route('/')
def welcome():
	str='You can search job log by id or datetime<br/><br/>If you want to search by id just type http://host:5000/jobid/(type here jobid)<br/><br/>Otherwise, type http://host:5000/jobdate/(type here jobid build time), date format YYYY-MM-DDTHH:MI<br/><br/>Thank you!'
	return str

@app.route('/jobid/<int:id>')
def search_byid(id):
        es = Elasticsearch([{'host': '192.168.0.248', 'port': 9200}])
	a=es.search(index='logstash',body={
					"query": {
						"bool": {
							"must": [
								{ "match_phrase_prefix": { "data.buildNum":   id }},
								],
							}
						}
					   })
#        b=json.dumps(a,sort_keys=True, indent=5)
        return jsonify(a)

@app.route('/jobdate/<datetime>')
def search_bydatetime(datetime):
        es = Elasticsearch([{'host': '192.168.0.248', 'port': 9200}])
        a=es.search(index='logstash',body={
                                        "query": {
                                                "bool": {
                                                        "must": [
                                                                { "match_phrase_prefix": { "@buildTimestamp":   datetime }},
                                                                ],
                                                        }
                                                }
                                           })
        return jsonify(a)




if __name__ == '__main__':
    app.run(host='0.0.0.0')
