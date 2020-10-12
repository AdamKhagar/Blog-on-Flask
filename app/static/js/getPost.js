var postsBox = document.querySelector('div.posts');
var postTemplate = document.querySelector('#post-template').content;
var form = document.querySelector('#post-search');
var select = form.querySelector('#category');
// var searchField = document.querySelector("#search")

function addPosts(posts) {
    for (let i = 0; i < posts.length; i++) {
        let data = posts[i];
        let postBox = postTemplate.cloneNode(true);
        let post = postBox.querySelector('.post');
        let title = postBox.querySelector('.title');
        // let category = post.querySelector('.category');
        let date = postBox.querySelector('.date');
        let content = postBox.querySelector('.content');

        post.setAttribute('post_id', data.id);
        post.setAttribute('category_id', data.category_id);
        title.textContent = data.title;
        date.textContent = data.pub_date;
        content.textContent = data.content;

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
        // console.log(posts);
        addPosts(posts)
    }

    // var responce = request.responseType;
    // if (request.status != 200) {
    //     alert( request.status + ': ' + request.statusText ); 
    // } else {
        
    // }


};

getPosts()

select.addEventListener("change", function() {
    postsBox.innerHTML = ''
    getPosts(select.value);
});
