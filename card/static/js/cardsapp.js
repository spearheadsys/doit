// // {% if page_name == "Cards" %}
// <!-- BEGIN NEW UIKIT -->
// <script type="text/javascript">
//     // generic: log start, added, removed, stop (useful for debugging)
//     // var util = UIkit.util;
//     // util.ready(function () {
//     //     util.on(document.body, 'start moved added removed stop', function (e, sortable, el) {
//     //         //console.log(e.type, sortable, el);
//     //     });
//     // });
//     // end generic
//
//   {% for column in columns %}
//   // add card to new column. then update order
//     UIkit.util.on('#{{column}}', 'added', function (e, el, type) {
//       {# console.log("card is " + e.detail[1].id);#}
//       var card = e.detail[1].id
//       var column = e.target.attributes[1].value;
//       {#console.log("card is " + card);#}
//       {#console.log("destination column " + column)#}
//
//       var sortResult = { elementsOrder: [] };
//       $('#{{column}} > li').each(function () {
//           var currentEl = $(this);
//           sortResult.elementsOrder.push(currentEl[0].id);
//       });
//       $.ajax({
//           type: "POST",
//           //async: true,
//           url: "/cards/updatecardorder/",
//           //traditional: true,
//           data: {
//             arr: JSON.stringify(sortResult)
//             }
//       });
//
//       //UIkit.notification(`"${item.detail[1].id}" was added.`, 'success');
//       $.ajax({
//       type: "POST",
//       url: "/cards/movecard/",
//       data: {
//         card: card,
//         column: column,
//         }
//       });
//     });
//     // end add card to new column
//
//   //  update card order (move within column)
//   UIkit.util.on('#{{column}}', 'moved', function (e, sortable, el) {
//     var sortResult = { elementsOrder: [] };
//     $('#{{column}} > li').each(function () {
//         var currentEl = $(this);
//         sortResult.elementsOrder.push(currentEl[0].id);
//     });
//     $.ajax({
//         type: "POST",
//         //async: true,
//         url: "/cards/updatecardorder/",
//         //traditional: true,
//         data: {
//           arr: JSON.stringify(sortResult)
//           }
//     });
//   });
//   // end update card order
//   {% endfor %}
// </script>
// {% endif %}
// <!--END NEW UIKIT -->