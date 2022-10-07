from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests import get
from bs4 import BeautifulSoup


def extract_product_bunjang(keyword):
    results = []
    pageNb = int(get_pageNb_bunjang(keyword))
    base_url = "https://m.bunjang.co.kr/search/products?order=score"

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)

    for i in range(pageNb):
        browser.get(f"{base_url}&q={keyword}&page={i+1}")

        response = browser.page_source

        soup = BeautifulSoup(response, "html.parser")
        ul = soup.find("div", class_="sc-iiUIRa")
        if ul == None:
            return []
        else:
            products = ul.find_all("div", class_="sc-hgRTRy")
            for product in products:
                anchor = product.find("a")
                link = anchor["href"]
                name = anchor.find("div", class_="sc-fcdeBU").string
                info = anchor.find("div", class_="sc-RcBXQ")
                price = info.find("div", class_="sc-gmeYpB").string
                product_data = {
                    "link": f"https://m.bunjang.co.kr{link}",
                    "title": name,
                    "price": f"{price}원"
                }
                results.append(product_data)
    return results


def get_pageNb_bunjang(keyword):
    base_url = "https://m.bunjang.co.kr/search/products?q="

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    browser.get(f"{base_url}apple")

    response = browser.page_source

    soup = BeautifulSoup(response, "html.parser")
    pagination = soup.find("div", class_="sc-cJOK")
    pageNbs = pagination.find_all("a", class_="sc-ccSCjj")[-2].string
    print(pageNbs)
    return pageNbs
