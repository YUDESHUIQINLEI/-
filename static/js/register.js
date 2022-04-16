function bindCaptchaBtnClick(){
    $("#captcha-btn").on("click", function(event){
         var $this = $(this);
         var email = $("input[name='email']").val();
         if(! email){
             alert("请先输入邮箱！");
             return;
         }
         // 通过js发送网络请求 ajax
         $.ajax({
             url : "/user/captcha",
             method : "POST",
             data : {
                 "email" : email
             },
             success : function (res){
                if(res['code'] == 200){
                    // 将点击设置为失效
                    $this.off("click");
                    var count = 60;
                    var timer = setInterval(function (){
                        if(count > 0){
                            $this.text(count+"秒后重新发送");
                        }else{
                            $this.text("获取验证码");
                            bindCaptchaBtnClick();
                            // 停掉倒计时，否则会一直执行
                            clearInterval(timer);
                        }
                        count -= 1;
                    }, 1000);
                    alert("验证码发送成功");
                }else{
                    alert(res['message']);
                }
             }
         })
    })
}

$(function(){
    bindCaptchaBtnClick()
});