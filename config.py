def search(name):
    from bs4 import BeautifulSoup
    import requests
    url=f"http://www.taronatv.com/search/?q={name}&sfSbm="
    page=requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    responses=soup.find_all(class_="entryLink")
    res_images=soup.find_all(class_="fancybox")
    return [responses,res_images]
def result_search(url):
    from bs4 import BeautifulSoup
    import requests
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    result = soup.find(class_="v_text").find_all("span")
    # print(result)

    results=[]
    res_href=[]
    for res in result:
        is_film = res.find_all("a")
        if len(is_film)!=0:
            for isf in  is_film:
                if "http://" in isf["href"]:
                    href=isf["href"]
                    name=isf.get_text()
                    if not href in res_href:
                        res_href.append(href)
                        results.append([name,href])
    return [result[0].get_text(),results]
def get_photo(url):
    from bs4 import BeautifulSoup
    import requests
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    result = soup.find(class_="fancybox")["href"]
    return f"http://taronatv.com{result}"