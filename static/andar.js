// When any user clicks on a button
// Add the record to connect user and property/experience in the UserProperty/Booked table
$(document).ready(function() {
    $("button.book-button").click(function() { //highlight the button
        console.log(this);
      $(this).toggleClass("blue");

    $.ajax("/add_wanderlist", {
        method: "POST",
        datatype:"json",
        data: {'experience_id': $(this).attr("id")}
        }).done(function() {
                console.log("go go go!");          // confirm in the console
        });
    });
});

$(document).ready(function() {
    $("button.wander-button").click(function() { //highlight the button
        console.log(this);
      $(this).toggleClass("blue");

// Send the new property to the database
    $.ajax("/add_booked", {
        method: "POST",
        datatype:"json",
        data: {'experience_id': $(this).attr("id")}
        }).done(function() {
                console.log("Victory!");          // confirm in the console
        });
    });
});

