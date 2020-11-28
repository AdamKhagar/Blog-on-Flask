// get and paste posts into div.poste


var postsBox = document.querySelector('div.posts');
var templates = document.querySelector('template').content;
var form = document.querySelector('#post-search');

function closeShowPosts(postList, currentPostId) {
    postList.forEach(function(post) {
        if (post.getAttribute("post-id") != currentPostId) {
            post.classList.toggle("hidden")
        }
    })
};

function addPosts(posts) {
    if (posts.length == 0) {
        let post = templates.querySelector(".post.not-found");

        post.textContent = "Nothing found at your request";
        postsBox.insertBefore(post, postsBox.lastChild)
        post.classList.add("not-found");
    } else {
        for (let i = 0; i < posts.length; i++) {
            let data = posts[i];
            let post = templates.querySelector('.post.ok').cloneNode(true);
            let title = post.querySelector('.title');
            let date = post.querySelector('.date');
            let content = post.querySelector('.content');
            let author = post.querySelector('.author');
            let authorLink = post.querySelector("a.author-link");
            let copyLinkBtn = post.querySelector(".copy-link-btn");
            let link = document.createElement("input");
            let readAllBtn = post.querySelector(".read-all-btn");
            let viewCount = post.querySelector("span.view-count");
            let likeCount = post.querySelector("span.like-count");
            let dislikeCount = post.querySelector("span.dislike-count");
            let commentCount = post.querySelector("span.comment-count")
            
            let linkText = window.location.host + '/post/' + data.id;
            link.type = "text";
            link.value = linkText;
            link.classList.add("non-visible");
            post.setAttribute('post-id', data.id);
            post.setAttribute('category-id', data.category_id);
            title.textContent = data.title;
            date.textContent = data.publication_date;
            content.innerHTML = data.prev_text;
            author.textContent = '@' + data.author;
            readAllBtn.setAttribute("onclick", "location.href='/post/" + data.id + "'")
            viewCount.textContent = data.views;
            likeCount.textContent = data.likes;
            dislikeCount.textContent = data.dislikes;
            commentCount.textContent = data.comments.length;
            let authorLinkURL = '/author/' + data.author;
            authorLink.setAttribute('href', authorLinkURL)

            postsBox.appendChild(post);
            post.appendChild(link)
            
            let hoverText = copyLinkBtn.querySelector(".hovertext");

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
        }
    }
}


function getPosts(category = 'all') {
    var url = '/posts/' + category;

    var request = new XMLHttpRequest();

    request.open('GET', url, true);
    request.responseType = 'json';
    request.send()
    
    request.onload = function() {
        var responce = request.response;
        var posts = responce.posts;
        postsBox.innerHTML = '';
        console.log(posts);
        addPosts(posts);
    }
};

getPosts()

// animate and work our "select" by radiobutton


var select = document.getElementById("category-select");
var checkedField = select.querySelector(".checked-field");
var options = select.querySelectorAll(".opt");
var labels = select.querySelectorAll("label");

function pasteCategoriesInSelect(opt, label) {
    checkedField.textContent = label.textContent;
    getPosts(opt.id);
}

options.forEach(function(opt, i) {
    let label = labels[i];
    // if (opt.checked) {
    //     pasteCategoriesInSelect(opt, label);
    // }
    opt.addEventListener("change", function() {
        pasteCategoriesInSelect(opt, label);
    })
})

// Post save btn