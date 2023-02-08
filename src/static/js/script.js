pathname = window.location.pathname;
url = new URL(window.location.href)

// switch(pathname){
//     case ('/search/'):
//         searh_page();
//     break;
// }


active_item = document.querySelector('#header-category-menu .item.active');
active_sub_category_menu = document.querySelector('#header-category-menu .sub-category.active');
sub_category_menus = document.querySelectorAll('#header-category-menu .sub-category');

function header_category_select(e, index){
    active_item.classList.remove('active');
    active_sub_category_menu.classList.remove('active');

    e.target.classList.add('active');
    sub_category_menus[index].classList.add('active');

    active_item = e.target;
    active_sub_category_menu = sub_category_menus[index];
}