#!/usr/bin/env python
from flask import Flask
from elasticsearch import Elasticsearch
from flask import jsonify
from flask import render_template
from flask import request
import json

app = Flask(__name__)


# First Page

@app.route('/')
def get_name_and_id():
    return render_template('form.html',string='')


@app.route('/', methods=['POST'])
def search():

# Get Vars From HTML Page

    jobname=request.form['jobname']
    jobid=request.form['jobid']
    jobdate=request.form['jobdate']
    action=request.form['submit']
    stage=request.form.get('stage',type=int)
    response_message=[]
    response_data=[]

    
# Connect to elasticsearch and query data

    es = Elasticsearch([{'host': 'jenkins-elasticsearch', 'port': 9200}])
    if jobname:
        if not jobid and not jobdate:
           return render_template('form.html',data="PLEASE, ENTER JOB ID OR JOB DATE AND RETRY")
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
     return render_template('form.html',data="PLEASE, ENTER PROJECT NAME AND JOB ID AND/OR JOB DATE AND RETRY")


# Next and Back Buttons

    if not stage:
        stage=0
 

    if action == 'get':
        stage=0
    elif action == 'next':
        stage=stage+1
    elif action == 'back' and stage > 0:
        stage=stage-1
    

# Data Output

    for result_filtred in result['hits']['hits']:
        response_message.append(result_filtred['_source']['message'])
        response_data.append(result_filtred['_source']['data'])

    if stage > len(response_data):
        stage=None

    try:
      return render_template('form.html',data=json.dumps(response_data[stage], sort_keys = True, indent = 4, separators = (',', ': ')),msg=json.dumps(response_message[stage], sort_keys = True, indent = 4, separators = (',', ': ')),jobname=jobname,jobid=jobid,jobdate=jobdate,stage=stage)
    except:
      return render_template('form.html',data="No data found",jobname=jobname,jobid=jobid,jobdate=jobdate)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
