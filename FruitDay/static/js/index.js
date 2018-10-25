/**
 * Created by tarena on 18-10-23.
 */
function check_login() {
    $.get('/checkLogin/',function (data) {

                 if(data.status=='1'){
                    var user = JSON.parse(data.user);
                     var name = user.uname;
                     var html = "欢迎："+name+"&nbsp&nbsp <a href='/logout/'>[退出]</a>"
                     $('#list>li:first').html(html);
                 }

             },'json')
}

function load_goods(){

    $.get('/loadgoods/',function (data) {
        var html = "";
        $(data).each(function (i,obj) {
            var jsonType = JSON.parse(obj.type);

            html += "<div class='item'>";
                html += "<p class='title'>";
                    html += "<a href='#'>更多</a>";
                    html += "<img src='/"+jsonType.picture+"'>";
                html += "</p>";
                html += "<ul>";
                    var jsonGoods = JSON.parse(obj.goods);

                    $(jsonGoods).each(
                        function (i,obj) {

                            html += "<li";
                                if((i+1)%5==0)
                                    html += "class='no-margin'";
                            html += ">";
                                html += "<p>";
                                    html += "<img src=/"+ obj.fields.picture + ">";
                                html += "</p>";
                                html += "<div class='content'>";
                                    html += "<a href='javascript:add_cart("+obj.pk+")' class='cart'>";
                                        html += "<img src='/static/images/cart.png'>";
                                    html += "</a>";
                                    html += "<p>"+obj.fields.title+"</p>";
                                    html += "<span>&yen"+obj.fields.price+"/"+obj.fields.spec+"</span>";
                                html += "</div>";
                            html += "</li>"
                        }
                    );
                html += "</ul>";
            html += "</div>";

            $('#main').html(html);
        })
    },'json')
}

//参数：goods_id表示的是要加入到购物车的商品id
function add_cart(goods_id) {
    $.get('/checkLogin/',function (data) {
        if(data.status==0){
            alert('请登录...');
        }else{
            $.get('/addcart/','goods_id='+goods_id,function (data) {
                if(data.status == 1){
                    alert('添加购物车成功！');
                      //更新购物车数量
                $.get('/cartcount/',function (data) {
                    $('#cart').html('我的购物车('+data+')');
        })
                }else{
                    alert('添加购物车失败');
                }
            },'json')

        }
    },'json')
}

function cartCount() {
    $.get('/checkLogin/',function (data) {

        if(data.status == '1'){
            $.get('/cartcount/',function (data) {
                $('#cart').html('我的购物车('+data+')');
        })
        }
},'json')
}

$(function () {
     check_login();
     load_goods();
     cartCount();

         })