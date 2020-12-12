console.log("DoIT :: loading organizationapp.js")

$(document).ready( function () {
  $.extend( $.fn.dataTable.defaults, {
    "responsive": true,
    "autoWidth": true,
    "searching": true,
    "paging":    false,
    "stateSave": false
  });

  $('#all-companies-table').DataTable({
    "processing": false,
    "deferRender": true,
    "serverSide": true,
    "lengthChange": false,
    "paging": true,
    "scroller": {
      loadingIndicator: true
    },
    "scrollY": '50vh',
    "ordering": false,
    "order": [[0, "asc"]],
    "ajax": {
      url: "/organizations/all_companies_dt",
    },
    "columnDefs": [
      // {
      //   "targets": 0,
      //   "render": function (data, type, row, meta) {
      //     return '<a href="/organization/edit/' + data + '">' + data + '</a>';
      //   }
      // },
      {
        "targets": 2,
        "data": null,
        "render": function (data, type, row, meta) {
          return '<a href="kblist/'+data[0]+'" uk-icon="file-text" uk-tooltip="title: Knowledge Base"></a><a target="_blank" href="/admin/organization/organization/'+data[0]+'/change/" uk-icon="settings" uk-tooltip="title: Company Settings"></a><a href="delete_organization/'+data[0]+'" uk-icon="trash" uk-tooltip="title: Delete '+data[1]+'" style="color: red;" onclick="return confirm(\'This is a non-recoverable operation! Are you sure?\')"></a>';
        }
      },


    ]
  });

  $('#all-companies-accordion').on('shown', function () {
    $($.fn.dataTable.tables(true)).DataTable().columns.adjust();
  });
});

console.log("DoIT :: unloading organizationapp.js")
