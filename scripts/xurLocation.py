import requests
import bs4

site = "https://whereisxur.com"
content = requests.get(site).content
data = bs4.BeautifulSoup(content,'lxml')
location = data.find("h4",{"class":"title"})
inventory = [i.text for i in data.find_all("h4",{"class":"et_pb_module_header"})]
print(f"\n{location.text}")

print("\nXur's Inventory: ")
for index, value in enumerate(inventory):
    print(index+1,value)