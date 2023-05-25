import requests, json, msvcrt, os
from bs4 import BeautifulSoup as BS
#url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=21&limit=20&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,self_reported_circulating_supply,self_reported_market_cap"

headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

def get_amount() -> int:
    r = requests.get("https://coinmarketcap.com/", headers=headers).text
    soup = BS(r, "lxml")
    last_page = int(soup.find_all("li", class_="page")[-1].text)
    amount_in_last = len(BS(requests.get("https://coinmarketcap.com/?page="+str(last_page), headers=headers).text, "lxml").find("tbody").find_all("tr"))
    return (last_page-1)*100+amount_in_last

def print_elements(elements: dict, page: int) -> None:
    os.system("cls")
    print("  #   |         NAME         |    SYMBOL    |      PRICE      |    MARKET CAP   ")
    for i, c in enumerate(elements, start=1+(page-1)*20):
        print("%-5d | %-20s | %-12s | $%-14.6f | $%3.3f" %(i, c["name"][:20], c["symbol"][:12], c["price"], c["market_cap"]))
    print("------+----------------------+--------------+-----------------+---------------------\n      | PgUp - next page     | PgDn - previous page \n\
      | Home - first page    | End - last page\n\
      | Insert - search      | R - Refresh")

def get_elements() -> list:
    jsn = requests.get("https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=%d&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d,self_reported_circulating_supply,self_reported_market_cap" % (get_amount())).text
    data = json.loads(jsn)      

    elements = [{"name":element["name"],
            "symbol":element["symbol"],
            "price":element["quotes"][2]["price"],
            "market_cap":element["quotes"][2]["marketCap"]} for element in data["data"]["cryptoCurrencyList"]]
    return elements

def search(all_elements: list, str: str) -> list:
    result = []
    stroke = str.lower()
    for element in all_elements:
        if stroke in element["name"].lower():
            result.append(element)
    return result

def listing(all_elements: list) -> int:
    length = len(all_elements)
    page = 1
    c = 0
    while c!=27: #esc = 27 pgup = 73  pgdown = 81 home = 71 end = 79 insert = 82 R = 114
        if (c == 73) and (page < (length//20+(length%20>0))):
            page += 1
        elif (c == 81) and (page > 1):
            page -= 1
        elif (c == 71):
            page = 1
        elif (c == 79):
            page = length//20+(length%20>0)
        elif (c == 82):
            return 1
        elif (c == 114):
            return 2
        print_elements(all_elements[(page-1)*20:page*20], page)
        c = ord(msvcrt.getch().decode())
    return 0
  
if __name__ == "__main__":
    c = 0
    data = get_elements()
    
    while True:
        mode = listing(data)
        if mode == 1: # search
            os.system("cls")
            print("Enter value: ")
            search_str = input()
            print("\nLoading...")
            listing(search(data, search_str))
        elif mode == 2:
            os.system("cls")
            print("Refreshing...")
            data = get_elements()
        else:
            break