var svgWidth = 960;
var svgHeight = 610;
var margin = {
    top: 30,
    right: 30,
    bottom: 80,
    left: 80
};
var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

var svg = d3.select("#scatter")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight)

var chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);


function xScale(health_data, chosenXAxis) {
    var xLinearScale = d3.scaleLinear()
        .domain([d3.min(health_data, d=> d[chosenXAxis])-1, d3.max(health_data, d=> d[chosenXAxis])+1])
        .range([0, chartWidth]);
    return xLinearScale;
}

function yScale(health_data, chosenYAxis) {
    // Linear scale for yScale
    var yLinearScale = d3.scaleLinear()
      .domain(d3.extent(health_data, d => d[chosenYAxis]))
      .range([chartHeight, 0]);
    return yLinearScale;
}

function renderAxes(newXScale, xAxis) {
    var bottomAxis = d3.axisBottom(newXScale);
    xAxis.transition()
        .duration(1000)
        .call(bottomAxis);
    return xAxis;
}

function renderCircles(circlesGroup, newXScale, chosenXaxis) {
    circlesGroup.transition()
        .duration(1000)
        .attr("cx", d => newXScale(d[chosenXAxis]));
    return circlesGroup;
}

d3.csv("assets/data/data.csv").then(function(health_data) {
    console.log(health_data);
  
    health_data.forEach(function(data) {
      data.healthcare = +data.healthcare;
      data.poverty = +data.poverty;
      data.age = +data.age;
      data.income = +data.income;
      data.obesity = +data.obesity;
      data.smokes = +data.smokes;
    });
  
    var xScale = d3.scaleLinear()
      .domain([8, d3.max(health_data, d => d.poverty)])
      .range([0, width]);
    var yScale = d3.scaleLinear()
      .domain([0, d3.max(health_data, d => d.healthcare)])
      .range([height, 0]);
  
    var bottomAxis = d3.axisBottom(xScale);
    var leftAxis = d3.axisLeft(yScale);
  
    chartGroup.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(bottomAxis);
    chartGroup.append("g").call(leftAxis);
  
    var circlesGroup = chartGroup.selectAll("circle")
      .data(health_data)
      .enter()
      .append("circle")
      .attr("cx", d => xScale(d.poverty))
      .attr("cy", d => yScale(d.healthcare))
      .attr("r", "14")
      .classed("stateCircle", true);
  
    var statesLabel = chartGroup.selectAll("texts")
      .data(health_data)
      .enter()
      .append("text")
      .attr("x", data => xScale(data.poverty))
      .attr("y", data => yScale(data.healthcare)+3)
      .classed("stateText", true)
      .text(d => d.abbr);
  
    chartGroup.append("text")
      .attr("transform", `translate(${width/2}, ${height + 50})`)
      .classed("aText", true)
      .text("In Poverty (%)");
  
    chartGroup.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 30)
      .attr("x", 0 - (height / 2))
      .classed("aText", true)
      .text("Lacks Healthcare (%)");
});  