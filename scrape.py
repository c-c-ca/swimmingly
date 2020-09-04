from bs4 import BeautifulSoup
import re
import pprint


def convert(t):
    m, s, h = re.search("(\d+)?:?(\d\d).(\d\d)", t).groups()
    m = m or 0
    return int(m) * 60 * 1000 + int(s) * 1000 + int(h) * 10


times = []
with open("index.html", "r") as f:
    soup = BeautifulSoup(f.read(), "lxml")
    table_data = soup.find("table").tbody.find_all("tr")
    for tr in table_data:
        tds = tr.find_all("td")
        if tds:
            times.append([convert(td.text) for td in tds])

with open("times.txt", "w") as f:
    pprint.pprint(times, stream=f)
