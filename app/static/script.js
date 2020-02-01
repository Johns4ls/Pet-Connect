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
function submitComment(postID, commentSock){
    comment = document.getElementById("Comment").value;
    commentSock.emit('sendComment',
    {'postID': postID, 'Comment': comment})
    commentSock.on('returnComment', function(messages) {
    console.log(messages)
    if(messages.message == 'Fail'){
        alert("Failed to add comment")
    }
    else{
        document.getElementById("Comment").value = "";
    }
    });
}