import pandas as pd
import requests
from bs4 import BeautifulSoup

# 추이에 대한 이미지를 출력하는 것
def get_img(stock_code):
    try:
        print(stock_code)
        url = "https://finance.naver.com/item/main.nhn?code={}".format(stock_code)
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser") # 현재 URL 가져옴
        img_link = bs_obj.find("div",{"class" : "chart"}).find("img").get("src")
        print(img_link)
        return img_link
    except:
        return "Error"

# 단축 종목을 부르는 함수
def get_Jongmok(stock_code):
    try :
        print(stock_code)
        url = "https://finance.naver.com/item/main.nhn?code={}".format(stock_code)
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser") # 현재 URL 가져옴
        ### 현재 시세 출력하는 구문
        if bs_obj == None :
            return "정확한 코드를 입력해주세요"
        name = bs_obj.find("div", {"class" : "h_company"}).find("div", {"class" : "wrap_company"}).find("h2").text
        print(name)
        no_today = bs_obj.find("p", {"class": "no_today"}) # 태그 p, 속성값 no_today 찾기
        no_today_blind = no_today.find("span", {"class": "blind"}).text # 태그 span, 속성값 blind 찾기 - 현재 시세
        no_info_table = bs_obj.find("table", {'class' : 'no_info'})
        trs = no_info_table.find_all('tr')
        for idx, tr in enumerate(trs) : 
            if idx > -1 :
                tds = tr.find_all('td')
                if idx == 0 :
                    before_day = tds[0].find("span", {"class": "sptxt sp_txt2"}).text ## 전일
                    before_day_value = str(tds[0].find("span", {"class" : "blind"}).text)
                    high = tds[1].find("span", {"class":"sptxt sp_txt4"}).text ## 고가
                    high_value = tds[1].find("span", {"class" : "blind"}).text
                    #max_ = tds[1].find("span", {"class":"sptxt sp_txt6"}).text ## 상한가
                    #max_value = tds[1].find("em", {"class": "no_cha"}).find("span", {"class" : "blind"}).text 

                    trading_volume = tds[2].find("span", {"class":"sptxt sp_txt9"}).text ## 거래랑
                    trading_volume_value = tds[2].find("span", {"class":"blind"}).text
                else :

                    market = tds[0].find("span", {"class": "sptxt sp_txt3"}).text ## 시가
                    market_value = tds[0].find("span", {"class" : "blind"}).text 

                    low = tds[1].find("span", {"class":"sptxt sp_txt5"}).text ## 저가
                    low_value = tds[1].find("span", {"class" : "blind"}).text
                    # max_ = tds[1].find("span", {"class":"sptxt sp_txt7"}).text ## 하한가
                    # max_value = tds[1].find("em", {"class": "no_cha"}).find("span", {"class" : "blind"}).text 

                    trading_money = tds[2].find("span", {"class":"sptxt sp_txt10"}).text ## 거래대금
                    trading_money_value = (tds[2].find("span", {"class":"blind"}).text) + "백만"

                    result = {before_day : before_day_value, high : high_value, trading_volume : trading_volume_value, market : market_value, low : low_value, trading_money : trading_money_value}
                    # json_val = json.dumps(dict1) dict to json
        result_str = name + "의 정보 입니다. \n" + "현재가 : " + no_today_blind + '\n '
        for key, val in result.items():
            result_str = result_str + key + " : " + val + " \n"
        print("result_str 값 입니다. ")
        print(result_str)
        return result_str
                            
                        
        ## Table을 가져와 전일 고가 거래량 시가 저가 출력
    except AttributeError as e :
        print("타입 에러 발생")
        return "정확한 코드를 입력해주세요"
    except :
        return "정확한 코드를 입력해주세요"



def get_sise(stock_code) : # 종목 별 여러 기간의 출력
    url = 'http://finance.naver.com/item/sise_day.nhn?code={}'.format(stock_code)
    df = pd.DataFrame()
    if stock_code == ""  or stock_code == None :
        return "적절한 값이 아닙니다."
    for page in range (1,5) :
        pg_url = '{url}&page={page}'.format(url = url, page = page)
        df = df.append(pd.read_html(pg_url,header =0)[0], ignore_index = True)
    df = df.dropna()
    df["날짜"] = df["날짜"].apply(lambda x : str(x))
    df["종가"] = df["종가"].apply(lambda x : str(x))
    df["전일비"] = df["전일비"].apply(lambda x : str(x))
    df["시가"] = df["시가"].apply(lambda x : str(x))
    df["고가"] = df["고가"].apply(lambda x : str(x))
    df["저가"] = df["저가"].apply(lambda x : str(x))
    df["거래량"] = df["거래량"].apply(lambda x : str(x))
    print(df)
    result_list = []
    result1 = "날짜  종가    전일비  \n"
    result2 = "시가    고가    저가    거래량\n"
    for idx,row in df.iterrows():
        result1 =  result1 + row["날짜"] + "  " + row["종가"] + " " + row["전일비"] + "\n" 
        result2 = result2 + row["시가"] + " " + row["고가"] + " " + row["저가"] + " " + row["거래량"] + "\n" 
    result_list.append(result1)
    result_list.append(result2)
    return result_list

def get_code () :
    code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
    code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
    code_df = code_df[['회사명', '종목코드']]
    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
    return code_df

def search_code(Name) :
    code_df = get_code()
    code_df['name'] = code_df['name'].apply(lambda x : str(x))
    code_df['code'] = code_df['code'].apply(lambda x : str(x))
    code_df = code_df[code_df['name'].str.contains(Name)]
    print(code_df)
    result = ""
    for idx,row in code_df.iterrows():
        result =  result + row["name"] + " : " + row["code"] + "\n"
    return result

if __name__ == '__main__' :
    print(1)