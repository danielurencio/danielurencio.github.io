var arr = [1,2,3,4,5];

arr.forEach(function(d) {
    $('h' + d).css('font-family','Lato')
	      .css('font-weight',800);
});

$('p,li').css('font-family','Lato')
      	.css('font-size','20px')
      	.css('font-weight','300')
	.css('text-align','justify');
