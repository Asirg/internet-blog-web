form = document.getElementById('form-reaction');
form_input = document.getElementById('reaction-value');
form_buttons = form.querySelectorAll('button');

form_buttons[0].addEventListener('click', e => {
    form_input.value = 1;
});

form_buttons[1].addEventListener('click', e => {
    form_input.value = 0;
});
form.addEventListener('submit', e => {
    e.preventDefault();
    if (!form.classList.contains('dis')){
        url = e.target.action

        csrf_token = form.querySelector("input[name='csrfmiddlewaretoken']").value;
        
        const formData = new FormData();134
        formData.append('like', form_input.value);
        formData.append('csrfmiddlewaretoken', csrf_token);

        fetch(url, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(result => {
            form_buttons[0].lastChild.textContent = result['likes'];
            form_buttons[1].lastChild.textContent = result['dislikes'];
        });
    }
})
// ////////////////////////////////////////////////////////////////
form_comment = document.getElementById('form-comment');
input_parent = document.getElementById('comment-parent');
input_content = document.getElementById('comment-content');

cancelParentButton = document.getElementById('parent-cancel');

function setCommentParent(id, username){
    input_parent.value = id;
    input_content.value = `${username}, `
    cancelParentButton.classList.remove('disabled');
};
function cancelCommentParent(){
    input_parent.value = '';
    cancelParentButton.classList.add('disabled');
};

update_mod = false;

function updateComment(id){
    if (!update_mod){
        update_mod = true;

        comment_block = document.getElementById(`comment-${id}`)
        comment_block.querySelector(".text").classList.add("disabled");
        comment_block.querySelector(".textarea").classList.remove("disabled");

        comment_block.querySelector(".textarea").value = comment_block.querySelector(".text").innerHTML;

        comment_block.querySelector(".update").classList.add("disabled");
        comment_block.querySelector(".save-update").classList.remove("disabled");
        comment_block.querySelector(".cancel").classList.remove("disabled");
    }
};

function cancelUpdateComment(id){
    update_mod = false;

    comment_block = document.getElementById(`comment-${id}`);
    comment_block.querySelector(".text").classList.remove("disabled");
    comment_block.querySelector(".textarea").classList.add("disabled");

    comment_block.querySelector(".update").classList.remove("disabled");
    comment_block.querySelector(".save-update").classList.add("disabled");
    comment_block.querySelector(".cancel").classList.add("disabled");
};

function saveUpdateComment(id){
    comment_block = document.getElementById(`comment-${id}`);

    text = comment_block.querySelector("textarea[name='content']").value;
    span_text = comment_block.querySelector("span.text");


    if (text != span_text.innerHTML){
        url = comment_block.querySelector(".form-update").action;
        csrf_token = comment_block.querySelector("input[name='csrfmiddlewaretoken']").value;

        formData = new FormData();
        formData.append('like', text);
        formData.append('csrfmiddlewaretoken', csrf_token);
        formData.append('content', text);

        fetch(
            url, {
                method:"post",
                body: formData,
            }
        ).then(response => response.json())
        .then(result => {
            span_text.innerHTML = text;
            cancelUpdateComment(id);
        });
    }

};