function buildPlot() {
  /* data route */
var url = "/api/pals-summary";
d3.json(url).then(function(response) {

  console.log(response);

  var pet_name = response.map(p => p.name);
  var pet_type = response.map(p => p.type);
  var pet_count = response.map(p => p.count);

  var trace = [{
    'x': pet_type,
    'y': pet_count,
    'type': 'bar'
  }];

  var layout = {
    title: "Pet Pals",
    xaxis: {
      title: "Pet Type"
    },
    yaxis: {
      title: "Number of Pals"
    }
  };

  Plotly.newPlot("plot", trace, layout);
});
}

function buildTable() {
/* data route */
var url = "/api/pals";
d3.json(url).then(function(response) {

  var pet_name = response.map(p => p.name);
  var pet_type = response.map(p => p.type);
  var pet_age = response.map(p => p.age);

  var table = d3.select("#pets-table");
  var tbody = table.select("tbody");
  console.log(tbody);
  var trow;
  for (var i = 0; i < pet_name.length; i++) {
    trow = tbody.append("tr");
    trow.append("td").text(pet_name[i]);
    trow.append("td").text(pet_type[i]);
    trow.append("td").text(pet_age[i]);
    }
});
}

buildPlot();

buildTable();