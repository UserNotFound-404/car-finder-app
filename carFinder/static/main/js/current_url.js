window.addEventListener('load', function() {
	var currentUrl = window.location.href;
	var title_name = ""
	var links = document.querySelectorAll('header a');
	for (var i = 0; i < links.length; i++) {
	var link = links[i];
	if (link.href === currentUrl) {
		link.classList.add('active');
		title_name = link.innerText;
	}
	}
	var title = document.querySelector('title');
	title.innerText = title_name
});