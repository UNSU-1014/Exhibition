import requests
from datetime import datetime, timedelta
from pprint import pprint

# 지역별 격자
locations_xy = {
    "서울":{"종로구": [60,127],"중구" : [60,127],"용산구" : [60, 126],
        "광진구":[62,126],"동대문구":[61,127],"중랑구":[62,128],
        "성북구":[61,127],"강북구":[61,128],"도봉구":[61,129],
        "노원구":[61,129],"은평구":[59,127],"서대문구":[59,127],
        "마포구":[59,127],"양천구":[58,126],"강서구":[58,126],
        "구로구":[58,125],"금천구":[59,124],"영등포구":[58,126],
        "동작구":[59,125],"관악구":[59,125],"서초구":[61,125],
        "강남구":[61,126],"송파구":[62,126],"강동구":[62,126],
        "성동구":[61,127]   
    },
    "대구":{
        "중구":[89,	90],"동구":[90,	91],"서구":[88,	90],"남구":[89,	90],
        "북구":[89,91],"수성구":[89,90],"달서구":[88,90],"달성군":[86,88]
    },
    "광주":{
        "동구":[60,74],"서구":[59,74],"남구":[59,73],"북구":[59,75],"광산구":[57,74]
    }
}


categorys = {
    "POP":	"강수확률",
    "PTY":	"강수형태",
    "R06":	"강수량",
    "REH":	"습도",
    "S06":	"신적설",
	"SKY":	"하늘상태",
	"T3H":	"온도",
	"TMN":	"최저기온",
	"TMX":	"최고기온",
	"UUU":	"풍속(동서성분)",
	"VVV":	"풍속(남북성분)",
	"WAV":	"파고", # 바다가 지역에서 받아와지기때문에 이 데이터는 들어오지 않는다.
	"VEC":	"풍향",
	"WSD":	"풍속"
}



# 동네 예보 api 정보 가져오기
def get_town_weather(city, local):
    # locations_xy에서 격자 좌표 가져오기
    x,y = locations_xy[city][local]
    
    # 현재 날짜 가져오기
    day = datetime.now()
    
    # 오늘 데이터 요청
    base_date = day.strftime("%Y%m%d") # '20200531'
    base_time = "0200" # 오늘, 내일 최저 최고기온은 2시발표에 들어있다.

    # 예외 상황 -2시 이전
    if  day.hour < 3 and day.minute < 15 :
        base_date = (day-timedelta(days=1)).strftime("%Y%m%d") # '20200530'
        base_time = "2300"

    town_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst"
    params ={
        'ServiceKey' : "X2fqMe/7ekwwheQ2Ev8BfcGO9vLw7iei11mKxLemkgiN1CCCii3vz1Mhl8wn2F4Knird5UlAOAcwyhW75lH2ow==",
        'pageNo' : 1,
        'numOfRows' : 300, # 요청시 받을 데이터의 개수
        'dataType' : 'JSON',
        'base_date' : base_date, # '20200531',
        'base_time' : base_time, # '0800',
        'nx' : x, # 1,
        'ny' : y # 1
    }

    res = requests.get(town_url, params=params)

    data = res.json()['response']['body']['items']['item']


    # 날짜 별로 요청 받기
    result = {}
    for d in data:

     
        # 처음 날짜 정보로 된 key가 없을 경우, 날짜 '20200606' 키 생성
        if not result.get(d['fcstDate']):
     
            result[d['fcstDate']] = {}
        
        # 현재 정보를 category로 번역해서 집어넣기

        if d['category'] not in ['POP',"PTY",'SKY','S06',"T3H",'UUU','VVV']:
            result[d['fcstDate']][categorys[d['category']]] = d['fcstValue']


    # 모레 데이터 삭제
    try:
        result.pop((day+timedelta(days=2)).strftime("%Y%m%d"))
    except:
        pass

    return result

