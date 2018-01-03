/**
 * Created by hdy on 2018/1/2.
 */

// 修改验证码的图片的地址 src
function get_img_code(url) {
    $('#verifyImg').attr("src", url + '?' + Math.random() )
}