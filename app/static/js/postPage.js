var templates = document.querySelector("template").content;

// CopyLinkBTN
var copyLinkBtn = document.querySelector('button.copy-link-btn');
let hoverText = copyLinkBtn.querySelector('.hovertext')
var link = document.querySelector('input.copy-link');
link.value = window.location.href;

copyLinkBtn.addEventListener("click", function() {
    link.select();
    document.execCommand("copy");
    window.getSelection().removeAllRanges(); 

    hoverText.classList.add("clicked");
    hoverText.textContent = "Copied by";
})

copyLinkBtn.addEventListener("mouseout", function() {
    hoverText.classList.remove("clicked");
    hoverText.textContent = "Link copy";
})

// comments
function textareaAutosize(textarea, counter, count) {
    count.textContent = textarea.value.length;

    if (count > 1000 || count == 0) {
        counter.style.color = "#e74c3c";
        submit.disabled = true;
        textarea.classList.add("error");
    } else {
        counter.style.color = "#34495e";
        submit.disabled = false;
        textarea.classList.remove("error");
    }

    if(textarea.scrollTop > 0){
        textarea.style.height = textarea.scrollHeight + "px";
    }
}

function replyBtnOnclick(replyBtn, comment) {
    let replyFormBox = comment.querySelector('.reply-form-box');
    if (!replyBtn.classList.contains("close-btn")) {
        let replyForm = templates.querySelector('.reply-form').cloneNode(true);
        replyBtn.textContent = "Cancel";
        replyBtn.classList.add("close-btn");
        replyFormBox.appendChild(replyForm);
        replyFormBox.classList.remove("hidden");
        
        let textarea = replyForm.querySelector("textarea");
        let counter = replyForm.querySelector(".counter");
        let count = replyForm.querySelector(".count");
        count.textContent = textarea.value.length;
        replyForm.addEventListener("keyup", function() {
            textareaAutosize(textarea, counter, count)
        })
        replyForm.addEventListener("submit", function(evt) {
            evt.preventDefault();
            if (comment.classList.contains(".reply")) {
                var replyesBox = comment.parentNode;
            } else {
                var replyesBox = comment.querySelector('.replyes');
            }
            replySubmit(replyForm, comment.id, replyesBox);
        });
    } else {
        comment.querySelector(".reply-form").remove();
        replyFormBox.classList.add("hidden");
        replyBtn.textContent = "Reply";
        replyBtn.classList.remove("close-btn");
    }
}

function replySubmit(replyForm, commentId, replyesBox) {
    textarea = replyForm.querySelector("textarea.reply-text");
    if (textarea.value.length !== 0) {
        let request = new XMLHttpRequest();
        let url = window.location.pathname + '/reply-comment';
        let requestObj = {
            text: textarea.value,
            replyedCommentId: commentId
        };
        request.open('POST', url, true);
        request.responseType = 'json';
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.send(JSON.stringify(requestObj));

        request.onload = function() {
            let data = request.response;
            console.log(data)
            addComment(data, replyesBox, isReply=true);
            textarea.value = 0;
            replyForm.classList.add("hidden")
            let comment = document.getElementById(commentId);
            let showReplyBtn = comment.querySelector('button.show-close-comments');
            showReplyBtn.disabled = false;
            let replyesCount = parseInt(showReplyBtn.getAttribute("reply-count")) + 1;
            showReplyBtn.setAttribute("reply-count", replyesCount);
            showReplyBtn.addEventListener("click", function() {
                let replyesBox = comment.querySelector('.replyes');
                if (this.getAttribute("is-open") == "false"){
                    replyesBox.classList.remove("hidden");
                    this.textContent = "Close comments";
                    this.setAttribute("is-open", "true");
                } else if (this.getAttribute("is-open") == "true") {
                    replyesBox.classList.add("hidden");
                    this.innerHTML = 'Show comments (<span class="replyes-count">' + replyesCount +'</span>)';
                    this.setAttribute("is-open", "false");
                }
            });
        };
    } 
};

function showAndCloseComments(comment) {
    let showReplyBtn = comment.querySelector('button.show-close-comments');
    let replyesCount = showReplyBtn.getAttribute('reply-count')
    if (replyesCount == 0) {
        showReplyBtn.disabled = true;
    } else {
        showReplyBtn.addEventListener("click", function() {
            let replyesBox = comment.querySelector('.replyes');
            if (this.getAttribute("is-open") == "false"){
                replyesBox.classList.remove("hidden");
                this.textContent = "Close comments";
                this.setAttribute("is-open", "true");
            } else if (this.getAttribute("is-open") == "true") {
                replyesBox.classList.add("hidden");
                this.innerHTML = 'Show comments (<span class="replyes-count">' + replyesCount +'</span>)';
                this.setAttribute("is-open", "false");
            }
        });
    }
};

