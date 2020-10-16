
// get and paste posts into div.poste


var postsBox = document.querySelector('div.posts');
var postTemplate = document.querySelector('#post-template').content;
var form = document.querySelector('#post-search');

function addPosts(posts) {
    for (let i = 0; i < posts.length; i++) {
        let data = posts[i];
        let postBox = postTemplate.cloneNode(true);
        let post = postBox.querySelector('.post');
        let title = postBox.querySelector('.title');
        let date = postBox.querySelector('.date');
        let content = postBox.querySelector('.content');
        let author = postBox.querySelector('.author');

        post.setAttribute('post_id', data.id);
        post.setAttribute('category_id', data.category_id);
        title.textContent = data.title;
        date.textContent = data.pub_date;
        content.textContent = data.content;
        author.textContent = '@' + data.author;

        postsBox.insertBefore(post, postsBox.lastChild);
    }
}

function getPosts(category = 'all') {
    var url = 'http://localhost:5000/get_posts/' + category;

    var request = new XMLHttpRequest();

    request.open('GET', url, true);
    request.responseType = 'json';
    request.send()
    
    request.onload = function() {
        var responce = request.response;
        var posts = responce.posts;
        postsBox.innerHTML = '';
        addPosts(posts)
        console.log(posts)
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

