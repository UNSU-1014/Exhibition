from flask import Flask, render_template, request, jsonify, redirect
import json
from random import randint
import gmail_send
import weather_api

import torch
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MaxAbsScaler

import copy

class Net(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, layers):
        super(Net, self).__init__()
        self.rnn = torch.nn.LSTM(input_dim, hidden_dim, num_layers=layers, batch_first=True)
        self.fc = torch.nn.Linear(hidden_dim, output_dim, bias=True)
    
    def forward(self, x):
        x, _status = self.rnn(x)
        x = self.fc(x[:, -1])
        return x


# 앱 생성
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html') # index.html를 반환

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method == "POST":
        # 웹 페이지에서 전달된 값 확인
        c_name = request.form.get('c_name')
        c_email = request.form.get('c_email')
        c_text = request.form.get('c_text')
        print(c_name,c_email,c_text)

        # 가계정 봇으로 전달
        s_mail = "real.light.bot@gmail.com"
        s_name = "참빛 문의봇"
        pwd = "rkdgmlwl70"

        # 관리자 메일
        r_mail = "real.light.manager@gmail.com"
        r_name = "참빛 관리자"

        # 메일 내용
        title = "참빛 문의가 들어왔습니다. [{}-{}]".format(c_name,c_email)
        content = "[성명] : {}\n[이메일] : {}\n[문의내용]\n{}".format(c_name,c_email,c_text)

        # 이메일로 전송
        gmail_send.sendmail(s_mail,r_mail,pwd,title,content,s_name,r_name)

        return redirect('/') 
    else:
    	return render_template('contact.html') 


# jquery의 ajax 통신
@app.route('/getData',methods=['POST'])
def get_data():
    data = request.get_json() # 요청 중 전달받은 데이터가 json형태 문자열이니 dict형으로 변환
    print("요청받은 데이터",data) # 문자열이 아닌 실제 데이터로 변환됨
    city = data['city_id'] # '서울'
    local = data['local_id'] # '강남구'

    ######## 공공데이터 포털 동네 예보 api 요청 ########
    
    while True:
        try:
            weather_data = weather_api.get_town_weather(city,local)
            print("받아온 날씨 정보 : ", weather_data)
            break
        except:
            pass

    # weather_data 든 데이터 예시

    ##################################################

    ################# 범죄율 계산 #####################
    
    torch.manual_seed(0)

    data_dim = 6
    hidden_dim = 20
    output_dim = 7
    #learning_rate = 0.01
    #iterations = 500
    
    PATH = "./static/model/[서울]MODEL"

    model = Net(data_dim, hidden_dim, output_dim, 1)
    model = torch.load(PATH)
    model.eval()

    ii = ['강수량', '최고기온', '최저기온', '습도', '풍향', '풍속']
    input = [ weather_data[list(weather_data.keys())[0]][i] for i in ii ]

  
    for i in range(len(input)):
        input[i] = float(input[i])
    print(input)
    hour_var = torch.tensor([[input]])
    print(model.forward(hour_var)[0])
    pred = model.forward(hour_var)[0]

    sum = 0
    pred = list(pred)
    for i in range(len(pred)):
        pred[i] = float(pred[i])
        sum += pred[i]
    ##################################################

	#임시
    
    data = {
        '강력범' : pred[0]/sum * 100, # 10 ,
        '절도범' : pred[1]/sum * 100, # 20 ,
        '폭력범' : pred[2]/sum * 100, # 30 ,
        '지능범' : pred[3]/sum * 100, # 40 ,
        '풍속범' : pred[4]/sum * 100, # 50 ,
        '기타형사범' : pred[5]/sum * 100, # 60,
        '특별법범' : pred[6]/sum * 100, # 70
    }
    print(pred)
    # 데이터 반환
    response = data
    print(response)

    return jsonify(response)

# 메인
if __name__ == '__main__':
    app.run(debug=True)