var allComments = document.querySelectorAll('.comment-list .comment');
allComments.forEach(function(comment) {
    let replyBtn = comment.querySelector("button.reply-btn");
    if (!comment.classList.contains('reply')) {
        showAndCloseComments(comment)
    }

    replyBtn.addEventListener("click", function() {
        replyBtnOnclick(replyBtn, comment)
    });

});

//  post comment add
var commentForm = document.querySelector("form.comment-form");
var counter = commentForm.querySelector(".counter");
var count = counter.querySelector(".count");
var commentTextArea = commentForm.querySelector("textarea");
var submit = commentForm.querySelector("input.submit");

count.textContent = commentTextArea.value.length;



commentTextArea.addEventListener("keydown", function() {
    textareaAutosize(commentTextArea, counter, count);
});
commentTextArea.addEventListener("keyup", function() {
    textareaAutosize(commentTextArea, counter, count);
});

commentForm.addEventListener("submit", function(evt) {
    evt.preventDefault();
    if (commentTextArea.value.length != 0) {
        let url = window.location.pathname + "/comment-post";
        request = new XMLHttpRequest();
        request.open("POST", url, true);
        request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        request.responseType = 'json';
        request.send(JSON.stringify({text: commentTextArea.value}));
        commentTextArea.value = '';
        
        commentTextArea.style.height = "72px";
        request.onload = function() {
            let data = request.response;
            console.log(data);    
            let commentList = document.querySelector(".comment-list");
            addComment(data, commentList);
        }
    } else {
        submit.disabled = true;
        submit.classList.add('error');
        commentTextArea.classList.add("error");
    }
})

function addComment(data, commentBox, isReply=false) {
    if (!isReply) {
        var comment = templates.querySelector(".comment").cloneNode(true);
    } else {
        var comment = templates.querySelector(".reply.comment").cloneNode(true);
    }
    let authorLink = comment.querySelector(".author-link");
    let date = comment.querySelector(".date");
    let text = comment.querySelector(".text");

    authorLink.textContent = '@' + data.author;
    let authorUrl = '/u/' + data.author;

    authorLink.setAttribute('href', authorUrl);
    date.textContent = data.date;
    text.textContent = data.text;
    comment.id = data.id;

    if (isReply) {
        let replyedCommentLink = comment.querySelector('.replyed-comment');
        replyedCommentLink.setAttribute("href", "#" + data.replyed_c_id);
        replyedCommentLink.textContent = "@" + data.replyed_c_author;
    } else {
        let replyes_count = comment.querySelector('.replyes-count');
        replyes_count.textContent = 0;

        showAndCloseComments(comment)
    }
    commentBox.insertBefore(comment, commentBox.firstChild);

    let replyBtn = comment.querySelector('.reply-btn')
    replyBtn.addEventListener("click", function() {
        replyBtnOnclick(this, comment);
    });
    if (!comment.classList.contains("reply")) {
        showAndCloseComments(comment)    
    }
}


//  like and dislike buttons work

let likeBtn = document.getElementById("like");
let dislikeBtn = document.getElementById("dislike");

function updateStatistics(data) {
    let statistics = document.querySelector(".post-head .statistics");
    let likeCounter = statistics.querySelector('.like-count');
    likeCounter.textContent = data.likes;
    let dislikeCounter = statistics.querySelector('.dislike-count');
    dislikeCounter.textContent = data.dislikes;
    let viewCounter = statistics.querySelector('.view-count');
    viewCounter.textContent = data.views;
    let commentCounter = statistics.querySelector(".comment-count");
    commentCounter.textContent = data.comments;
}

likeBtn.addEventListener("click", function() {
    let url = window.location.pathname + "/like/1";
    let request = new XMLHttpRequest();
    request.open("POST", url, true);
    request.responseType = "json";
    request.send();

    request.onload = function() {
        updateStatistics(request.response)
    }
})

dislikeBtn.addEventListener("click", function() {
    let url = window.location.pathname + "/like/0";
    let request = new XMLHttpRequest();
    request.open("POST", url, true);
    request.responseType = "json";
    request.send();

    request.onload = function() {
        updateStatistics(request.response)
    }
})

