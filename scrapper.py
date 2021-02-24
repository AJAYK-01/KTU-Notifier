import requests
from bs4 import BeautifulSoup

def scrape():
    url = "https://ktu.edu.in/eu/core/announcements.htm"
    #Since Dumb KTU can go down any minute, it's best to use Try Except
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html5lib')
        table = soup.find("table", {"class": "ktu-news"})
        tr_list = table.findAll("tr")

        data = []
        for tr in tr_list:
            links = []
            content = tr.findAll("b")
            try:
                links_all = tr.findAll("a")
                for link in links_all:
                    text = link.find(text=True)
                    link = str(link.get('href'))
                    if link.startswith('/'):
                        link = "https://ktu.edu.in"+link
                    links.append(dict({'url': link, 'text': text}))
            except:
                links = []
            date = content[0].text.split(':')[0][:-3]
            title = content[1].text

            texts = tr.find("li").findAll(text=True)
            content = ''
            for text in texts:
                if len(text) > 25 and text != title:
                    """ 25 is an arbitrarily taken length, content is definitely more than 25 characters
                    and hyperlink text (eg, notification, timetable) is definitely less than 25 """
                    content += text.replace('\n','').replace('\r','')+'\n'

            data.append(dict({'date': date, 'title': title, 'link': links, 'content': content}))
    
    except Exception as e:
        data = []
        print(str(e))
    # print(data[0])
    return data
