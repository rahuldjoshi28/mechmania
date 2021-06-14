function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function reactReq(i, id){
	var c;
	if(i == 1){
		c = "accept";
	}
	else if(i == 0){
		c = "reject";
	}

	var csrftoken = getCookie('csrftoken');

	$.post("/internships/notificationResp/",
		{
			'pk':id,
			'response': c,
			'csrfmiddlewaretoken': csrftoken,
		}
	);
}

function reactReqPro(i, id){
	var c;
	if(i == 1){
		c = "accept";
	}
	else if(i == 0){
		c = "reject";
	}

	var csrftoken = getCookie('csrftoken');

	$.post("/projects/notificationResp/",
		{
			'pk':id,
			'response': c,
			'csrfmiddlewaretoken': csrftoken,
		}
	);
}


function writeNotice(data){
	data = data.messages;
	var ans = "";
	for(var i=0; i<data.length; ++i){
		if(data[i].label == "gen_notice"){
			ans +=  '<div class="dropdown-item custom-not-dropdown-item nopadding">'
					+'<div class="row col-md-12 nomargin" style="padding-left:0;padding-right:0">'
					+'<div class="col-md-12 nopadding" href="#" >'
					+'<h6 class="col-md-12" style="word-wrap:break-word;white-space: normal;">'
					+data[i].data.message
					+'<br><br>'
					+'<small style="color:#737373;">'+data[i].timestamp+'</small>'
					+'</h6></div></div>'
					+'</div>'
					+'<div class="dropdown-divider" style="border-color:#464a53;"></div>';
		}
		else if(data[i].label == "iv_request"){
			ans +=
				'<div class="dropdown-item custom-not-dropdown-item nopadding">'
				+'<div class="row col-md-12 nomargin" style="padding-left:0;padding-right:0">'
				+'<div class="col-md-12 nopadding" href="#">'
				+'<h6 class="col-md-12" style="word-wrap:break-word;white-space: normal;">'
				+data[i].data.user+' invited you for visiting '+data[i].data.company+' Want to accept ?'
				+'<br><div class="row col-md-12 nomargin">'
				+'<button type="button"class="btn btn-secondary btn-sm col-md-4"style="border:none; cursor:pointer; color:GREEN; background-color:#2f3238;" onclick="reactReq(1,'+data[i].data.pk+')"><i class="fas fa-check-circle"></i>&nbsp;&nbsp;Accept</button>'
				+'<div class="col-md-1"><br></div>'
				+'<button type="button"class="btn btn-secondary btn-sm col-md-4"style="border:none; cursor:pointer; color:RED; background-color:#2f3238;" onclick="reactReq(0,'+data[i].data.pk+')"><i class="fas fa-times-circle"></i>&nbsp;&nbsp;Reject</button>'
				+'</div>'
				+'<small style="color:#737373;">'+data[i].timestamp+'</small>'
				+'</h6></div></div></div>'
				+'<div class="dropdown-divider" style="border-color:#464a53;"></div>';
		}
		else{
			ans +=
				'<div class="dropdown-item custom-not-dropdown-item nopadding">'
				+'<div class="row col-md-12 nomargin" style="padding-left:0;padding-right:0">'
				+'<div class="col-md-12 nopadding" href="#">'
				+'<h6 class="col-md-12" style="word-wrap:break-word;white-space: normal;">'
				+data[i].data.user+' invited you for '+ data[i].data.type +' project @ '+data[i].data.company+' Want to accept ?'
				+'<br><div class="row col-md-12 nomargin">'
				+'<button type="button"class="btn btn-secondary btn-sm col-md-4"style="border:none; cursor:pointer; color:GREEN; background-color:#2f3238;" onclick="reactReqPro(1,'+data[i].data.pk+')"><i class="fas fa-check-circle"></i>&nbsp;&nbsp;Accept</button>'
				+'<div class="col-md-1"><br></div>'
				+'<button type="button"class="btn btn-secondary btn-sm col-md-4"style="border:none; cursor:pointer; color:RED; background-color:#2f3238;" onclick="reactReqPro(0,'+data[i].data.pk+')"><i class="fas fa-times-circle"></i>&nbsp;&nbsp;Reject</button>'
				+'</div>'
				+'<small style="color:#737373;">'+data[i].timestamp+'</small>'
				+'</h6></div></div></div>'
				+'<div class="dropdown-divider" style="border-color:#464a53;"></div>';
		}
	}
	document.getElementById("noticePanel").innerHTML = ans;

  var api = $('.scroll-pane').data('jsp');
  if(api != undefined)
    api.destroy();

  $('.scroll-pane').jScrollPane(
    {
      contentWidth: 1,
      showArrows: false
    }
  );
}


function fetchNotices(){
	$.post('/shortNotifications/',{
		'csrfmiddlewaretoken': getCookie('csrftoken')
		},
		function(data){
			JSON.stringify(data);
			writeNotice(data);
	});
}
