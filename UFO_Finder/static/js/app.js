// from data.js
var tableData = data;

// Creating variable for table
var tbody = d3.select("tbody");

// Creating for loop from data.js
tableData.forEach(function (ufo_data) {

  // Appending result to table row    
  var row = tbody.append("tr");

  // Key-value pairs from ufoData
  Object.entries(ufo_data).forEach(function ([key, value]) {

    // Appending result to table as cell 
    var cell = tbody.append("td");
    cell.text(value);

  });
});

// Creating submit button and on-click function
var submit_button = d3.select("#filter-btn");
submit_button.on("click", function () {
  d3.event.preventDefault();

  // Removing and creating a new table with results
  var table = d3.select("table");
  d3.select("tbody").remove();
  var table = d3.select("table");
  table.append("tbody");

  // Creating variable for filter result
  var input_element = d3.select("#datetime");

  // Creating input value from element
  var input_value = input_element.property("value");

  // Filtering results based on date
  var new_results = tableData.filter(date => date.datetime === input_value);

  // Selecting New tbody
  var tbody = d3.select("tbody");

  // Creating new table with filtered results
  new_results.forEach((filtered_ufo_data) => {
    var row = tbody.append("tr");
    Object.entries(filtered_ufo_data).forEach(([key, value]) => {
      var new_cell = tbody.append("td");
      new_cell.text(value);
      
    });
  });
});