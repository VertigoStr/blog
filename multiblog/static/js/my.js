$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});


$('document').ready(function(){
    $('#modal').modal({show: false});
});


$('.delete-object').on('click', function(e){
	var post_id = $(this).attr('data-id');
	$('#file-to-delete').html('<strong>' + $(this).attr('data-title') + '</strong>');

	$('#confirm').on('click', function(e){
		// console.log(post_id);		
		$.ajax({
			url: window.location.pathname,
			type: "GET",
			data : {"post_id":post_id},

			success: function(json){
				if(!json.error) {
					$("#" + post_id).remove();  
					$('#confirm-delete').modal('hide');
				}
			},

			error: function(xhr, errmsg, err) {
				alert("Something went wrong!");
				// alert(xhr.status + ": " + xhr.responseText);
			}
		});
	});
});

var sort_page = function(f, st) {
	var field = f, sort_type = st;
	var list = $('.index-page').get();
	var new_list = new Array();

	for (var i in list)
		new_list.push({indx: i, val: list[i]['attributes'][field].value});

	new_list.sort(function(a,b) {
    	return sort_type == 'asc' ? a.val > b.val : a.val < b.val; 
	});
	
	for (var i in list)
		document.getElementById("main_page").insertBefore(list[new_list[i].indx], document.getElementById("navigation"));
}

$('.sort-page-time-desc').on('click', function(e){
	sort_page(2,'desc');
});

$('.sort-page-time-asc').on('click', function(e){
	sort_page(2,'asc');
});
$('.sort-page-name-desc').on('click', function(e){
	sort_page(1,'desc');
});

$('.sort-page-name-asc').on('click', function(e){
	sort_page(1,'asc');
});