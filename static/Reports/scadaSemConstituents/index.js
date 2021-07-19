$(document).ready(function () {
    //for dataTable
    var table = $("#constituentsError").DataTable({
      dom: "Bfrtip",
      // dom: '<"dt-buttons"Bpi>rtp',
      // scrollY: 700,
      // scrollX: true,
      // scroller: true,
      fixedHeader: true,
      //orderCellsTop: true,
      lengthMenu: [96, 192, 188],
  
      buttons: {
        dom: {
          button: {
            tag: "button",
            className: "",
          },
        },
        buttons: [
          {
            extend: "pageLength",
            className: "btn btn-dark rounded-0",
            text: '<i class="far fa-page"></i> Show Entries',
          },
          {
            extend: "copy",
            className: "btn btn-dark rounded-0",
            text: '<i class="far fa-copy"></i> Copy',
          },
          {
            extend: "excel",
            className: "btn btn-dark rounded-0",
            text: '<i class="far fa-file-excel"></i> Excel',
          },
          {
            extend: "pdf",
            className: "btn btn-dark rounded-0",
            text: '<i class="far fa-file-pdf"></i> Pdf',
          },
          {
            extend: "csv",
            className: "btn btn-dark rounded-0",
            text: '<i class="fas fa-file-csv"></i> CSV',
          },
          {
            extend: "print",
            className: "btn btn-dark rounded-0",
            text: '<i class="fas fa-print"></i> Print',
          },
        ],
      },
    });
});