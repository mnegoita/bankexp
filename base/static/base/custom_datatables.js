/*--------------------------------------------------------------
# Datatables customization
--------------------------------------------------------------*/
  
$(document).ready(function() {
    
    var strIconSearch = '<i class="icofont-search"></i>';
    var resumesTable = $('.bankexpTable').DataTable( {
        ordering: false,
        responsive: true,
        language: {
            search: strIconSearch,
        },
        dom: 'Bfrtip',
        buttons: { 
            buttons: [ 
            {extend: 'csvHtml5'},
            {extend: 'excelHtml5'},
            {extend: 'pdfHtml5'},
            {extend: 'pageLength', className: 'btn-test1',}
            ], 
            dom: { button: {className: 'dt-button'} }
        } 
    })
    $("#resumesTable_filter input").attr('placeholder', 'Search...');
});
  
