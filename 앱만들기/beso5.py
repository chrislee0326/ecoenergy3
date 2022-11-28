#<라이브러리 함수 가져오기>
import requests 
from bs4 import BeautifulSoup
import re

#<한국 전력 거래소_실시간 전력수급현황 사이트에서 발전원별 발전량 데이터 가져오기>
url = "https://new.kpx.or.kr/powerSource.es?mid=a10606030000&device=chart"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
res = requests.get (url, headers = headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml") 

#<변수 설정>
all = soup.find("tbody").tr #전체 정보(리스트 형태)
time = all.td #일시:all안의 리스트에서 가장 첫번째 줄 데이터  (예시: 2022년 11월 13일 20시 30분)
another = time.next_sibling.next_sibling #기타(발전량):all안의 리스트에서 time 다음 줄의 데이터  (예시: 1,248)

#<현재 시각의 정보를 가져오기>

#아직 정보가 올라오지 않은 경우 발전량 값이 0이 표시된다.(예를 들어 현재시각이 9시이라 하면 11시의 데이터 값은 0으로 표시된다)
#따라서 발전량 값이 처음으로 0이 나온 시각 바로 전 시간의 데이터를 가져오는 과정을 수행한다.
#(예, 8시데이터:1283, 9시데이터:3589, 10시데이터:0 ==> 10시바로 전시간인 9시 데이터"3589"를 가져온다.)

while True:  
    if str(another) == '<td>0</td>': #another;기타 발전량이 0일때
        all = all.previous_sibling.previous_sibling #바로 전(previous)의 정보 확인

        #변수 재설정
        time = all.td #시각
        another = time.next_sibling.next_sibling #기타
        gas = another.next_sibling.next_sibling #가스
        eco = gas.next_sibling.next_sibling #신재생
        coal = eco.next_sibling.next_sibling #석탄
        nuclear = coal.next_sibling.next_sibling #원자력

        break #while loof문 나가기

    else:
        #가져온 데이터가 23시 30분인지 확인
        p = re.compile("23시 30분")
        m = p.search(str(time))

        if m: #23시30분인 경우 (마지막이라 뒤에 0이 나오는 경우가 없음)
            another = time.next_sibling.next_sibling #기타
            gas = another.next_sibling.next_sibling #가스
            eco = gas.next_sibling.next_sibling #신재생
            coal = eco.next_sibling.next_sibling #석탄
            nuclear = coal.next_sibling.next_sibling #원자력 

            break #while loof문 나가기

        else: #23시 30분이 아닌 경우
            all = all.next_sibling.next_sibling #11시 30분이 아니고, 0이 아니라면 다음 시각의 정보 확인

            #변수 재설정
            time = all.td 
            another = time.next_sibling.next_sibling 
        
        continue #0이 되기 전까지 계속 반복하기

#<받아온 자료 숫자형으로 변환>

#기타(another)의 경우 양수 펌핑에 의해 발전량이 - 값이 되는 경우가 있어 다음 과정을 수행
another = str(str(another).replace(',',''))
another2 = [];del another2[:]
another2 = re.findall("-?\d+", str(another));another2 = another2[0]

#나머지의 경우 항상 + 값이므로 아래와 같은 과정을 수행
gas = re.sub(r'[^0-9]', '', str(gas))
eco = re.sub(r'[^0-9]', '', str(eco))
coal = re.sub(r'[^0-9]', '', str(coal))
nuclear = re.sub(r'[^0-9]', '', str(nuclear))

#<전체 발전량 계산>
total = int(another2) + int(gas) + int(eco) + int(coal) + int(nuclear)

#<비율계산>
rate1 = int(eco)/total#신재생에너지 발전량/전체 발전량

#<등급 판정하기>
def gradejudge(rate):
    if rate > 0.12:
        return("최고") 
    elif 0.12>=rate>0.1:
        return("좋음") 
    elif 0.1>=rate>0.08:
        return("보통") 
    elif 0.08>=rate>0.06:
        return("나쁨") 
    else:
        return("매우나쁨") 

grade1 = gradejudge(rate1)

#<UI표현하기>
import streamlit as st
primaryColor="white"

st.write('# 현재 재생에너지 등급은...?')

#<배경&이미지 출력하기>
from PIL import Image
import pandas as pd
from PyPDF2 import PdfFileReader
import os

#<등급별 아이콘 표시 및 배경색 변경>
if grade1 == "최고" :
    st.image('https://api.rootall.org/media/editor/verygoodjpg.jpg', width=300)
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-color : #1E73D2
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
if grade1 == "좋음" :
    st.image('https://api.rootall.org/media/editor/goodjpg_9uhyYZs.jpg', width=380)
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-color : #0785D1
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
if grade1 == "보통" :
    st.image('https://api.rootall.org/media/editor/normaljpg_mIG1m3L.jpg', width=380)
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-color : #07B86A
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
if grade1 == "나쁨" :
    st.image('https://api.rootall.org/media/editor/badjpg_GbV9mas.jpg', width=380)
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-color : #FA9102
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
if grade1 == "매우나쁨" :
    st.image('https://api.rootall.org/media/editor/verybadjpg_0aMa6ST.jpg', width=380)
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-color : #CC332E
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

#<기타 정보 표시>
rate2 = 100*float(str(rate1)); rate2 = round(rate2, 2)
st.write('##    발전 비율: '+ str(rate2) + '%')
if st.checkbox('자세히 보기'):
    st.write('날짜/시간: '+ str(time))
    st.write('전체발전량: '+ str(total)+'MW')
    st.write('신재생에너지: '+str(eco)+'MV')
    st.write('가스: '+str(gas)+'MV')
    st.write('화력발전(석탄발전): '+str(coal)+'MV')
    st.write('원자력발전: '+str(nuclear)+'MV')
    st.write('기타: '+str(another2)+'MV')
st.write("*매우나쁨 일 때는 이렇게 행동하세요! : 인쇄 작업, 난방, 샤워 등 일시적으로 전기를 사용해야하는 행동을 자제하세요. 이후 등급이 올라갔을 때 미루었던 일을 마무리하시기 바랍니다.")
st.write("*이 앱은 한국 전력 거래소 사이트의 실시간 전력수급현황_발전원별 발전량 데이터를 기반으로 합니다. (링크)")
st.write("*비율계산식: (신재생에너지 발전량/전체 발전량)*100(%)")
st.write("<등급표>")






