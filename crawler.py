import requests
from bs4 import BeautifulSoup
def card():
    card_dic={}
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    url='https://rich01.com/credit-card-utility-bill/'
    re=requests.get(url,verify=False,headers=header)
    soup=BeautifulSoup(re.text,'html.parser')
    table=soup.find_all('table',{'style':'border-collapse: collapse; width: 100%; height: 181px;'})
    t=soup.find('table', {'style':"border-collapse: collapse; width: 100%;"})
    table.append(t)
    i=0
    for title in soup.find_all('span',{'style':"font-size: 20px; color: #014876;"}):
        card_dic[title.text.strip()]=[]
        t=table[i]
        for tr in t.find_all('tr'):
            td=tr.find_all('td')
            try:
                c=td[1].text.replace('\n', '').strip()
                card_dic[title.text.strip()].append(f'{td[0].text.strip()}  {c}')
            except:
                break
        i+=1 

    card_4=soup.find('table', {'style':"border-collapse: collapse; width: 100%; height: 112px;"}).find('p',{'style':'text-align: center;'}).text.replace('\n','').strip()
    card_dic[card_4]=[]
    c_lst=soup.find('td', {'style':"text-align: center; height: 48px;"}).text.split('\n')
    card_dic[card_4].append(c_lst[2])
    card_dic[card_4].append(f'回饋比例  {c_lst[0]} {c_lst[1]}')
    card_dic[card_4].append(f'回饋條件  {c_lst[3]}')
    ld_lst=soup.find_all('td', {'style':"text-align: center; height: 48px;"})[1].text.strip().split('\n')
    card_dic[card_4].append(f'回饋上限/可刷金額  {ld_lst[0]}:{ld_lst[1]} {ld_lst[2]}')
    card_dic[card_4].append(f'活動日期  {ld_lst[3]}')
    #print(c_lst[2])
    card_5=soup.find('table', {'style':"border-collapse: collapse; width: 100%; height: 129px;"}).find('p',{'style':'text-align: center;'}).text.replace('\n','').strip()
    card_dic[card_5]=[]
    c5_lst=soup.find('td', {'style':"height: 48px; width: 34.6864%;"}).text.strip().split('\n')
    card_dic[card_5].append(c5_lst[1])
    card_dic[card_5].append(f'回饋比例  {c5_lst[0]}')
    card_dic[card_5].append(f'回饋條件  • 綁定Fami Pay{c5_lst[2]}{c5_lst[3]}')
    ld5_lst=soup.find('td', {'style':"text-align: center; height: 48px; width: 36.0397%;"}).text.strip().split('\n')
    card_dic[card_5].append(f'回饋上限/可刷金額  {ld5_lst[0]}')
    card_dic[card_5].append(f'活動日期  {ld5_lst[1]}')

    card_6=soup.find('table', {'style':"border-collapse: collapse; width: 100%; height: 129px;"}).find_all('p',{'style':'text-align: center;'})[5].text.replace('\n','').strip()
    card_dic[card_6]=[]
    c6_lst=soup.find('td', {'style':"width: 34.6864%;"}).text.strip().split('\n')
    card_dic[card_6].append(c6_lst[1])
    card_dic[card_6].append(f'回饋比例  {c6_lst[0]}')
    card_dic[card_6].append(f'回饋條件  {c6_lst[2]}{c6_lst[3]}')
    ld6_lst=soup.find('td', {'style':"text-align: center; width: 36.0397%;"}).text.strip().split('\n')
    card_dic[card_6].append(f'回饋上限/可刷金額  {ld6_lst[0]}')
    card_dic[card_6].append(f'活動日期  {ld6_lst[1]}')

    card_7=soup.find('table', {'style':"border-collapse: collapse; width: 100%; height: 130px;"}).find_all('p',{'style':'text-align: center;'})[6].text.replace('\n','').strip()
    card_dic[card_7]=[]
    c7_lst=soup.find_all('td', {'style':"width: 34.6864%;"})[1].text.strip().split('\n')
    card_dic[card_7].append(c7_lst[1])
    card_dic[card_7].append(f'回饋比例  {c7_lst[0]}')
    card_dic[card_7].append(f'回饋條件  {c7_lst[2]}')
    ld7_lst=soup.find_all('td', {'style':"text-align: center; width: 36.0397%;"})[1].text.strip().split('\n')
    card_dic[card_7].append(f'回饋上限/可刷金額  {ld7_lst[0]}')
    card_dic[card_7].append(f'活動日期  {ld7_lst[1]}')

    card_dic['國泰Cube icash卡'].insert(0,'水電/瓦斯/路邊停車')
    card_dic['聯邦綠卡'].insert(0,'水電/瓦斯/電信/路邊停車')
    card_dic['台新@GoGo卡'].insert(0,'水電/瓦斯/電信')

    for k in card_dic:
        print(k)
        for i in card_dic[k]:
            print(i)
        print('\n')
    return 'ok'
card()
