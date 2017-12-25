var svg1 = d3.select("div#i")
 .append("svg")//.append("g")
  .attr("width","550px")
  .attr("height","300px")//.append("g")

var layers = [3,2,1]


function NN(layers) {
  var g_NN = svg1.append("g");
  var h = svg1.attr("height").split("px")[0];
  var w = svg1.attr("width").split("px")[0];

  for(var l in layers) {
    var arr = [];

    for(var i=0; i<layers[l]; i++) {
      arr.push(0);
    };

    var LAYER = g_NN.append("g").attr("id","l_" + l);
    LAYER.selectAll("circle").data(arr)
        .enter().append("circle")
        .attr({
          "cx": function(d,i) { return 100*l; },
          "cy": function(d,i) { return 80*i; },
          "r": 15,
	  "stroke": "black",
	  "fill": "white",
	  "stroke-width":"2px",
	  "id": function(d,i) { return "n_" + i; },
	  "class": function(d,i) { return "l_" + l; }
         });

    var g_h = LAYER.node().getBBox().height / 2;
    LAYER.attr("transform","translate(0," + String(h/2-g_h) + ")")
  };

  var g_w = g_NN.node().getBBox().width / 2;
  g_NN.attr("transform","translate(" + String(w/2-g_w) + ",0)");

  var cero = d3.selectAll("circle.l_0")

  g_NN.selectAll("line").data(cero[0])
    .enter().append("line")
    .attr({
      "x1": function(d,i) {
	var x = d3.select("circle.l_0").attr("cx");
	return x 
      },
      "y1": function(d,i) {
	var offset = d3.select("g#l_0").attr("transform");
	//console.log("y1 offset: ",offset)
	var y = d3.select(".l_0#n_" + i).attr("cy");
        console.log(Number(y)+1)
        return Number(y)+55
      },
      "x2": function(d,i) {
	var x = d3.select("circle.l_1").attr("cx");
	return x
      },
      "y2": function(d,i) {
	var offset = d3.select("g#l_1").attr("transform")
	console.log("y2 offset: ",offset)
	return d3.select("#n_" + 0).attr("cy") + 95
      },
      "stroke":"black",
      "stroke-dasharray":"5,5"
    })
};

NN(layers);
