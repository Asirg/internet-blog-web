active_item = document.querySelector(".item.active");
sub_categories = document.getElementById("sub-category").children;

function func(e){
    active_item.classList.remove("active")
    e.target.classList.add("active");

    active_item = e.target;

    for (let i = 0; i < sub_categories.length; i++) {
        sub_categories[i].href = "123";
    }
}