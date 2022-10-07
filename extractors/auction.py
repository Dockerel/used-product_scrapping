from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests import get
from bs4 import BeautifulSoup


def extract_product_auction(keyword):
    results = []

    pageNb = get_pageNb_bunjang(keyword)
    base_url = "https://corners.auction.co.kr/corner/UsedMarketList.aspx"
    if pageNb == 1:
        final_url = f"{base_url}?keyword={keyword}"
    elif pageNb == 0:
        return []
    else:
        final_url = f"{base_url}?keyword={keyword}&page={pageNb}"

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)

    for i in range(pageNb):
        browser.get(final_url)

        response = browser.page_source

        soup = BeautifulSoup(response, "html.parser")
        products_ul = soup.find("div", class_="used_listview_wrap")

        products = products_ul.find_all("div", class_="list_view")
        for product in products:
            linkDiv = product.find("div", class_="image_info")
            linkAnchor = linkDiv.find("a")
            link = linkAnchor["href"]
            titleDiv = product.find("div", class_="item_title_info")
            titleAnchor = titleDiv.find("a")
            title = titleAnchor.string
            priceDiv = product.find("div", class_="market_info")
            price = priceDiv.find("strong").string
            product_data = {
                "link": link,
                "title": title,
                "price": f"{price}원"
            }
            results.append(product_data)
    return results


def get_pageNb_bunjang(keyword):
    base_url = "https://corners.auction.co.kr/corner/UsedMarketList.aspx"

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    browser.get(f"{base_url}?keyword={keyword}")

    response = browser.page_source

    soup = BeautifulSoup(response, "html.parser")

    pagination = soup.find("div", class_="paginate")
    if pagination == None:
        pageNb = 0
    else:
        anchorLen = len(pagination.find_all("a"))
        if anchorLen == 8:
            pageNb = 7
        elif anchorLen > 0 and anchorLen < 8:
            pageNb = anchorLen
    return pageNb
