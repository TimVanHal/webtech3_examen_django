from django.shortcuts import render
from django.http import HttpResponse
import urllib2, json, redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def index(request):
    return render(request, 'chuck_norris/index.html')

def joke(request):
	firstname = request.POST['firstname']
	lastname = request.POST['lastname']
	response = urllib2.urlopen('http://api.icndb.com/jokes/random?firstName=' + firstname + '&lastName=' + lastname)
	parsed_json = json.loads(response.read())
	value = parsed_json['value']
	joke = value['joke']
	#geen eenvoudige manier om te controleren of joke al in jokes staat ==> remove en dan terug toevoegen
	#http://stackoverflow.com/questions/9312838/checking-if-a-value-exists-in-a-list-already-redis
	r.lrem(jokes, 1, joke)
	r.rpush(jokes, joke)
	return HttpResponse(response)