import requests
from bs4 import BeautifulSoup

def main():
    url = "https://ktu.edu.in/eu/core/announcements.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table", {"class": "ktu-news"})
    tr_list = table.findAll("tr")
    # print(tr_list)

    data = []
    for tr in tr_list:
        links = []
        content = tr.findAll("b")
        try:
            links_all = tr.findAll("a")
            for link in links_all:
                link = str(link.get('href'))
                if link.startswith('/'):
                    link = "https://ktu.edu.in"+link
                links.append(link)
        except:
            links = []
        date = content[0].text
        title = content[1].text

        texts = tr.find("li").findAll(text=True)
        content = ''
        for text in texts:
            if len(text) > 22:
                if text != title:
                    content = text.replace('\n','').replace('\r','')
                    break

        data.append(dict({'date': date, 'title': title, 'link': links, 'content': content}))
        
    # print(data[21])

if __name__ == "__main__":
    main()