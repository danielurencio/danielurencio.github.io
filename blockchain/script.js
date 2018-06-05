Reveal.initialize({});

Reveal.addEventListener('hola',function() {

	var str = '<div style="z-index:2;position:fixed;" class="sha">'+
	    '<div>'+
		'<input></input>'+
	        '<div id="shaString">'+
	        '</div>'+
	    '</div>'+
	   '</div>';

	$('body').prepend(str)

	$('input').on('input',function() {
		var val = $('input').val();
		var sha = CryptoJS.SHA256(val).toString();
		$('#shaString').html(sha)
	});
});

Reveal.addEventListener('A',ABfunc)
Reveal.addEventListener('B',ABfunc)

function ABfunc() {
  $('.sha').remove();
}
