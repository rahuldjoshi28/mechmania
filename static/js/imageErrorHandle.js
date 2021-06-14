function handleError(){
	var tags = document.getElementsByTagName("img");
	for(var i=0; i<tags.length; ++i){
		document.tags[i].onerror = function(){
			document.tags[i].src = "static/images/quiz01.jpg";
		}
	}
}