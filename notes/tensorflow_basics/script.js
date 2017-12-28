var svg1 = d3.select("div#i_0")
 .append("svg")
  .attr("width","550px")
  .attr("height","310px");

var layers = {
  layers: [3,2,1],
  x_space: 110,
  y_space: 90,
  radius: 25,
  neuronCol: "rgb(50,50,50)"
}

NN(layers,svg1);

var linesDel = d3.selectAll("#i_0 line")[0]

for(var i=0; i<linesDel.length; i++) {
  if(i==2 || i==3 || i ==78) {
    d3.select(linesDel[i]).attr("class","del");
  }
}

d3.selectAll(".del").remove();

var circles_0 = d3.selectAll("#i_0 circle")[0];
var offset_x = +d3.select("#i_0 svg>g").attr("transform")
		.split(",")[0].split("(")[1];

var labels_0 = ["A = 3","B = 2","C = 1","D = 5","E = 1","F = 5"];
var labels_1 = ["constant","constant","constant","summation","subtraction","multiplication"];

for(var i=0; i<circles_0.length; i++) {
  var cx = +d3.select(circles_0[i]).attr("cx");

  var cy = d3.select(circles_0[i]).attr("cy");

  var offset_y = d3.select(circles_0[i].parentNode)
		.attr("transform")
		.split(",")[1].split(")")[0];

  d3.select("#i_0 svg").append("text")
	.attr("x",+cx + +offset_x)
	.attr("y",+cy + +offset_y)
	.attr("alignment-baseline","central")
	.attr("text-anchor","middle")
	.attr("font-family","Roboto")
        .attr("font-weight","700")
	.attr("font-size","14px")
	.text(labels_0[i]);

  d3.select("#i_0 svg").append("text")
	.attr("x",+cx + +offset_x)
	.attr("y",+cy + +offset_y - layers.radius - 3)
	.attr("alignment-baseline","text-after-edge")
	.attr("text-anchor","middle")
	.attr("font-family","Roboto")
        .attr("font-weight","400")
	.attr("font-size","12px")
	.text(labels_1[i]);

}
