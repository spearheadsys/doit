
$(document).ready(function(){
  console.log("DoIT :: loading doit.js ... ")

  // add additional columns
  $('#add_column').click(function(e) {
      let column = $('#initial-column').clone();
      $( "#column_form" ).after( column );
  });

});