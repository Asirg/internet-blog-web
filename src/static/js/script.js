active_item = document.querySelector(".item.active");
active_sub_category_menu = document.querySelector(".sub-category.active");
sub_category_menus = document.querySelectorAll(".sub-category");

function func(e, index){
    active_item.classList.remove("active");
    active_sub_category_menu.classList.remove("active");

    e.target.classList.add("active");
    sub_category_menus[index].classList.add("active");

    active_item = e.target;
    active_sub_category_menu = sub_category_menus[index];
}