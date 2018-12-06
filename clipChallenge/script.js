var arr = [1,2,3,4,5];

arr.forEach(function(d) {
    $('h' + d).css('font-family','Lato')
	      .css('font-weight',800);
});

$('#Clip-Challenge').css('font-size','45px');

$('.prompt').html('');
$('.prompt').css('display','none');

$('p,li').css('font-family','Lato')
      	.css('font-size','20px')
      	.css('font-weight','300')
	.css('text-align','justify')
	.css('line-height','1.4');

Array.prototype.slice.call(document.querySelectorAll('span'))
	.filter(function(d) {
		return $(d).text() == 'Loading BokehJS ...';
	})
	.forEach(function(d) {
		$(d).parent().css('display','none');
	});

$('.container').css('box-shadow','none');
