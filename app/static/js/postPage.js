var templates = document.querySelector("template").content;

// CopyLinkBTN
var copyLinkBtn = document.querySelector('button.copy-link-btn');
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
            replySubmit(replyForm)
        });
    } else {
        comment.querySelector(".reply-form").remove();
        replyFormBox.classList.add("hidden");
        replyBtn.textContent = "Reply";
        replyBtn.classList.remove("close-btn");
    }
}

function replySubmit(replyForm) {
    textarea = replyForm.querySelector("textarea.reply-text");
    console.log(textarea.value);
};
var allComments = document.querySelectorAll('.comment-list .comment');
allComments.forEach(function(comment) {
    let replyBtn = comment.querySelector("button.reply-btn"); 
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
    textareaAutosize(this, counter, count);
});
commentTextArea.addEventListener("keyup", function() {
    textareaAutosize(this, counter, count);
});

commentForm.addEventListener("submit", function(evt) {
    evt.preventDefault();
    if (commentTextArea.value.length != 0) {
        

        url = window.location.pathname + "/comment-post";
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
            addComment(data);
            
        }
    } else {
        submit.disabled = true;
        submit.classList.add('error');
        commentTextArea.classList.add("error");
    }
})

function addComment(data) {
    let commentList = document.querySelector(".comment-list");
    let comment = templates.querySelector(".comment").cloneNode(true)

    let authorLink = comment.querySelector(".author-link");
    let date = comment.querySelector(".date");
    let text = comment.querySelector(".text");

    authorLink.textContent = '@' + data.author;
    let authorUrl = '/auhtor/' + data.author;
    console.log(authorUrl);
    authorLink.setAttribute('href', authorUrl);
    date.textContent = data.date;
    text.textContent = data.text;
    comment.setAttribute('comment-id', data.id);
    commentList.insertBefore(comment, commentList.firstChild);
}



