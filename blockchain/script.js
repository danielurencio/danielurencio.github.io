Reveal.initialize({
  width:'100%',
  height:'100%'
});

var alphabet = '0123456789abcdefghijklmnopqrstuvwxyz';
var colors = palette('tol-rainbow',36)

Reveal.addEventListener('hola',function() {

	var str = '<div style="z-index:2;position:relative;width:100%" class="sha">'+
	    '<div style="width:50%">'+
		'<input style="width:100%; height:50px;text-align:center;font-size:40px;"></input>'+
	        '<div id="shaBlock" style="width:100%;display:table;height:100px;background:red;">'+
	        '</div>'+
	    '</div>'+
	   '</div>';

	var str_ = '<div>' +
		    '<div id="shaString"></div>'
		  '</div>';

	$('#hash').prepend(str)

	var arr = []

	for(var i=0; i<8; i++) {
	  arr.push([])
	  for(var j=0; j<8; j++) {
	    arr[i].push('e' + String(i) + '_' + String(j));
	  }
	}

	arr = arr.map(function(d) {
	  var sub_el = d.map(function(e) { return '<div style="border:1px solid white;display:table-cell;height:50px" id="'+e+'">&nbsp;</div>' }).reduce(function(a,b) { return a + b; });
	  return '<div style="display:table-row;">'+sub_el+'</div>'
	}).reduce(function(a,b){ return a + b; })
	

	$('#shaBlock').html(arr)


	$('input').on('input',function() {
		var val = $('input').val();
		var sha = CryptoJS.SHA256(val).toString();
		var shaArr = []
		var i = 0;

		while(i<8) {
		  var substr = sha.substring(8*i,8*(i+1))
		  var temp_arr = []
		  for(var j=0; j<substr.length; j++) {
		      temp_arr.push(substr[j])
		      $('#e'+ i +'_' + j).html(substr[j]);
		  }
		  shaArr.push(temp_arr)
		  i++
		}

		console.log(sha);
	});

});

Reveal.addEventListener('A',ABfunc)
Reveal.addEventListener('B',ABfunc)

function ABfunc() {
  $('.sha').remove();
}
