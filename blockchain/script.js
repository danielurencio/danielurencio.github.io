Reveal.initialize({
  width:'100%',
  height:'100%'
});

var alphabet = '0123456789abcdef';
var colors = palette.listSchemes('rainbow')[0](16,.75,1)

//palette(['sequential'],alphabet.length,1)

Reveal.addEventListener('sha256',function() {
    shaBlock('hash','SHA256')
});

Reveal.addEventListener('merkleTree',function() {
  ABfunc();
  var arr = [
	  { pos:'1', tx:'A -> 11 -> B' },
	  { pos:'2', tx:'C -> 4 -> D' },
	  { pos:'3', tx:'E -> 80 -> F' },
	  { pos:'4', tx:'G -> 25 -> H' }
  ];
  for(var i in arr) {
      shaBlock('a_'+arr[i].pos,'&#11014;')
      shaBlock('b_'+arr[i].pos,i % 2 == 0 ? '&#11016;' : '&#11017;')
      
      var selInput_a = $('#a_'+arr[i].pos + ' input');
	  selInput_a.val(arr[i].tx).trigger('input');

      var selInput_b = $('#b_'+arr[i].pos + ' input');
	  selInput_b.val(arr[i].tx).trigger('input');
  }

  d3.select('#a_1 input').on('input',function() {
    var val = $('#a_1 input').val();
    $('#b_1 input').val('');
    $('#b_1 input').val(val).trigger('input')

  })

  d3.select('#a_2 input').on('input',function() {
    var val = $('#a_2 input').val();
    $('#b_2 input').val('');
    $('#b_2 input').val(val).trigger('input')

  })

  d3.select('#a_3 input').on('input',function() {
    var val = $('#a_3 input').val();
    $('#b_3 input').val('');
    $('#b_3 input').val(val).trigger('input')

  })

  d3.select('#a_4 input').on('input',function() {
    var val = $('#a_4 input').val();
    $('#b_4 input').val('');
    $('#b_4 input').val(val).trigger('input')

  })

  
  $('#shaBlock>div>div').css('font-size','15px')
  $('input').css('height','25px')
  	    .css('font-size','20px')

  d3.selectAll('.a1 #shaBlock').remove()
  d3.selectAll('.a2 input').style('display','none')
});

Reveal.addEventListener('A',ABfunc)
Reveal.addEventListener('B',ABfunc)

function ABfunc() {
  $('.sha').remove();
}


function shaBlock(id,text) {


	var str = '<div style="font-weight:800;z-index:2;position:relative;width:100%;" class="sha">'+
		text +
	    '<div style="width:50%;margin-left:25%">'+
		'<input style="width:100%; height:50px;text-align:center;font-size:40px;"></input>'+
	        '<div id="shaBlock" style="width:100%;display:table;height:100px;background:transparent;">'+
	        '</div>'+
	    '</div>'+
	   '</div>';

	var str_ = '<div>' +
		    '<div id="shaString"></div>'
		  '</div>';

	$('#'+ id).prepend(str)

	var arr = []

	for(var i=0; i<8; i++) {
	  arr.push([])
	  for(var j=0; j<8; j++) {
	    arr[i].push('e' + String(i) + '_' + String(j));
	  }
	}

	arr = arr.map(function(d) {
	  var sub_el = d.map(function(e) { return '<div style="border:1px solid white;display:table-cell;height:auto" id="'+e+'">&nbsp;</div>' }).reduce(function(a,b) { return a + b; });
	  return '<div style="display:table-row;">'+sub_el+'</div>'
	}).reduce(function(a,b){ return a + b; })
	

	$('#'+id+' #shaBlock').html(arr)


	$('#'+id+' input').on('input',function() {
		var val = $('#'+ id +' input').val();
		var sha = CryptoJS.SHA256(val).toString();
		var shaArr = []
		var i = 0;

		while(i<8) {
		  var substr = sha.substring(8*i,8*(i+1))
		  var temp_arr = []
		  for(var j=0; j<substr.length; j++) {
		      temp_arr.push(substr[j])
		      var selection = '#'+id+' #e'+ i +'_' + j;
		      $(selection).html(substr[j]);
		      $(selection).css('font-weight','800')
			  	  .css('color','rgba(0,0,0,0.85)')
		      var color = '#' + colors[alphabet.indexOf(substr[j])]
		      d3.select(selection).transition()
			  	  .duration(500)
				  .style('background-color',color)
		  }
		  shaArr.push(temp_arr)
		  i++
		}

		console.log(sha);
	});
}
