$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});


$('#upload-btn').on('click', function(e) {
});

$('article').click(function(e){
	e.preventDefault()
	var cat = $(this).attr('id');

	if (cat){
		$.ajax({
			url: window.location.pathname,
			type: 'GET',
			data: { 'cat_id':cat },

			success: function(json){
				if (!json.error) {
					$('#posts').empty();
					//var sourceHtml = $('#').html(); 
					//var template = Handlebars.compile(sourceHtml);
					//var element = template({author: json.author})

					$('.sort-main').prepend('<ol><a href="#" class="sort-page" act="2-desc" data-placement="bottom" data-toggle="tooltip" title="Сортировка по убыванию даты публикации" ><span class="glyphicon glyphicon-sort-by-order-alt"></span></a></ol>');
					$('.sort-main').prepend('<ol><a href="#" class="sort-page" act="2-asc" data-placement="bottom" data-toggle="tooltip" title="Сортировка по возрастанию даты публикации"><span class="glyphicon glyphicon-sort-by-order"></span></a></ol>');
					$('.sort-main').prepend('<ol><a href="#" class="sort-page" act="1-desc" data-placement="bottom" data-toggle="tooltip" title="Сортировка в обратном алфавитном порядке"><span class="glyphicon glyphicon-sort-by-alphabet-alt"></span></a></ol>');
					$('.sort-main').prepend('<ol><a href="#" class="sort-page" act="1-asc" data-placement="bottom" data-toggle="tooltip" title="Сортировка в алфавитном порядке"><span class="glyphicon glyphicon-sort-by-alphabet"></span></a></ol>');
					$('#navigation').prepend('<a id="left" href=""><span class="glyphicon glyphicon-arrow-left"></span></a><span id="page-number">1</span><a id="right" href=""><span class="glyphicon glyphicon-arrow-right"></span></a>');
					$('#navigation').attr('cat-id', cat);
					// $('body').append(element);
					for (var i = 1; i < json.length; i++) {
					$('#posts').prepend('<article class="index-page" data-author="' 
						+ json[i].author + '" data-time="'
						+ json[i].when + '"><h4><a href="/publication/'
						+ json[i].post_id + '">' 
						+ json[i].post_title + '</a></h4><p class="post-meta"><time datetime="' 
						+ json[i].when + '">' 
						+ json[i].when + '</time>&nbsp;/&nbsp;<span item="author"><a href="/my_profile/' 
						+ json[i].author_id + '">' 
						+ json[i].author + '</a></span></p><p>' 
						+ json[i].txt + '</p></article>');
					}
				}
			}

		});
	}
});

$('.rating').click(function(e) {
	var rating_value = $(this).attr('value'),
		post_id = $('h2').attr('id'),
		is_enable = $.parseJSON($('#rating').attr('data-enable'));

	if (rating_value && is_enable) {
		$.ajax({
			url: '/rating/',
			type: 'GET',
			data: {'rating_value':rating_value, 'post_id' : post_id},

			success: function(json){
				if (!json.error){
					$('#rating').empty()
					var i = 0;
					while (i < 5) {
						if (i < json.res) 
							$('#rating').append('<span class="glyphicon glyphicon-star rating" value="' + (i + 1) + '"></span>')
						else 
							$('#rating').append('<span class="glyphicon glyphicon-star-empty rating" value="' + (i + 1) + '"></span>')
						i++;
					}
				}
			},

			error: function(xhr, errmsg, err) {
				console.log(xhr.status + ": " + xhr.responseText);
			}

		});
	}
});


$('#go_search').on('click', function(e){
	var input = $('#input-search').val();
	if (input) {
		$.ajax( {
			url: 'search',
			type: 'GET',
			data: {'search_value':input},

			success : function(json) {
				if (!json.error) {
					$('#posts').empty();
					$('#navigation').empty();
					for (var i = 0 in json) {
						$('#posts').prepend('<article class="index-page" data-author="' 
							+ json[i].author + '" data-time="'
							+ json[i].when + '"><h4><a href="/publication/'
							+ json[i].post_id + '">' 
							+ json[i].post_title + '</a></h4><p class="post-meta"><time datetime="' 
							+ json[i].when + '">' 
							+ json[i].when + '</time>&nbsp;/&nbsp;<span item="author"><a href="/my_profile/' 
							+ json[i].author_id + '">' 
							+ json[i].author + '</a></span></p><p>' 
							+ json[i].txt + '</p></article>');
					}
				}
			}, 

			error: function(xhr, errmsg, err) {
					//alert("Something went wrong!");
					console.log(xhr.status + ": " + xhr.responseText);
				}
		});
	}
});


