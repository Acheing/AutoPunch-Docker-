import json
import app

def Load():
    filename = 'data.json'
    with open(filename) as f:
        Student =json.load(f)
    return Student

def run():
    data=Load()
    l=[]
    for i in data["Students"]:
        if app.run(i["Username"],i["Password"],i["DiYiZhen"],i["DiErZhen"],i["DiSanZhen"])=="Wrong":
            l.append(i["Username"])
    for i in l:
        print(i+"打卡失败")

if __name__=="__main__":
    run()