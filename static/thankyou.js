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
            let order_number = window.location.href.split('=').pop();
            order_status(order_number);
        } else{
            window.location = "/";
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


function order_status(order_number){
    fetch(`api/order/${order_number}`
    ).then(function(response){
        return response.json();
    }).then(function(res){
        let number = document.querySelector("#number");
        let message = document.querySelector("#message");

        if (res.data == null){
            number.textContent= `訂單編號：${order_number}`;
            message.textContent = "查無此筆訂單編號資料，請再次確認編號"
        } else {
            number.textContent= `訂單編號：${order_number}`;
            if (res.data.status == 0){
                message.textContent = "付款成功，祝旅途愉快！"  
            } else {
                message.textContent = "付款失敗，請重新下訂"  
            }
          
        }
    })

}




window.onload = function(){
    signin_info();
} 