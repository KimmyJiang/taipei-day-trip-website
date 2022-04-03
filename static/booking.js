
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


// 確認使用者登入狀態
function signin_check(){
    let url = "/api/user";
    fetch(url)
    .then(function(response){
        return response.json();
    }).then(function(res){
        if (res.data){
            document.getElementById("username").textContent = res.data.name;
            booking_content();
        } else{
            window.location.href = "/";
        }
    })
}

// 顯示預定行程
function booking_content(){
    fetch("api/booking")
    .then(function(response){
        return response.json();
    }).then(function(res){
        if (res.data == null){
            no_booking();
        } else {
            let name = res.data.attraction.name;
            let address = res.data.attraction.address;
            let photo = res.data.attraction.image;
            let date = res.data.date;
            let time = res.data.time;
            let price = res.data.price;

            document.getElementById("name").textContent = name;
            document.getElementById("date").textContent = date;
            document.getElementById("price").textContent = `新台幣 ${price} 元`;
            document.getElementById("address").textContent = address;
            
            let image = document.getElementById("image");
            image.src = photo;

            if (time == "morning"){
                document.getElementById("time").textContent = "早上 9 點到中午 12 點";
            } else {
                document.getElementById("time").textContent = "下午 1 點到下午 4 點";
            }   
        }
    })
}


// 刪除行程
function delete_booking(){
    fetch("/api/booking",{
        method : "DELETE",
    }).then(function(response){
        return response.json()
    }).then(function(res){
        if(res.ok){
            window.location.reload();
        }
    })
}


// 無預定行程
function no_booking(){
    let book_info = document.querySelector("#book_info");
    let user_info = document.querySelector("#user_info");
    let card_info = document.querySelector("#card_info");
    let total_info = document.querySelector("#total_info");
    let no_data = document.querySelector("#no_data");
    let footer = document.querySelector("#footer");
    let height = window.innerHeight - 203;
    book_info.style.display = "none";
    user_info.style.display = "none";
    card_info.style.display = "none";
    total_info.style.display = "none";
    no_data.style.display = "block";   
    footer.style.height = `${height}px`;
}


let dialog_login;
let dialog_signup;
let login;
let logout;


// 頁面載入執行動作
window.onload = function(){
    signin_check();
    signin_info(); 
    dialog_login = document.getElementById("dialog_login");
    dialog_signup = document.getElementById("dialog_signup");
    login = document.getElementById("login"); 
    logout = document.getElementById("logout"); 
}