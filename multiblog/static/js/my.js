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