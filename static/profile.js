
  $(".commentForm").on('keypress',function(e){
     $(this).unbind('submit').bind('submit',function(event){
      event.preventDefault(); // Prevent form from being submitted
        var comment1=$(this);
        var post_id1=$(this).attr('id');
        var post_id=post_id1.split("-")[1];
        var comment_area=$(this).parent().siblings(".comment-list");
        var commentForm=$(this).serialize(); //alert(comment_input_id);
        $.post("/create-comment/"+post_id, commentForm, function(response) {
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
          var newCommentEle="<div id=\"comment-"+post_id+"\" class=\"comment-list\"> <table> <tr> <td class=\"comment_image\"> <div class=\"comment_image_div\" class=\"col-sm-2\"> <img src=\"../photo/"+profileid+"\" class=\"img-circle\" width=\"40\" height=\"40\"> </div> </td> <td> <div class=\"comment_image_div\" class=\"col-sm-10\"> <a href=\"/profile/"+profileid+"\"> "+firstname+" " +lastname+"</a> <small>"+timestamp+"</small> <p>"+text+"</p></div> </td> </tr> </table> </div>"
          comment_area.prepend(newCommentEle);
        });     
     });
  });
