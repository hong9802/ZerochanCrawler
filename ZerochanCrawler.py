from bs4 import BeautifulSoup
import re
import requests
import urllib
from multiprocessing import Pool

count = [] #페이지 저장용 리스트
i = 1
userurl = "https://www.zerochan.net/Shigure+%28Kantai+Collection%29"
#시구레 사진만 크롤링하기 위해 시구레 이미지 주소 넣음
#타 캐릭터도 저런 형식으로 이미지 주소 넣으면 됨.

def checkingimg(imgstr): #각 이미지 확장자 함수
    if(imgstr.find(".jpg") != -1) :
        return ".jpg"
    elif(imgstr.find(".png") != -1) :
        return ".png"
    elif(imgstr.find(".jpeg") != -1) :
        return ".jpeg"
    elif(imgstr.find(".gif") != -1) :
        return ".gif"

def pageChecker(): #페이지 수 체크용 함수
    while True :
        global i
        print(i)
        url = userurl +'?p='+ str(i)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        mr2 = soup.find("ul", id = 'thumbs2')
        if(mr2 == None) :
            print('break')
            break
        else :
            count.append(i)
            i+=1
    print(len(count))

def worker(page): #크롤링 전용 함수
    global i
    url = userurl + '?p='+ str(page)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    try :
        for z in range(0, 90, 1) :
            mr = soup.find("ul", id = 'thumbs2')
            mr2 = mr.find_all("a")
            link1 = str(mr2[z])
            print(link1[9:17])
            if(link1[9:17].startswith('https://')) :
                pass
            elif(link1[9:17].startswith('/registe')) :
                pass
            else :
                url2 = 'https://www.zerochan.net' + link1[9:17]
                r2 = requests.get(url2)
                soup2 = BeautifulSoup(r2.text, "html.parser")
                mr = soup2.find("div", id = "large")
                if(mr == None) :
                    pass
                mr2 = mr.find("img")
                i+=1
                link2 = str(mr2)
                first = link2.find('src') + 5
                link3 = link2[first:]
                a = link3.split()
                stra = str(a[0])
                final = stra.replace("\"", "")
                extension = checkingimg(final)
                urllib.request.urlretrieve(final, 'shigure/' + str(page) + "00" + str(i) + extension) #이미지 저장!
    except IndexError as e :
        pass

if(__name__ == "__main__"):
    pageChecker() #페이지를 체크하고~
    i = 0
    thread = Pool(8) #프로세스를 8개 만들고~
    thread.map(worker, range(1, len(count) + 1, 1)) #일해라 핫산!!!