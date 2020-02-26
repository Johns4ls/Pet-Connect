function commentSock() { 
    userInfoNamespace = '/Comments/';
    var commentSock = io.connect(location.protocol + '//' + document.domain + ':' + location.port + userInfoNamespace, {
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax : 5000,
    reconnectionAttempts: 99999
    }); 
    commentSock.emit('connect',{});
    return commentSock
}
function submitComment(view, postID, commentSock){
    comment = document.getElementById(view+"Comment"+postID).value;
    commentSock.emit('sendComment',
    {'postID': postID, 'Comment': comment})
    commentSock.on('returnComments', function(messages) {
        if(messages.message != 'Fail'){
            for (var i=0; i < messages.message.length; i++){
                var text = "";
                text += "<p> \n"
                comment = messages.message[i]

                if (comment.image == null)
                {
                    text += "<a href=\"/static/pictures/Profile/thor'.jpg')\"> \n"
                    text += "<img src=\"/static/pictures/Profile/thor.thumbnail')\"class=\"img-thumbnail\"></a> \n"
                }
                else
                {
                    text += "<a href=\"/static/" + comment.image + ".jpg \"> \n"
                    text += "<img src=\"/static/" + comment.image + ".thumbnail \"class=\"img-thumbnail\"></a> \n"
                }
                text += "<a href=\"/User/Profile/"+ comment.userID + "\"><b style=\"color: #0d6591;\">" + comment.firstName + " " + comment.lastName + "</b></a> said: </p> \n"
                text += "<p>" + comment.Comment + "</p> \n"
                try{
                document.getElementById("mobilesubcommentcontainer"+comment.postID+(i)).innerHTML = text
                }
                catch{
                    console.log("Has mobile been implemented on this page?")
                }
                document.getElementById("desktopsubcommentcontainer"+comment.postID+(i)).innerHTML = text
            }
        }
        if(messages.message == 'Fail')
        {
            alert("Failed to add comment")
        }
        else
        {
            document.getElementById(view+"Comment"+postID).value = "";
        }
    });
}