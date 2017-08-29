path = location.path.split('/');
username = path[2];

d3.csv(location.origin + "/profile/" + username + "username/categories/csv", function(error, data) {
  if (error) throw error;
  
  var size = data.length;
  var pds = 0;
  var maxpds = 0;

for (var i = 0; i < size; i++) {
  pds = ((data[i]["id"]).match(/\./g) || []).length;
  if (pds > maxpds) {
    maxpds = pds;
  }
}
  
  var svg = d3.select("svg");
  var width = window.innerWidth - 100;
  var height = 2000;
  
  
// width based on depth of tree  
  if (maxpds < 5) {
    width = 700;
  }
  
// height based on number of nodes
  height = 20 * size;
  
  svg.attr("width", width + 150);
  svg.attr("height", height);
  
    var g = svg.append("g").attr("transform", "translate(100,0)");
  

var tree = d3.cluster()
    .size([height, width - 160]);

var stratify = d3.stratify()
    .parentId(function(d) { return d.id.substring(0, d.id.lastIndexOf(".")); });

  var root = stratify(data)
      .sort(function(a, b) { return (a.height - b.height) || a.id.localeCompare(b.id); });
  


  tree(root);

  var link = g.selectAll(".link")
      .data(root.descendants().slice(1))
    .enter().append("path")
      .attr("class", "link")
      .attr("d", function(d) {
        return "M" + d.y + "," + d.x
            + "C" + (d.parent.y + 100) + "," + d.x
            + " " + (d.parent.y + 100) + "," + d.parent.x
            + " " + d.parent.y + "," + d.parent.x;
      });

  var node = g.selectAll(".node")
      .data(root.descendants())
    .enter().append("g")
      .attr("class", function(d) { return "node" + (d.children ? " node--internal" : " node--leaf"); })
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })

  node.append("circle")
      .attr("r", 2.5);

  node.append("text")
      .attr("dy", 3)
      .attr("x", function(d) { return d.children ? -8 : 8; })
      .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
      .text(function(d) { return d.id.substring(d.id.lastIndexOf(".") + 1); });
});


