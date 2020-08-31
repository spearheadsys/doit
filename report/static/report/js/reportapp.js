$(document).ready(function(){
  console.log("DoIT :: loading reportapp.js")

  var report = $('#reports').DataTable({
    dom: 'Bfrtip',
    buttons: [
        'copy', 'csv', 'excel'
    ]
  });
  report.buttons().container().appendTo( $('.col-sm-6:eq(0)', report.table().container() ) );

  $(function() {
    $('input[name="daterange"]').daterangepicker(
    {
      timePicker: true,
      timePicker24Hour: true,
      locale: {
          format: 'YYYY-MM-DD H:mm'
      },
      ranges: {
       'Today': [moment(), moment()],
       'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
       'Last 7 Days': [moment().subtract(6, 'days'), moment()],
       'Last 30 Days': [moment().subtract(29, 'days'), moment()],
       'This Month': [moment().startOf('month'), moment().endOf('month')],
       'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
      }
    }
    );
  });
  console.log("DoIT :: loaded reportapp.js")
});