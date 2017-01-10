#!/usr/bin/env php

<!DOCTYPE html>
<html>

<head>
    <title>Waydrow</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script type="application/x-javascript">
    addEventListener("load", function() {
        setTimeout(hideURLbar, 0);
    }, false);

    function hideURLbar() {
        window.scrollTo(0, 1);
    }
    </script>
    <link rel="stylesheet" href="../public/css/style.css">
    <script src="../public/js/jquery-1.11.3.min.js"></script>
</head>

<body>
    <script>
    $(document).ready(function(c) {
//         $('.close').on('click', function(c){
//         	$('.login-form').fadeOut('slow', function(c){
//           		$('.login-form').remove();
//         	});
//         });
    });
    </script>
    <!--SIGN UP-->
    <h1>计算机网络课程实验</h1>
    <div class="login-form">
         <!--<div class="close"> </div>-->
        <div class="head-info">
            <label class="lbl-1"> </label>
            <label class="lbl-2"> </label>
            <label class="lbl-3"> </label>
        </div>
        <div class="clear"> </div>
        <div class="avtar">
            <img src="../public/images/avatar.png" />
        </div>
        <div class="info">

            <?php
            $param = $argv[1];
            $param = explode('&', $param);

            $username = $param[0];
            $username = explode('=', $username)[1];

            $num = $param[1];
            $num = explode('=', $num)[1];

            echo "<p>欢迎你 " . $username . "</p>";
            echo "<p>用户名: " . $username . "</p>";
            echo "<p>学号: " . $num . "</p>";

            //echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />';
            //echo "<script>alert('登录成功');</script>";
            //echo "</pre></body></html>";
            ?>
        </div>
    </div>
    <div class="copy-rights">
        <p>Copyright &copy; 2017.Waydrow All rights reserved. - By <a href="http://blog.waydrow.com" title="Waydrow" target="_blank">Waydrow</a></p>
    </div>
</body>

</html>



