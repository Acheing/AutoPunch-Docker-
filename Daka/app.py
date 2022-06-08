import re
import requests
from bs4 import BeautifulSoup
import api
import json

sess = requests.session()
sess_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
}


def download_img(imgurl):
    rsp = sess.get(imgurl)
    if rsp.status_code == 200:
        content = rsp.content
        with open("./Captcha.png", "wb+") as f:
            f.write(content)
        return str(content)


def GetExecution(be):
    return be.find(name="input", attrs={"name": "execution"})["value"]

def GETCaptcha(be):
    pattern = re.compile(r"id: '\d+'$",re.MULTILINE)
    ID0 = be.find_all("script",text=pattern)
    ID1 = pattern.findall(str(ID0[0]))[0]
    ID2 = re.findall(r"\d+",ID1)[0]
    CaptchaURL = "http://ua.scu.edu.cn/captcha?captchaId="+ID2
    download_img(CaptchaURL)
    Captcha = api.Get("./Captcha.png")
    return Captcha

def Visit():
    LoginUrl = "http://ua.scu.edu.cn/login?service=https%3A%2F%2Fwfw.scu.edu.cn%2Fa_scu%2Fapi%2Fsso%2Fcas-index%3Fredirect%3Dhttps%253A%252F%252Fwfw.scu.edu.cn%252Fncov%252Fwap%252Fdefault%252Fsave"
    res = sess.get(LoginUrl, headers=sess_header)
    return BeautifulSoup(res.text, 'html.parser')

def SetPost(Username,Password,Execution,Captcha):
    POSTDATA = {
        'username': Username,
        'password': Password,
        'captcha': Captcha,
        'submit': '%E7%99%BB%E5%BD%95',
        'type': 'username_password',
        'execution': Execution,
        '_eventId': 'submit'
    }
    return POSTDATA

def Rush(data):
    URL = "https://ua.scu.edu.cn/login"
    res = sess.post(URL,headers=sess_header,data=data)
    return res.status_code

def Daka(data):
    url = "https://wfw.scu.edu.cn/ncov/wap/default/save"
    res=sess.post(url,data=data)
    mess=json.loads(res.text)
    print(mess["m"])

def HealthData(DiYiZhen,DiErZhen,DiSanZhen):
    data = {
        "zgfxdq": "0",
        "mjry": "0",
        "csmjry": "0",
        "szxqmc": "江安校区",
        "sfjzxgym": "1",
        "jzxgymrq": DiYiZhen,
        "sfjzdezxgym": "1",
        "jzdezxgymrq": DiErZhen,
        "sfjzdszxgym": "1",
        "jzdszxgymrq": DiSanZhen,
        "uid": "",
        "date": "",
        "tw": "2",
        "sfcxtz": "0",
        "sfyyjc": "0",
        "jcjgqr": "0",
        "jcjg": "",
        "sfjcbh": "0",
        "sfcxzysx": "0",
        "qksm": "",
        "remark": "",
        "address": "四川省成都市双流区西航港街道四川大学江安校区",
        "area": "四川省+成都市+双流区",
        "province": "四川省",
        "city": "成都市",
        "geo_api_info": {
            "type": "complete",
            "position": {"Q": 30.55300374349, "R": 103.99391167534799, "lng": 103.993912, "lat": 30.553004},
            "location_type": "html5",
            "message": "Get+ipLocation+failed.Get+geolocation+success.Convert+Success.Get+address+success.",
            "accuracy": 35,
            "isConverted": "true",
            "status": 1,
            "addressComponent": {
                "citycode": "028",
                "adcode": "510116",
                "businessAreas": [{
                    "name": "白家",
                    "id": "510116",
                    "location": {
                        "Q": 30.562482,
                        "R": 104.006821,
                        "lng": 104.006821,
                        "lat": 30.562482
                    }
                }],
                "neighborhoodType": "",
                "neighborhood": "",
                "building": "",
                "buildingType": "",
                "street": "川大路二段",
                "streetNumber": "1号",
                "country": "中国",
                "province": "四川省",
                "city": "成都市",
                "district": "双流区",
                "towncode": "510116002000",
                "township": "西航港街道"
            },
            "formattedAddress": "四川省成都市双流区西航港街道四川大学江安校区学生西园8舍围合",
            "roads": [],
            "crosses": [],
            "pois": [],
            "info": "SUCCESS"
        },
        "created": "1649433631",
        "sfzx": "1",
        "sfjcwhry": "0",
        "sfcyglq": "0",
        "gllx": "",
        "glksrq": "",
        "jcbhlx": "",
        "jcbhrq": "",
        "sftjwh": "0",
        "sftjhb": "0",
        "fxyy": "",
        "bztcyy": "1",
        "fjsj": "0",
        "sfjchbry": "0",
        "sfjcqz": "",
        "jcqzrq": "",
        "jcwhryfs": "",
        "jchbryfs": "",
        "xjzd": "",
        "szgj": "",
        "sfsfbh": "0",
        "szsqsfybl": "0",
        "sfsqhzjkk": "0",
        "sqhzjkkys": "",
        "sfygtjzzfj": "0",
        "gtjzzfjsj": "",
        "szcs": "",
        "sfjxhsjc": "0",
        "hsjcrq": "",
        "hsjcdd": "",
        "hsjcjg": "0",
        "bzxyy": "",
        "id": "",
        "gwszdd": "",
        "sfyqjzgc": "",
        "jrsfqzys": "",
        "jrsfqzfy": "",
        "szgjcs": "",
        "ismoved": "0"
    }
    if DiYiZhen=="":
        data["sfjzxgym"]="0"
    if DiErZhen=="":
        data["sfjzdezxgym"]="0"
    if DiSanZhen=="":
        data["sfjzdszxgym"]="0"
    return data

def Login(Username,Password):
    count=1
    while count<=5:
        be =Visit()
        Execution =GetExecution(be)
        Captcha =GETCaptcha(be)
        data =SetPost(Username,Password,Execution,Captcha)
        status =Rush(data)
        if status==200:
            return "Success!";
        count+=1
    return "Failed!"

def Logout():
    sess.get("http://uc.scu.edu.cn/api/logout")

def run(User,Pass,DiYiZhen,DiErZhen,DiSanZhen):
    Username=User
    Password=Pass
    print("%s登录微服务中............"%(Username))
    if Login(Username,Password) == "Failed!":
        print("用户名或密码错误")
        return "Wrong"
    print("登陆成功！正在配置打卡数据................")
    data = HealthData(DiYiZhen,DiErZhen,DiSanZhen)
    print("配置成功！正在打卡................")
    Daka(data)
    Logout()
    print("已下线.........")
    return "OK"