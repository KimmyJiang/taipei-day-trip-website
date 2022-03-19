function show_index(page,keyword){
    let url  = `/api/attractions?page=${page}&keyword=${keyword}`;

    fetch(url)
    .then(function(response){
        return response.json();
    })
    .then(function(my_json){
        nextpage = my_json.nextPage;
        data = my_json.data;
        data_len = data.length;
        show_data();
        return nextpage;
    })
    .then(function(nextpage){
        let timer = null;
        window.onscroll = function(){
            let footer = document.getElementById("footer");
            clearTimeout(timer);
            if (window.scrollY + window.innerHeight > footer.offsetTop && nextpage ) {
                timer = setTimeout(function(){
                    show_index(nextpage,keyword);}
                ,200);
            }
        }
    })
}

function show_data(){
    let gallery = document.getElementById("gallery");
    if (!data_len) {
        gallery.innerHTML = "<h3>查無景點相關資訊<h3>";
    }else{
        for (let i = 0 ; i < data_len ; i++){
            let id = data[i].id;
            let img = data[i].images[0];
            let name = data[i].name;
            let mrt = data[i].mrt;
            let category = data[i].category;

            gallery.innerHTML += `
            <div class="box" onclick="link_page(${id})">
                <img class="image" src="${img}"/>
                <div class="name">${name}</div>
                <div class="mrt">${mrt}</div>
                <div class="category">${category}</div>
            </div>
            `;
        }
    }
}

function link_page(id){
    window.location.href = `attraction/${id}`;
}

function query_keyword(){
    let keyword = document.getElementById("keyword").value;
    gallery.innerHTML = '';
    show_index(0,keyword);
}


let keywordInput = document.querySelector("#keyword");
let loadMore = false;

window.onload = function(){
    show_index(0,"");
}
