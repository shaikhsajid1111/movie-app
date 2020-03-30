$(document).ready(function(){
    $(".btn-search").on("click",function(){
        $('.overlay').css("display","block");
        //$('body').css("display","none");
        //$('.form-container').css("display",'block');
       
        //document.body.style.opacity = "0.1";
    })
    $(".closebtn").click(function(){
        $('.overlay').css("display","none");
    });
})