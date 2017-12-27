
function NN(config,svg1) {
  var layers = config.layers;

  var g_NN = svg1.append("g");
  var h = svg1.attr("height").split("px")[0];
  var w = svg1.attr("width").split("px")[0];

  for(var l in layers) {
    var arr = [];

    for(var i=0; i<layers[l]; i++) {
      arr.push(0);
    };

    var LAYER = g_NN.append("g")
	.attr("id","l_" + l)
	.attr("class","layer");

    LAYER.selectAll("circle").data(arr)
        .enter().append("circle")
        .attr({
          "cx": function(d,i) { return config.x_space*l; },
          "cy": function(d,i) { return config.y_space*i; },
          "r": config.radius,
	  "stroke": config.neuronCol,
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

  var noOfLayers = d3.selectAll(".layer")[0].length - 1;
  for(var l=0; l<noOfLayers; l++) {
    var cero = d3.selectAll("circle.l_" + l)
    var y_0_offset = d3.select("g#l_" + l)[0][0]
		.getAttribute("transform")
		.split(",")[1].split(")")[0];

    var y_1_offset = d3.select("g#l_" + (l+1))[0][0]
		.getAttribute("transform")
		.split(",")[1].split(")")[0];

    var nextNeurons = d3.selectAll("#l_"+(l+1)+">circle")[0].length;

    for(var j=0; j<nextNeurons;j++) {
      g_NN.append("g").selectAll("line").data(cero[0])
      .enter().append("line")
      .attr({
        "x1": function(d,i) {
	  var x = d3.select("circle.l_" + l).attr("cx");
	  return x 
        },
        "y1": function(d,i) {
	  var y = d3.select(".l_"+l+"#n_" + i).attr("cy");
          return Number(y) + +y_0_offset;
        },
        "x2": function(d,i) {
	  var x = d3.select("circle.l_"+(l+1)).attr("cx");
	  return x
        },
        "y2": function(d,i) {
	  var offset = d3.select("g#l_"+(l+1)).attr("transform")
	  return +d3.select("#n_" + j + ".l_"+(l+1)).attr("cy") + +y_1_offset;
        },
        "stroke":config.neuronCol,
        "stroke-dasharray":"5,5"
      });
    }
  }
  d3.selectAll("g.layer").remove()

  for(var l in layers) {
    var arr = [];

    for(var i=0; i<layers[l]; i++) {
      arr.push(0);
    };

    var LAYER = g_NN.append("g")
	.attr("id","l_" + l)
	.attr("class","layer");

    LAYER.selectAll("circle").data(arr)
        .enter().append("circle")
        .attr({
          "cx": function(d,i) { return config.x_space*l; },
          "cy": function(d,i) { return config.y_space*i; },
          "r": config.radius,
	  "stroke": config.neuronCol,
	  "fill": "white",
	  "stroke-width":"3px",
	  "id": function(d,i) { return "n_" + i; },
	  "class": function(d,i) { return "l_" + l; }
         });

    var g_h = LAYER.node().getBBox().height / 2;
    LAYER.attr("transform","translate(0," + String(h/2-g_h) + ")")
  };


};
