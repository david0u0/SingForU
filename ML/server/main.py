# -*- coding: utf8 -*-
from bottle import route, run, template, static_file, request
from os import walk, path, mkdir
from subprocess import call

@route('<path:path>')
def static(path):
	return static_file(path, root='static')

@route('/index')
def index():
	urls = []
	for (dirpath, dirnames, filenames) in walk('static/audios'):
		urls.extend(filenames)
		urls = ["'"+s+"'" for s in urls]
		break
	return template('main', img_urls=','.join(urls))

@route('/rander')
def rander():
	word = request.query['word'].decode('utf8')
	url = request.query['url']
	if not path.exists('../data'):
		mkdir('../data')
	if not path.exists('../data/'+word):
		mkdir('../data/'+word)
	call(['mv', 'static/audios/'+url, ('../data/'+word).encode('big5')])

@route('/discard')
def discard():
	url = request.query['url']
	call(['rm', 'static/audios/'+url])


run(host='0.0.0.0', port=8888, debug=True)
