// When any user clicks on a button
// Add the record to connect user and property/experience in the UserProperty/Booked table
$(document).ready(function() {
    $(".book-button").click(function() { //highlight the button
        console.log(this);
      $(this).addClass("btn-warning");
    alert($(this).attr("id"));
    $.ajax("/add_booked", {
        method: "POST",
        datatype:"json",
        data: {'experience_id': $(this).attr("id")}
        }).done(function() {
                console.log("go go go!");          // confirm in the console
                // graph is likely to change, refresh it
        });
    });
});

$(document).ready(function() {
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
});

// $(document).ready(function() {
//         /*-------
//         event delegation 
//         *  $("#exp-details") is the parent div
//         *  '.nav-toggle' is the element that you are targeting. So if you were to click any other element
//             in $("#exp-details") that element would not run the preceeding function.
//         *In the function, what we are doing is called DOM traversal
            

//         -----------------*/

//         $('#exp-details').on('click', '.nav-toggle', function (evt){
//             $(this).parent().next().css("display", "block");
//         });
//           // $('.nav-toggle').click(function(){
//           //   //get collapse content selector
//           //   var collapse_content_selector = $(this).attr('href');

//           //   //make the collapse content to be shown or hide
//           //   var toggle_switch = $(this);
//           //   $(collapse_content_selector).toggle(function(){
//           //     if($(this).css('display')=='none'){
//           //                       //change the button label to be 'Show'
//           //       toggle_switch.html('Show');
//           //     }else{
//           //                       //change the button label to be 'Hide'
//           //       toggle_switch.html('Hide');
//           //     }
//           //   });
//           // });
                
//         });