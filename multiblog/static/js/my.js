$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});


$('document').ready(function(){
    $('#modal').modal({show: false});

	var name = $('#get-names').attr('data-name'), 
		surname = $('#get-names').attr('data-surname'),
		phone = $('#get-phone').attr('data-phone'),
		skype = $('#get-skype').attr('data-skype');

	var add_email = (name + surname).length == 0;
	$('#input-name').html('<input class="form-control" type="text" id="name" value='+ name +'>');
	$('#input-surname').html('<input class="form-control" type="text" id="surname" value='+ surname +'>');
	if (phone)
		$('#input-phone').html('<input class="form-control" type="text" id="phone" value='+ phone +'>');

	if (skype)
		$('#input-skype').html('<input class="form-control" type="text" id="skype" value='+ skype +'>');
	
    $('#submit-edit').on('click', function(e){

    	var csrftoken = getCookie('csrftoken');
		e.preventDefault();

    	var params = {'name': $('#name').val(), 'surname': $('#surname').val(), 'phone' : $('#phone').val(), 'skype' : $('#skype').val() }
    	$.ajax({
			url: window.location.pathname,
			type: "POST",
			data : {
					"new_name" : params['name'], 
					"new_surname" : params['surname'],
					"new_phone" : params['phone'],
					"new_skype" : params['skype'],
					'new_avatar' : params['avatar']
				},

			beforeSend: function(xhr, settings) {
        		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            		xhr.setRequestHeader("X-CSRFToken", csrftoken);
        		}
    		},

			success: function(json){
				if(!json.error) {
					$('#modal').modal('hide');
					var full_name = params['name'] + " " + params['surname'],
						email = $('#get-names').attr('data-email');

					$('#get-names').attr('data-name', params['name']);
					$('#get-names').attr('data-surname', params['surname']);
					$('#get-names').html((full_name.length != 1 ? full_name : email)
							 + '<a href="#modal" role="button" class="btn" data-toggle="modal" ><span class="glyphicon glyphicon-pencil"></span></a>'
							 );

					$('.index-page').attr('data-author',
						 full_name.length != 1 ? full_name : email);
					$('.author-title').html(full_name.length == 1 ? email : full_name);


					if (add_email) {
						if (!$('#get-phone').attr('data-phone'))
							$('.contact-info').prepend('<div class="col-lg-6"><h6>Телефон</h6></div><div class="col-lg-6" id="get-phone" data-phone="' + params['phone'] + '"><h6>' + params['phone'] + '</h6></div>');

						if (!$('#get-email').attr('data-email') && full_name.length != 1)
							$('.contact-info').prepend('<div class="col-lg-6"><h6>Email</h6></div><div class="col-lg-6" id="get-email" data-email="' + params['email'] + '"><h6>' + email + '</h6></div>');

						if (!$('#get-skype').attr('data-skype'))
							$('.contact-info').prepend('<div class="col-lg-6"><h6>Skype</h6></div><div class="col-lg-6" id="get-skype" data-skype="' + params['skype'] + '"><h6>' + params['skype'] + '</h6></div>');
					}

					$('#get-phone').attr('data-phone', params['phone']);
					$('#get-phone').html('<h6>' + params['phone'] + '</h6>');

					$('#get-skype').attr('data-skype', params['skype']);
					$('#get-skype').html('<h6>' + params['skype'] + '</h6>');
				}
			},

			error: function(xhr, errmsg, err) {
				alert("Something went wrong!");
				//alert(xhr.status + ": " + xhr.responseText);
			}
		});
    });
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

$('.sort-page').on('click', function(e){
	$('[data-toggle="tooltip"]').tooltip('hide');
	var args = $(this).attr('act').split('-')
	sort_page(args[0], args[1]);
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function create_comment() {
	var csrftoken = getCookie('csrftoken');
	$.ajax({
		url: window.location.pathname,
		type: "POST",
		data: {'comment': $('#comment').val()},

		beforeSend: function(xhr, settings) {
        	if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            	xhr.setRequestHeader("X-CSRFToken", csrftoken);
        	}
    	},

		success: function(json) {
			if(!json.error) {
				$('#comment').val('');
				$('#comments').prepend('<div class="media"><a class="pull-left" href="#"><img class="media-object" src="'
				 + json.avatar + '" width="64" height="64"></a><div class="media-body"><h4 class="media-heading"><a href="/my_profile/'
				 + json.author_id +'">'
				 + json.author + '</a></h4><p>' 
				 + json.txt + '</p><p class="post-meta"><time datetime="' 
				 + json.when + '">' 
				 + json.when + '</time></p></div></div>'
				);
				
			}
		},

		error: function(xhr, errmsg, err) {
			alert(xhr.status + ": " + xhr.responseText);
		}

	});
};


$('#comment-form').on('submit', function(e) {
	e.preventDefault();
	create_comment()
});