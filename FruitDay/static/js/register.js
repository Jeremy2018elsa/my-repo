/**
 * Created by tarena on 18-10-22.
 */
function checkPhone() {

                var phoneVal = $('[name=uphone]').val();
                var show = '';
                var pattern = /^1[345789]\d{9}$/;

                if(phoneVal==''){
                    show = '手机号码不能为空';
                     $('#showphone').html(show);
                    return false;
                }else{
                    if(!(pattern.test(phoneVal))){
                        show = '手机号码格式不正确';
                        $('#showphone').html(show);
                    }else{
                        $.get('/checkphone/','phone='+phoneVal,function (data) {
                            //alert(data);
                            show = data;
                            $('#showphone').html(show);

                        })
                    }
                    return true;
                }

            }


        function checkPassword() {

                var upwd = $('[name=upwd]').val();
                if(upwd.length<6){
                    $('#showupwd').html('密码必须６位以上');
                    return false;
                }else{
                    $('#showupwd').html('');
                    return true;
                }
            }


        function checkCpassword() {


                if($('#cpwd').val()!=$('[name=upwd]').val()){
                    $('#showcpwd').html('确认密码与密码必须保持一致');
                    return false;
                }else{
                   $('#showcpwd').html('');
                }
            }


        function checkUname() {

                if($('[name=uname]').val()==''){
                    $('#showuname').html('用户名不能为空');
                    return false;
                }else{
                   $('#showuname').html('');
                }
            }


        function checkUemail() {

                var email = $('[name=uemail]').val();
                if(email==''){
                    $('#showuemail').html('邮箱不能为空');
                    return false;
                }else{
                    var pattern = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
                    if(!pattern.test(email)){
                        $('#showuemail').html('邮箱格式不正确');
                    }
                    return true;
                }
            }



        $(function () {
            $('[name=uphone]').blur(function () {

            checkPhone();
            });
            $('[name=upwd]').blur(function () {
            checkPassword();
            });
            $('#cpwd').blur(function () {
            checkCpassword();
            });
            $('[name=uname]').blur(function () {
            checkUname();
            });
            $('[name=uemail]').blur(function () {
            checkUemail();
            });

            $('#formRegister').submit(function () {
                return checkPhone()&&checkPassword();
            });
        });
