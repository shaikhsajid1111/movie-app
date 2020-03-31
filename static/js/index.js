$(document).ready(function(){
    $(".btn-search").on("click",function(){
        $('.overlay').css("display","block");
    })
    $(".closebtn").click(function(){
        $('.overlay').css("display","none");
    });
})