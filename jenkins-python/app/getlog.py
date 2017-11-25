#!/usr/bin/env python
from flask import Flask
from elasticsearch import Elasticsearch
from flask import jsonify
from flask import render_template
from flask import request
import json

app = Flask(__name__)



@app.route('/')
def get_name_and_id():
    return render_template('form.html',string='')


@app.route('/', methods=['POST'])
def search_byid():

    jobname=request.form['jobname']
    jobid=request.form['jobid']
    jobdate=request.form['jobdate']

    es = Elasticsearch([{'host': 'jenkins-elasticsearch', 'port': 9200}])
    if jobname:
        if not jobid and not jobdate:
           return "PLEASE, ENTER JOB ID OR JOB DATE AND RETRY"
        if jobid and not jobdate:
            result=es.search(index='logstash',body={
   					 "query": {
					  	"bool": {
							"must": [
								{ "match_phrase_prefix": { "data.buildNum":   jobid }},
								{ "match_phrase_prefix": { "data.projectName":   jobname }}
								],

							}
						}
					   })
        elif not jobid and jobdate:
           result=es.search(index='logstash',body={
                                        "query": {
                                                "bool": {
                                                        "must": [
                                                                { "match_phrase_prefix": { "@buildTimestamp":   jobdate }},
                                                                { "match_phrase_prefix": { "data.projectName":   jobname }}
                                                                ],
                                                        }
                                                }
                                           })
        else:
           result=es.search(index='logstash',body={
                                         "query": {
                                                "bool": {
                                                        "must": [
								{ "match_phrase_prefix": { "@buildTimestamp":   jobdate }},
                                                                { "match_phrase_prefix": { "data.buildNum":   jobid }},
                                                                { "match_phrase_prefix": { "data.projectName":   jobname }}
                                                                ],

                                                        }
                                                }
                                           })
    else:
     return "PLEASE, ENTER PROJECT NAME AND JOB ID AND/OR JOB DATE AND RETRY"


    result_filtred=result['hits']['hits']
    response = json.dumps(result_filtred, sort_keys = True, indent = 4, separators = (',', ': '))
    return render_template('form.html',string=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
