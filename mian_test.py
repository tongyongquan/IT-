# encoding: utf-8
import sys
from flask import session, make_response, Flask

import captcha_cn
import captcha_en
import config

reload(sys)
sys.setdefaultencoding('UTF8')

app = Flask(__name__)
app.config.from_object(config)


@app.route('/code/')
def get_verify_code():
    # 把strs发给前端,或者在后台使用session保存
    # code_img, code_text = utils.generate_verification_code()
    code_img, code_text = captcha_cn.generate_verification_code()
    session['code_text'] = code_text
    print code_text
    response = make_response(code_img)
    response.headers['Content-Type'] = 'image/jpeg'
    response.headers['Pragma'] = 'No-cache'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Cache-Expires'] = -10
    return response


if __name__ == '__main__':
    app.run(host="localhost", port=4000, debug=True)
