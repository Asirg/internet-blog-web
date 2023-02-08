pathname = window.location.pathname;
url = new URL(window.location.href)

const sort = url.searchParams.get('sort');
if (sort)
    document.querySelector(`select[name='sort'] option[value='${sort}']`).selected = true;

add_tag_menu = document.getElementById("tags-search-menu");
added_tags_list = document.getElementById("added-tags-list");
search_menu = document.querySelector('#search-category-menu');
search_main_category_items = search_menu.querySelectorAll('.main-category .item');
search_active_sub_category_menu = search_menu.querySelector('#search-category-menu .sub-category.active');
search_sub_category_menus = search_menu.querySelectorAll('#search-category-menu .sub-category');

select_add_tag = false;
{
    document.getElementById("tags-search-menu").addEventListener('mouseover', e=> {
        select_add_tag = true;
    });
    
    document.getElementById("tags-search-menu").addEventListener('mouseleave', e=> {
        select_add_tag = false;
    });
    
    document.getElementById("add-tags-input").addEventListener('focusout', e=> {
        e.preventDefault();
        if (!select_add_tag){
            add_tag_menu.classList.remove('active');
        }
    });
}


document.getElementById("add-tags-input").addEventListener('focus', e=> {
    e.preventDefault();
    add_tag_menu.classList.add('active');
});

for ( let i = 0; i < search_sub_category_menus.length; i++){
    all_item_active = true;
    for (sub_cat of search_sub_category_menus[i].querySelectorAll(".item")){
        if (!sub_cat.classList.contains('active'))
            all_item_active = false;
    }
    if (all_item_active && search_sub_category_menus[i].querySelectorAll(".item").length > 0 )
        search_main_category_items[i].classList.add('active');
}

document.getElementById("add-tags-input").addEventListener('input', e => {
    e.preventDefault();
    const url = `/tags/?q=${e.target.value}`;
    fetch(url, {
            method:'get',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
        }
    })
    .then(resonse=>resonse.json())
    .then(result => {
        add_tag_menu.innerHTML = '';
        list_result = Object.entries(result);

        if (list_result.length){
            add_tag_menu.classList.add('active');

            for (const [key, value] of list_result){
                if (!added_tags_list.querySelector(`input[value="${value['name']}"]`)){

                    let tag = document.createElement("div");
                    tag.innerHTML = value['name'];
                    tag.addEventListener('click', event => {
                        document.getElementById("add-tags-input").value = "";
                        
                        add_tag_menu.innerHTML = "";
                        add_tag_menu.classList.remove('active');

                        let adtag = document.createElement("div");
                        adtag.classList.add("tag-block");
                        adtag.innerHTML = value['name'];
                        added_tags_list.appendChild(adtag);

                        let adtag_input = document.createElement("input");
                        adtag_input.type = "hidden";
                        adtag_input.name = "tag";
                        adtag_input.value = value['name'];
                        adtag.appendChild(adtag_input);

                        adtag.addEventListener('click', event => {

                            event.target.remove();
                        });
                    })
                    add_tag_menu.appendChild(tag);
                }
            }
        }else{
            add_tag_menu.classList.remove('active');
        }
    });
})

function check_category(e, index){
    if (e.target.classList.contains('active')){
        e.target.classList.remove('active');

        search_sub_category_menus[index].querySelectorAll('.item').forEach(element => {
            element.classList.remove('active');
            document.getElementById(element.htmlFor).checked = false;
        });
    }else{
        e.target.classList.add('active');

        search_sub_category_menus[index].querySelectorAll('.item').forEach(element => {
            element.classList.add('active');
            document.getElementById(element.htmlFor).checked = true;
        });
    }

}

function check_subcategory(e, category){
    if (e.target.classList.contains('active')){
        e.target.classList.remove('active');
        search_menu.querySelector(`label[for=${category}]`).classList.remove('active')
        search_menu.querySelector(`input[id=${category}]`).checked = false;
    }else{
        e.target.classList.add('active');

        ls_el = e.target.parentElement.querySelectorAll('label');
        all_active = true;
        for (let i = 0; i < ls_el.length; i ++ ){
            if (!ls_el[i].classList.contains('active'))
                all_active = false;
        }
        
        if (all_active)
            search_menu.querySelector(`label[for=${category}]`).classList.add('active')
    }
}

function search_category_select(e, index){
    search_active_sub_category_menu.classList.remove('active');
    search_sub_category_menus[index].classList.add('active');
    search_active_sub_category_menu = search_sub_category_menus[index];
}