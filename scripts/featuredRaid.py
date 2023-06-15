import requests
import datetime
import bs4
import calendar

today = datetime.datetime.now().date()
raid_rotation = {}
raid_challenges = {}

#extracts data from source
def grab_content():
    site = "https://www.shacknews.com/article/130769/destiny-2-featured-raid-rotator-schedule"
    data = requests.get(site).content
    scraper = bs4.BeautifulSoup(data,'lxml')
    return scraper

#scans the raids that are in current rotation
def scrape_raid():
    scraper = grab_content()
    dateTable = scraper.find_all('tr')
    for index,value in enumerate(dateTable):
        if index > 1:
            mainContent = value.text.split('\n')
            date = mainContent[1]
            raid_name = mainContent[2]
            raid_rotation[date] = raid_name
    return raid_rotation

#extracts the challenges of each raid
def scrape_challenges():
    raid_info = scrape_raid()
    scraper = grab_content()
    challenges_section = scraper.find_all('ul')
    for index, value in enumerate(challenges_section):
        if "challenge" in value.text:
            internalScraper = bs4.BeautifulSoup(str(value), "lxml")
            challenge_link = internalScraper.find_all("a")
            for i in challenge_link:
                if "raid" in i["href"]:
                    challenge_url = i["href"]
                    for date, raid_name in raid_info.items():
                        if raid_name.lower() in challenge_url.lower() or raid_name.lower().replace(" ", "-") in challenge_url.lower():
                            if raid_name not in raid_challenges:
                                raid_challenges[raid_name] = []
                            raid_challenges[raid_name].append(challenge_url)
    return raid_challenges

scrape_raid()
# print(raid_rotation)
scrape_challenges()
theMonth = calendar.month(theyear=today.year,themonth=today.month)
thisMonth = theMonth.split()[0]
theWeek = theMonth.split('\n')
for i in range(len(theWeek)):
    if (str(today.day)) in theWeek[i]:
        found_week = i

for i in theWeek[found_week].split():
    for key,value in raid_rotation.items():
        if (f"{thisMonth} {i}") in key:
            featured_raid = raid_rotation[key]
            print("This weeks featured raid is",featured_raid)
            print("The challenges are: ")

#prevents duplicates from being displayed
used_challenges = []
for i in (raid_challenges[featured_raid]):
    if i not in used_challenges:
        used_challenges.append(i)
        print(i)


