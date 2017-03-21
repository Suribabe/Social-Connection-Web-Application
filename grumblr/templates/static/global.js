

// function sendRequest() {
//  if (window.XMLHttpRequest) {
//         req = new XMLHttpRequest();
//     } else {
//         req = new ActiveXObject("Microsoft.XMLHTTP");
//     }
//     req.onreadystatechange = handleResponse;
//     req.open("GET", "/grumblr/main", true);
//     req.send(); 
// }
  $(".commentForm").on('keypress',function(e){ alert("");
     $(this).unbind('submit').bind('submit',function(event){
      event.preventDefault(); // Prevent form from being submitted
        var comment1=$(this);
        var post_id1=$(this).attr('id');
        var post_id=post_id1.split("-")[1];
        var comment_area=$(this).parent().siblings(".comment-list");
        var commentForm=$(this).serialize(); //alert(comment_input_id);
        $.post("/create-comment/"+post_id, commentForm, function(response) {
          if(response["message"]==undefined) {
          firstname=response["firstname"];
          lastname=response["lastname"];
          profileid=response["profileid"];
          timestamp = response["time"];
          text=response["commentText"];
         
          console.log(firstname);
          console.log(lastname);
          console.log(profileid);
          console.log(text);
          console.log(timestamp);
          var newCommentEle="<div id=\"comment-"+post_id+"\" class=\"comment-list\"> <table> <tr> <td class=\"comment_image\"> <div class=\"comment_image_div\" class=\"col-sm-2\"> <img src=\"photo/"+profileid+"\" class=\"img-circle\"  width=\"40\" height=\"40\"> </div> </td> <td> <div class=\"comment_image_div\" class=\"col-sm-10\"> <a href=\"/profile/"+profileid+"\"> "+firstname+" " +lastname+"</a> <small>"+timestamp+"</small> <p>"+text+"</p></div> </td> </tr> </table> </div>"
          comment_area.prepend(newCommentEle);
        }
        });      
     });
  });

function getUpdates(){
    var last_post =$("#allposts").attr("class");
    if (last_post==undefined) {last_post==0} 
    $.post("/get-update/"+last_post, function(response) {
      var profiles=new Object();
        $.each($.parseJSON(response["profile"]), function(key,value){
          profiles[value.pk]=value;
        });
        $.each($.parseJSON(response["posts"]), function(key,value){
          var profile_json=profiles[value.fields.profile];
          timestamp = response["time"];
          console.log(profile_json.fields.user);
          console.log(timestamp[value.pk]);
          console.log(response["last_post_id"]);
          profileid=profile_json.fields.user;
          last_post_id=response["last_post_id"];
          appendChanges(profile_json, value, timestamp[value.pk], profileid);
          $("#allposts").attr("class",response["last_post_id"]);
        });       
    });
}

  $("#create-post-form").on('submit',function(event){ 
    event.preventDefault(); // Prevent form from being submitted
    var postForm = $("#create-post-form").serialize(); 
    var last_post =$("#allposts").attr("class"); //alert($("#allposts").attr("id"));
    if (last_post==undefined) {last_post==0}
    $.post("/create-post/"+last_post, postForm, function(response) {//alert(last_post);
        //alert(response["message"]);
        if(response["message"]==undefined) {
        var profiles=new Object();
        $.each($.parseJSON(response["profile"]), function(key,value){
          profiles[value.pk]=value;
        });
        $.each($.parseJSON(response["posts"]), function(key,value){
          var profile_json=profiles[value.fields.profile];
          timestamp = response["time"];
          console.log(profile_json.fields.user);
          profileid=profile_json.fields.user;
          console.log(timestamp[value.pk]);
          console.log(response["last_post_id"]);
          last_post_id=response["last_post_id"];
          appendChanges(profile_json, value, timestamp[value.pk], profileid);
        });
        $("#allposts").attr("class",response["last_post_id"]);
      }
      });

    });

function appendChanges(profile,post,time, profileid) {
  var newEle="<div class=\"col-sm-12\"><div class=\"col-sm-2\"> <img src=\"photo/"+profile.fields.user+"\" class=\"img-circle\" id=\"img-circle\" width=\"60\" height=\"60\"></div> <div class=\"col-sm-10\" id=\"profilePost\"> <a href=\"/profile/"+profileid+"\">" + profile.fields.firstname + " " +profile.fields.lastname+"</a> <div id=\"comment-"+post.pk+"\"> <small>"+post.fields.time+"</small> <p>"+post.fields.text+"</p> </div> <div class=\"comment-area\"> <h4>Leave a Comment</h4> <form method=\"POST\" id=\"commentform-"+ post.pk +"\" class=\"commentForm\"> <textArea class=\"form-control\" rows=\"2\"  name=\"commentArea\" height=\"40\"></textArea> <input type=\"submit\" class=\"btn btn-success\" value=\"submit\"> </form> </div></div></div>"
  $(newEle).insertAfter("#allposts");
  var formid="commentform-"+post.pk;
  $("#"+formid).attr("class","commentForm");
  //alert($("#"+formid).attr("class")); 

  $("#"+formid).on('submit',function(event){     //alert("d");
      event.preventDefault(); // Prevent form from being submitted
        var comment1=$("#"+formid);
        var post_id1=$("#"+formid).attr('id');
        var post_id=post_id1.split("-")[1];
        var comment_area=$("#"+formid).parent().siblings(".comment-list"); //alert(comment_area);
        var commentForm=$("#"+formid).serialize(); //alert(comment_input_id);
        // alert(commentForm);
        // var formvalid=commentForm.split("=")[1]
        // alert(formvalid);
        $.post("/create-comment/"+post_id, commentForm, function(response) {
          //alert(response["message"]);
          if(response["message"]==undefined) {
          firstname=response["firstname"];
          lastname=response["lastname"];
          profileid=response["profileid"];
          timestamp = response["time"];
          text=response["commentText"];
         
          console.log(firstname);
          console.log(lastname);
          console.log(profileid);
          console.log(text);
          console.log(timestamp);
          var newCommentEle="<div id=\"comment-"+post_id+"\" class=\"comment-list\"> <table> <tr> <td class=\"comment_image\"> <div class=\"comment_image_div\" class=\"col-sm-2\"> <img src=\"photo/"+profileid+"\" class=\"img-circle\"  width=\"40\" height=\"40\"> </div> </td> <td> <div class=\"comment_image_div\" class=\"col-sm-10\"> <a href=\"/profile/\""+profileid+"\"> "+firstname+" " +lastname+"</a> <small>"+timestamp+"</small> <p>"+text+"</p></div> </td> </tr> </table> </div>"
          // comment_area.append(newCommentEle); alert("d");
          $(newCommentEle).insertAfter("#"+formid);
          }
        });
  });

}

var csrftoken;
$( document ).ready(function() {  // Runs when the document is ready
  // using jQuery
  // https://docs.djangoproject.com/en/1.10/ref/csrf/
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

  csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

  window.setInterval(getUpdates, 5000);

}); // End of $(document).ready



// function handleResponse() {
//  if (req.readyState != 4 || req.status != 200) {
//      return;
//  }

//     $('#postlist').empty();
//     var posts = $("#postList");

    
// }


//window.setInterval(sendRequest, 2000);