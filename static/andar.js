function setupBookButton() {
   $(".book-button").click(function() { //highlight the button
        console.log(this);
      $(this).addClass("btn-warning");
      
    $.ajax("/add_booked", {
        method: "POST",
        datatype:"json",
        data: {'experience_id': $(this).attr("id")}
        }).done(function() {
                console.log("go go go!");          // confirm in the console
                // graph is likely to change, refresh it
        });
    });
}

function setupWanderButton() {
    $("button.wander-button").click(function() { //highlight the button
      console.log(this);
      $(this).addClass("btn-primary");

      // Send the new property to the database
      $.ajax("/add_wanderlist", {
          method: "POST",
          datatype:"json",
          data: {'experience_id': $(this).attr("id")}
          }).done(function() {
                  console.log("Victory!");          // confirm in the console
          });
    });
}


function setupDonutGraph() {
  var width = 1140,
      height = 450,
      radius = Math.min(width, height) / 2;

  var color = d3.scale.category20();

  var arc = d3.svg.arc()
      .outerRadius(radius - 10)
      .innerRadius(radius - 130);

  var pie = d3.layout.pie()
      .sort(null)
      .value(function(d) { return d.cat_count; });

  var svg = d3.select("#donut").append("svg")
      .attr("width", width)
      .attr("height", height)
    .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  d3.json("/visualize?data=True", function(error, data) {
    if (error){
      alert(error);
    }
    data.data.forEach(function(d) {
      d.cat_count = +d.cat_count;
    });

    var g = svg.selectAll(".arc")
        .data(pie(data.data))
      .enter().append("g")
        .attr("class", "arc");

    g.append("path")
        .attr("d", arc)
        .style("fill", function(d) {
          console.log(d);
          return color(d.data.category); });

    g.append("text")
        .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
        .attr("dy", ".35em")
        .style("text-anchor", "middle")
        .text(function(d) { return d.data.category; });

  });

}

function prependDollarSigns() {
  $('.price').toArray().forEach(function (el) {
    var $el = $(el);
     
    var price = $el.text();
    if (!price.startsWith('$')) {
       $el.text('$' + price);
    }
  });
}

function setupTabs() {
  $('.section.listed').hide();
  $('.section.wanderlist').hide();

  $('.wanderlist .tab').click(function() {
    console.log('clicked wanderlist!');
    $('.section.booked').hide();
    $('.section.wanderlist').show();
    $('.section.listed').hide();

    $('.nav-tabs li').removeClass('active');
    $('li.wanderlist').addClass('active');
  });

  $('.booked .tab').click(function() {
    $('.section.booked').show();
    $('.section.wanderlist').hide();
    $('.section.listed').hide();

    $('.nav-tabs li').removeClass('active');
    $('li.booked').addClass('active');
  });

  $('.listed .tab').click(function() {
    $('.section.booked').hide();
    $('.section.wanderlist').hide();
    $('.section.listed').show();

    $('.nav-tabs li').removeClass('active');
    $('li.listed').addClass('active');
  });
}


// When any user clicks on a button
// Add the record to connect user and property/experience in the UserProperty/Booked table
$(document).ready(function() {
   setupBookButton();
   setupWanderButton();
   setupDonutGraph();
   prependDollarSigns();
   setupTabs();
});
