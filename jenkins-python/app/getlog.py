#!/usr/bin/env python
from flask import Flask
from elasticsearch import Elasticsearch
from flask import jsonify
#import json

app = Flask(__name__)


@app.route('/')
def welcome():
	str='You can search job log by id or datetime<br/><br/>If you want to search by id just type http://host:5000/yourprojectname/id/(type here jobid)<br/><br/>Otherwise, type http://host:5000/yourprojectname/date/jobdate/(type here jobid build time), date format YYYY-MM-DDTHH:MI<br/><br/>Thank you!'
	return str

@app.route('/<string:projectname>/id/<int:id>')
def search_byid(projectname,id):
        es = Elasticsearch([{'host': 'jenkins-elasticsearch', 'port': 9200}])
	a=es.search(index='logstash',body={
					"query": {
						"bool": {
							"must": [
								{ "match_phrase_prefix": { "data.buildNum":   id }},
								{ "match_phrase_prefix": { "data.projectName":   projectname }}
								],
							}
						}
					   })
#        b=json.dumps(a,sort_keys=True, indent=5)
        return jsonify(a)

@app.route('/<string:projectname>/date/<datetime>')
def search_bydatetime(projectname,datetime):
        es = Elasticsearch([{'host': 'jenkins-elasticsearch', 'port': 9200}])
        a=es.search(index='logstash',body={
                                        "query": {
                                                "bool": {
                                                        "must": [
                                                                { "match_phrase_prefix": { "@buildTimestamp":   datetime }},
								{ "match_phrase_prefix": { "data.projectName":   projectname }}
                                                                ],
                                                        }
                                                }
                                           })
        return jsonify(a)




if __name__ == '__main__':
    app.run(host='0.0.0.0')
