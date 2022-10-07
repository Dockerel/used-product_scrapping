from extractors.auction import extract_product_auction
from extractors.bunjang import extract_product_bunjang

keyword = input("Search for Used Products : ")
filename = keyword
auction = extract_product_auction(keyword)
bunjang = extract_product_bunjang(keyword)
products = auction+bunjang

file = open(f"{filename}.csv", "w")
file.write("Link, Title, Price\n")

for product in products:
    file.write(f"{product['link']}, {product['title']}, {product['price']}\n")
file.close()
