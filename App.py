from flask import Flask, request, jsonify
import API_Crawling as Ap

app = Flask(__name__)

@app.route("/")
def hello() :
    return "Hello,Flask"

@app.route('/keyboard')
def Keyboard():
    dataSend = {
    }
    return jsonify(dataSend)

@app.route('/message', methods=['POST'])
def Message():
    Value = " 주식 정보 공개를 위한 오픈 API Bot 입니다. \n 명령어는 아래와 같습니다. \n 1. 목록(종목코드 조회 - /종목 '검색하고자 하는 이름' ex) /종목 삼성)  \n 2. 조회(/코드 '검색하고자 하는 종목 코드' ex) /코드 291230) "
    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText":
                        {
                        "text" : Value
                        }
                }
            ]
        }
    }
    return jsonify(dataSend)
# https://i.kakao.com/docs/skill-response-format#%EC%83%81%EC%84%B8-%ED%95%84%EB%93%9C-9

@app.route('/code', methods=['POST'])
def Search_Code () :
    content = request.get_json()
    content = content['action']['params']['sys_text']
    print(content)
    print(1)
    content = content.replace("/종목", "")
    content = content.replace("종목", "")
    content = content.strip()
    print('Search_Code 수행')
    print(content)
    Value = Ap.search_code(content)

   # print(result)
    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText":
                        {
                        "text" : Value
                        }
                }
            ]
        }
    }

    return jsonify(dataSend)

@app.route('/page_sise', methods=['POST'])
def Search_Page_sise () :
    content = request.get_json()
    content = content['action']['params']['sys_text']
    print('Search_Page_sise 수행')
    print(content)
    content = content.replace("/기간조회", "")
    content = content.replace("기간조회", "")
    content = content.strip()
    Value = Ap.get_sise(content)

   # print(result)
    dataSend = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText":
                        {
                        "text" : Value[0]
                        }
                },
                {
                      "simpleText":
                        {
                        "text" : Value[1]
                        }
                }
            ]
        }
    }

    return jsonify(dataSend)

@app.route('/sise', methods=['POST'])
def Get_sise () :
    try:
        content = request.get_json()
        content = content['action']['params']['sys_text']
        print('Get_sise 수행')
        print(content)
        content = content.replace("/코드", "")
        content = content.strip()
        Value = Ap.get_Jongmok(content)
        Message_send = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText":
                        {
                        "text" : Value
                        }
                }
            ]
        }
    }
        return jsonify(Message_send)
    except:
        Value = " 정상적인 값이 아닙니다. "
        Message_send = {
            "version": "2.0",
            "template": {
                "outputs": [
                {
                      "simpleText":
                        {
                        "text" : Value
                        }
                }
            ]         
            }
           }
        
        return jsonify(Message_send)

if __name__ == "__main__":
    app.run(host='0.0.0.0')