// ////////////////////////////////////////////////////////////////
///////// Реакции
const reactionForm = document.getElementById('form-reaction');
const reactionButtons = reactionForm.querySelectorAll('button');
const reachionCounters = reactionForm.querySelectorAll('.reactions');

let reactionData = new FormData();
reactionData.append('post', reactionForm.querySelector("input[name='post']").value);
reactionData.append(
    'csrfmiddlewaretoken', 
    reactionForm.querySelector("input[name='csrfmiddlewaretoken']").value
);

send_fetch = async (url, formData) => {
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

    send_fetch(e.target.action, reactionData)
    .then(result => {
        reachionCounters[0].innerHTML = result['likes'];
        reachionCounters[1].innerHTML = result['dislikes'];
    })
})
// ////////////////////////////////////////////////////////////////
///////// Ответ на комментарий
const commentForm = document.getElementById('form-comment');
const commentInputParent = commentForm.querySelector('#comment-parent');
const commentInputContent = commentForm.querySelector('#comment-content');

function AnswerComment(id, parent, username){
    commentInputParent.value = parent ? parent : id;
    commentInputContent.value = `${username}, `
    
    cancelAnswerButton.classList.remove('disabled');
};

cancelAnswerButton = commentForm.querySelector('#answer-cancel');
function cancelAnswerComment(){
    commentInputParent.value = '';
    cancelAnswerButton.classList.add('disabled');
};

///////// Редактирование комментария

let updateMod = false;
let updateCommentBlock = false;

function changeUpdateMod(){
    updateCommentBlock.querySelectorAll('button').forEach(element => {
        if (['update', 'answer', 'delete'].includes(element.name) && !updateMod)
            element.classList.remove('disabled');
        else if (['save-update', 'cancel'].includes(element.name) && updateMod)
            element.classList.remove('disabled');
        else
            element.classList.add('disabled');
    });
}

function updateComment(id){
    if (!updateMod){
        updateMod = true;

        updateCommentBlock = document.getElementById(`comment-${id}`)

        updateCommentBlock.querySelector(".text").classList.add("disabled");

        updateCommentBlock.querySelector("textarea").classList.remove("disabled");
        updateCommentBlock.querySelector("textarea").value = updateCommentBlock.querySelector(".text").innerHTML;

        changeUpdateMod()
    }
};

function cancelUpdateComment(){
    updateMod = false;

    updateCommentBlock.querySelector(".text").classList.remove("disabled");
    updateCommentBlock.querySelector("textarea").classList.add("disabled");

    changeUpdateMod()
};

function saveUpdateComment(){
    newText = updateCommentBlock.querySelector("textarea").value;
    originalText = updateCommentBlock.querySelector(".text");

    if (newText != originalText.innerHTML){
        url = updateCommentBlock.querySelector(".form-update").action;
        csrf_token = updateCommentBlock.querySelector("input[name='csrfmiddlewaretoken']").value;

        formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrf_token);
        formData.append('content', newText);

        send_fetch(url, formData)
        .then(result => {
            originalText.innerHTML = newText;
            cancelUpdateComment();
        });
    }
};