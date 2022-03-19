function show_attraction(){
    let pathname =  window.location.pathname;
    let url = `/api${pathname}`;
    
    fetch(url)
    .then(function(response){
        return response.json();
    })
    .then(function(my_json){
        let name = my_json.data.name;
        let cat = my_json.data.category;
        let mrt = my_json.data.mrt;
        let description = my_json.data.description;
        let address = my_json.data.address;
        let transport = my_json.data.transport;
        photo = my_json.data.images;
        photo_length = photo.length;
        
        document.getElementById("name").textContent = name;
        document.getElementById("cat").textContent = `${cat}  at  ${mrt}`;
        document.getElementById("description").textContent = description;
        document.getElementById("address").textContent = address;
        document.getElementById("transport").textContent = transport;
        photo_btns(photo_length);
        photo_change(0);
    })
}

function photo_change(num){
    let pre_photo = document.querySelector(`#index_${photo_ord}`);
    pre_photo.style.background = "rgba(255, 255, 255, 0.849)";
    photo_ord += num;
    if (photo_ord == photo_length){
        photo_ord = 0;
    } else if (photo_ord == -1){
        photo_ord = photo_length -1;
    }
    document.getElementById("img").innerHTML = `<img src="${photo[photo_ord]}"/>`;
    let click_photo = document.querySelector(`#index_${photo_ord}`);
    click_photo.style.background = "#000000c9";
}

function photo_btns(photo_length){
    let photo_btns = document.querySelector("#photo_btns");
    for (let i=0; i < photo_length ; i++){
        let photo_list = document.createElement("div");
        photo_list.className = "photo_list";
        photo_list.id = `index_${i}`;
        photo_btns.appendChild(photo_list);
    }
}

function price(){
    let msg = document.getElementById("price");
    let period = document.getElementsByName("period");

    if (period[1].checked){
        msg.textContent = "新台幣 2500 元";
    } else {
        msg.textContent = "新台幣 2000 元";
    }
}

window.onload = function(){
    show_attraction();
}

let photo_ord = 0; 
let photo = [];
let photo_length = 0;

