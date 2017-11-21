Deployment Steps


1. Install OS (tested on CentOS 7.4 x86_64 kernel 3.10)

2. Install Docker (tested on Docker CE 17.09)

3. Install Docker-compose ( tested on docker-compose 1.17.1 )

4. Get source from github ( git clone https://github.com/AgasiAm/docker-jenkins )

5. Create user jenkins or just create directory /home/jenkins, and change dir to /home/jenkins

6. Get simple maven app from github ( git clone https://github.com/AgasiAm/simple-java-maven-app )

7. Change dir to docker-jenkins

8. Build containers using docker-compose ( docker-compose -p jenkins build )

9. Run containers using docker-compose ( docker-compose -p jenkins up -d jenkinsdata jenkinsmaster jenkinsnginx jenkinselasticsearch jenkinspython jenkinsrabbitmq and after docker-compose -p jenkins up -d jenkinssendmail (rabbitmq startup delay problem) )

10. Configure Jenkins http://yourserverip

11. Configure Jenkins Plugins
         
	Configure system
	
		 MQ Notifier Plugin
		 
		 MQ URI 		- amqp://jenkins-rabbitmq
		 user			- guest
		 password		- guest (you can change it for security reason)
		 Exchange Name		- jenkins
		 Routing Key		- buildjenkins
		
	Global Tool Configuration
	
		Logstash Plugin
		
		Indexer type		- ELASTICSEARCH
		Host name		- http://jenkins-elasticsearch
		Port			- 9200
		Key			- logstash/maven
		
		
12. Create new job -> Pipeline

13. Go to Pipeline tab

14. Configure job 
		
		Definition		- Pipeline script from SCM
		SCM			- GIT
		Repository URL		- Point to local Repository cloned on step 6 (/home/jenkins/imple-java-maven-app)
		
15. Run Pipeline job
