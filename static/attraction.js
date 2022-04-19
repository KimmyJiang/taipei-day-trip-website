// 展示個別景點頁面資訊
function show_attraction(id){
    let url = `/api/attraction/${id}`;
    
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


// 圖片輪播
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


// 圖片輪播鈕
function photo_btns(photo_length){
    let photo_btns = document.querySelector("#photo_btns");
    for (let i=0; i < photo_length ; i++){
        let photo_list = document.createElement("div");
        photo_list.className = "photo_list";
        photo_list.id = `index_${i}`;
        photo_btns.appendChild(photo_list);
    }
}


// 訂購時段價格
function price(){
    let msg = document.getElementById("price");
    let period = document.getElementsByName("period");

    if (period[1].checked){
        msg.textContent = "新台幣 2500 元";
    } else {
        msg.textContent = "新台幣 2000 元";
    }
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


// 台北一日遊
function back_to_home(){
    window.location.href = '/';
}


// 預定行程 button
function show_booking(){
    fetch("/api/user")
    .then(function(response){
        return response.json();
    }).then(function(res){
        if (res.data){
            window.location.href = "/booking";
        } else{
            show_dialog_login()
        }
    })
}


// 開始預定行程 button
function booking(){
    let date = document.getElementById("date").value;
    let select_date = new Date(date);
    let time;
    let price;
    let period = document.getElementsByName("period");

    if (date == ""){
        return alert("請選擇日期");
    }

    if (Date.now() > select_date){
        return alert("日期選擇錯誤，請再次確認日期");
    }

    if (period[0].checked){
        time = "morning";
        price = 2000;
    } else if (period[1].checked) {
        time = "afternoon";
        price = 2500;
    } else {
        return alert("請選擇時間");
    }
    
    let data = {
        "attractionId" : id,
        "date" : date,
        "time" : time,
        "price": price
    }

    fetch("/api/booking",{
        method : "POST",
        headers : new Headers ({
        "Content-Type" : "application/json"
    }),
        body : JSON.stringify(data)
    }).then(function(response){
        return response.json();
    }).then(function(res){
        if (res.error){
            if (res.message == "尚未登入系統"){
                show_dialog_login();
            }
        } else{
            window.location.href = "/booking";  
        }
    })
}

let photo_ord = 0; 
let photo = [];
let photo_length = 0;
let dialog_login;
let dialog_signup;
let login;
let logout;
let id = window.location.href.split('/').pop();


// 頁面載入執行動作
window.onload = function(){
    show_attraction(id);
    signin_info(); 
    dialog_login = document.getElementById("dialog_login");
    dialog_signup = document.getElementById("dialog_signup");
    login = document.getElementById("login"); 
    logout = document.getElementById("logout"); 
}
