// 首頁景點資訊
function show_index(page,keyword){
    let url  = `/api/attractions?page=${page}&keyword=${keyword}`;

    fetch(url)
    .then(function(response){
        return response.json();
    })
    .then(function(res){
        nextpage = res.nextPage;
        data = res.data;
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


// 新增景點資訊 box
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


// 點擊 box 連結至景點詳細資訊
function link_page(id){
    window.location.href = `attraction/${id}`;
}

// 關鍵字查詢功能
function query_keyword(){
    let keyword = document.getElementById("keyword").value;
    gallery.innerHTML = '';
    show_index(0,keyword);
}


// 顯示登入視窗
function show_dialog_login(){  
    dialog_login.style.display = "block";
}


// 顯示註冊視窗
function show_dialog_signup(){
    dialog_signup.style.display = "block";
}


// 關閉登入視窗
function close_dialog_login(){
    dialog_login.style.display = "none";
}


// 關閉註冊視窗
function close_dialog_signup(){
    dialog_signup.style.display = "none";
}


// 使用者登入狀態流程
function signin_info(){
    let url = "/api/user";
    fetch(url)
    .then(function(response){
        return response.json();
    }).then(function(res){
        if (res.data){
            login.style.display = "none";
            logout.style.display = "block";
        } else{
            logout.style.display = "none";
            login.style.display = "block";
        }
    })
}


// 註冊帳號流程
function sign_up(){
    let url = "/api/user"
    let user = document.getElementById("user").value;
    let new_email = document.getElementById("new_email").value;
    let new_pswd = document.getElementById("new_pswd").value;
    let signup_msg = document.getElementById("signup_msg");
    let data = {
        "name":user,
        "email":new_email,
        "password":new_pswd
    };

    fetch(url,{
        method : "POST",
        headers : new Headers ({
            "Content-Type" : "application/json"
        }),
        body : JSON.stringify(data)
    }).then(function(response){
        return response.json();
    }).then(function(res){
        if(res.ok){
            signup_msg.textContent = "註冊成功"; 
            signup_msg.style.textAlign = "center"; 
            signup_msg.style.color = "red";

        } else {
            signup_msg.textContent = res.message;
            signup_msg.style.textAlign = "center"; 
            signup_msg.style.color = "red";
        }
    })
}


// 登入帳號流程
function sign_in(){
    let email = document.getElementById("email").value;
    let pswd = document.getElementById("pswd").value;
    let login_msg = document.getElementById("login_msg");
    let url = "/api/user";
    let data = { 
        "email" : email,
        "password":pswd 
    };

    fetch(url,{
        method : "PATCH",
        headers : new Headers ({
            "Content-Type": "application/json"
        }),
        body : JSON.stringify(data)
    }).then(function(response){
        return response.json();
    }).then(function(res){
        if(res.ok){
            window.location.reload();
        } else {
            login_msg.textContent = res.message;
            login_msg.style.textAlign = "center"; 
            login_msg.style.color = "red";
        }
    })
}


// 登出流程
function sign_out(){
    let url = "/api/user";
    fetch(url,{
        method : "DELETE",
    }).then(function(response){
        return response.json()
    }).then(function(res){
        if(res.ok){
            window.location.reload();
        }
    })
}

// 預定行程 button
function show_booking(){
    let url = "/api/user";
    fetch(url)
    .then(function(response){
        return response.json();
    }).then(function(res){
        if (res.data){
            window.location.href = "/booking";
        } else{
            show_dialog_login();
        }
    })
}


let keywordInput = document.querySelector("#keyword");
let loadMore = false;
let dialog_login;
let dialog_signup;
let login;
let logout;


// 頁面載入執行動作
window.onload = function(){
    show_index(0,"");
    signin_info(); 
    dialog_login = document.getElementById("dialog_login");
    dialog_signup = document.getElementById("dialog_signup");
    login = document.getElementById("login"); 
    logout = document.getElementById("logout");   
}
