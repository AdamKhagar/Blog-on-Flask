
// get and paste posts into div.poste


var postsBox = document.querySelector('div.posts');
var templates = document.querySelector('template').content;
var form = document.querySelector('#post-search');

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

            post.setAttribute('post_id', data.id);
            post.setAttribute('category_id', data.category_id);
            title.textContent = data.title;
            date.textContent = data.pub_date;
            content.innerHTML = data.content;
            author.textContent = '@' + data.author;

            let authorLinkURL = '/author_page/' + data.author;
            authorLink.setAttribute('href', authorLinkURL)

            postsBox.insertBefore(post, postsBox.lastChild);
        }
    }
}

function getPosts(category = 'all') {
    var url = 'http://localhost:5000/get-posts/' + category;

    var request = new XMLHttpRequest();

    request.open('GET', url, true);
    request.responseType = 'json';
    request.send()
    
    request.onload = function() {
        var responce = request.response;
        var posts = responce.posts;
        postsBox.innerHTML = '';
        addPosts(posts)
        
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

