var audio_player; 
var audios = [];
var cur = -1;

function init(a) {
	audio_player = document.getElementById("audio");
	audio_player.type = "type/wav";
	audios = a;
	next();
}

function next() {
	cur++;
	audio_player.src = '/audios/' + audios[cur];
	replay();
	document.getElementById('prompt').innerHTML = cur + '/' + audios.length;
}

function replay() {
	audio_player.play();
}

function go() {
	var req = new XMLHttpRequest();
	var word = document.getElementById('word').value;
	if(word.length != 1) {
		alert('fuck u?');
		return;
	}
    var query = '?word=' + word + '&url=' + audios[cur];
    req.open("GET", "/rander"+query, true);
    req.send();
    document.getElementById('word').value = '';
    next();
}

function discard() {
	var req = new XMLHttpRequest();
    var query = '?url=' + audios[cur];
    req.open("GET", "/discard"+query, true);
    req.send();
    document.getElementById('word').value = '';
    next();
}