$('document').ready(function(){
    $('#modal').modal({show: false});

	var name = $('#get-names').attr('data-name'), 
		surname = $('#get-names').attr('data-surname'),
		phone = $('#get-phone').attr('data-phone'),
		skype = $('#get-skype').attr('data-skype'),
		id = $('#get-names').attr('data-id');

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

    	var params = {'name': $('#name').val(), 'surname': $('#surname').val(), 'phone' : $('#phone').val(), 'skype' : $('#skype').val()}
    	//console.log(params);
    	$.ajax({
			url: '/edit/' + id + '/',
			type: "POST",
			data : {
					"edit" : "edit",
					"new_name" : params['name'], 
					"new_surname" : params['surname'],
					"new_phone" : params['phone'],
					"new_skype" : params['skype'],
				},

			beforeSend: function(xhr, settings) {
        		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            		xhr.setRequestHeader("X-CSRFToken", csrftoken);
        		}
    		},

			success: function(json){
				if(!json.error) {
					$('#modal').modal('hide');
					var email = $('#get-names').attr('data-email'),
						full_name = params['name'] + " " + params['surname'],
						add_email = false;

					$('.contact-info').empty();
					$('#title-params').empty();

					if (params['phone']) {
						$('.contact-info').prepend('<div class="col-lg-6"><h6>Телефон</h6></div><div class="col-lg-6" id="get-phone" data-phone="' + params['phone'] + '"><h6>' + params['phone'] + '</h6></div>');
					}

					if (params['skype']) {
						$('.contact-info').prepend('<div class="col-lg-6"><h6>Skype</h6></div><div class="col-lg-6" id="get-skype" data-skype="' + params['skype'] + '"><h6>' + params['skype'] + '</h6></div>');
					}

					if (params['name'] || params['surname']) {
						add_email = true;
						$('.index-page').attr('data-author', full_name);
						$('.author-title').html(full_name);

						$('#title-params').prepend('<h3 class="featurette-heading" id="get-names" data-name="' 
							+ params['name'] + '" data-surname="' + params['surname'] + '" data-email="' + email + '" data-id="' + id + '">' + full_name + '<a href="#modal" role="button" class="btn" data-toggle="modal" ><span class="glyphicon glyphicon-pencil"></span></a></h3>');
					} else {
						$('.index-page').attr('data-author', email);
						$('.author-title').html(email);
						$('#title-params').prepend('<h3 class="featurette-heading" id="get-names" data-email="' + email + '">' + email + '<a href="#modal" role="button" class="btn" data-toggle="modal" ><span class="glyphicon glyphicon-pencil"></span></a></h3>');
					}
					if (add_email){
						$('.contact-info').prepend('<div class="col-lg-6"><h6>Email</h6></div><div class="col-lg-6" id="get-email" data-email="' + email + '"><h6>' + email + '</h6></div>');
					}
				}
			},

			error: function(xhr, errmsg, err) {
				//alert("Something went wrong!");
				console.log(xhr.status + ": " + xhr.responseText);
			}
		});
    });
});


$('.delete-object').on('click', function(e){
	var post_id = $(this).attr('data-id');
	$('#file-to-delete').html('<strong>' + $(this).attr('data-title') + '</strong>');

	$('#confirm').on('click', function(e){
		//console.log(post_id);		
		$.ajax({
			url: '/delete/',
			type: "GET",
			data : {"post_id":post_id},

			success: function(json){
				if(!json.error) {
					$("#" + post_id).remove();  
					$('#confirm-delete').modal('hide');
				}
			},

			error: function(xhr, errmsg, err) {
				//alert("Something went wrong!");
				alert(xhr.status + ": " + xhr.responseText);
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
		document.getElementById("posts").appendChild(list[new_list[i].indx]);
}

$('body').on('click', '.sort-page', function(e){
	alert($(this).attr('act'));
	$('[data-toggle="tooltip"]').tooltip('hide');
	var args = $(this).attr('act').split('-')
	console.log(args);
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

				var count = parseInt($('.muted').attr('value'));
				count++;
				$('.muted').attr('value', count);
				$('.muted').html(count + " Комментариев");				
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


function paginator(page) {
	$.ajax({
		url: window.location.pathname,
		type: "GET",
		data: {'page': page, "cat-id" : $('#navigation').attr('cat-id')},

		success : function(json) {
			if (!json.error) {
				$('#posts').empty();
				console.log(json)
				for (var i = 1; i < json.length; i++) {
					$('#posts').prepend('<article class="index-page" data-author="' 
						+ json[i].author + '" data-time="'
						+ json[i].when + '"><h4><a href="/publication/'
						+ json[i].post_id + '">' 
						+ json[i].post_title + '</a></h4><p class="post-meta"><time datetime="' 
						+ json[i].when + '">' 
						+ json[i].when + '</time>&nbsp;/&nbsp;<span item="author"><a href="/my_profile/' 
						+ json[i].author_id + '">' 
						+ json[i].author + '</a></span></p><p>' 
						+ json[i].txt + '</p></article>');
				}
				$('#page-number').html(page == json[0].pages + 1 ? page - 1: page);
			}
		}, 

		error: function(xhr, errmsg, err) {
			console.log(xhr.status + ": " + xhr.responseText);			
		}

	});
}


$('body').on('click', '#right', function(e) {
	e.preventDefault();
	var page = parseInt($('#page-number').text());
	page = page + 1;
	paginator(page);
});

$('body').on('click', '#left', function(e) {
	e.preventDefault();
	var page = parseInt($('#page-number').text());
	paginator(page <= 1 ? page : page - 1);
});