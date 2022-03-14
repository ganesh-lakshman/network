
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit').forEach(post => {
        post.style.display = 'none';
    })
    document.querySelectorAll('.showposts').forEach(showpost => {
        
        showpost.childNodes[11].addEventListener('click', () => {
            console.log("cameeee");
            console.log(showpost.childNodes[11].value);
            fetch(`like/${showpost.childNodes[11].value}`, {
                method: 'PUT',
                body: JSON.stringify({
                    likedby: document.querySelector('#username').value
                })
                })
                .then(() => {
                    location.reload();
                })
        })
    
    })
    
    document.querySelectorAll('.container').forEach(container => {
        post = container.childNodes[1];
        button = post.childNodes[11];
        text = container.childNodes[3];
        editor = document.querySelector('#username').value;
        
        button.addEventListener('click', () => {
            console.log("camehere")
            container.childNodes[1].style.display = 'none';
            container.childNodes[3].style.display = 'block';
            post = container.childNodes[1];
            let text = post.childNodes[4];
            text = text.textContent;
            console.log(text.textContent);
            edit = container.childNodes[3];
            textarea = edit.childNodes[1];
            textarea.value = text.substring(5);
            editbutton = edit.childNodes[3];
            console.log(editbutton.value);
            
            editbutton.addEventListener('click', () => {
                edit = container.childNodes[3];
                textarea = edit.childNodes[1];
                editedpost = textarea.value;
                console.log(editedpost);
                fetch(`/posts/${editbutton.value}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        post: editedpost,
                        editor: document.querySelector('#username').value
                        })
                    })
                    .then(() => {
                        location.reload();
                        container.childNodes[1].style.display = 'block';
                        container.childNodes[3].style.display = 'none';
                    })
            })
            


    })
    })
})


