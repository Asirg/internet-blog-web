reactionForm = document.getElementById('form-reaction');
reactionButtons = reactionForm.querySelectorAll('button');
reachionCounters = reactionForm.querySelectorAll('.reactions');

const reactionData = new FormData();
reactionData.append('post', reactionForm.querySelector("input[name='post']").value);
reactionData.append(
    'csrfmiddlewaretoken', 
    reactionForm.querySelector("input[name='csrfmiddlewaretoken']").value
);

send_reaction = async (url, formData) => {
    return await fetch(url, {
        method: 'POST',
        body: formData,
    }).then(response => response.json())
}

reactionButtons[0].addEventListener('click', e => {
    reactionData.append('like', 1);
});

reactionButtons[1].addEventListener('click', e => {
    reactionData.append('like', 0);
});

reactionForm.addEventListener('submit', e => {
    e.preventDefault();

    send_reaction(e.target.action, reactionData)
    .then(result => {
        reachionCounters[0].innerHTML = result['likes'];
        reachionCounters[1].innerHTML = result['dislikes'];
    })
})
// ////////////////////////////////////////////////////////////////
commentForm = document.getElementById('form-comment');
commentInputParent = commentForm.querySelector('#comment-parent');
commentInputContent = commentForm.querySelector('#comment-content');

cancelAnswerButton = commentForm.querySelector('#answer-cancel');

function AnswerComment(id, username){
    commentInputParent.value = id;
    commentInputContent.value = `${username}, `
    
    cancelAnswerButton.classList.remove('disabled');
};
function cancelAnswerComment(){
    commentInputParent.value = '';
    cancelAnswerButton.classList.add('disabled');
};

// update_mod = false;

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

// function cancelUpdateComment(id){
//     update_mod = false;

//     comment_block = document.getElementById(`comment-${id}`);
//     comment_block.querySelector(".text").classList.remove("disabled");
//     comment_block.querySelector(".textarea").classList.add("disabled");

//     comment_block.querySelector(".update").classList.remove("disabled");
//     comment_block.querySelector(".save-update").classList.add("disabled");
//     comment_block.querySelector(".cancel").classList.add("disabled");
// };

// function saveUpdateComment(id){
//     comment_block = document.getElementById(`comment-${id}`);

//     text = comment_block.querySelector("textarea[name='content']").value;
//     span_text = comment_block.querySelector("span.text");


//     if (text != span_text.innerHTML){
//         url = comment_block.querySelector(".form-update").action;
//         csrf_token = comment_block.querySelector("input[name='csrfmiddlewaretoken']").value;

//         formData = new FormData();
//         formData.append('like', text);
//         formData.append('csrfmiddlewaretoken', csrf_token);
//         formData.append('content', text);

//         fetch(
//             url, {
//                 method:"post",
//                 body: formData,
//             }
//         ).then(response => response.json())
//         .then(result => {
//             span_text.innerHTML = text;
//             cancelUpdateComment(id);
//         });
//     }

// };