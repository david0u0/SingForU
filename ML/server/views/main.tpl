<html>
<head>
<title>KP processor</title>
</head>
<script type="text/javascript" src='/js/audio.js'></script>
<script type="text/javascript">
	function onload() {
		init({{! '['+img_urls+']'}});
	}
</script>
<body onload='onload()'>

<p id='prompt'></p>
<audio id="audio"></audio>
<button onclick='replay()'>REPLAY</button>
<br/><br/><br/>
<input type='text' id='word'/>
<br/><br/><br/>
<button onclick='go()'>ENTER</button>
<br/><br/><br/>
<button onclick='discard()'>DISCARD</button>

</body>
</html>
