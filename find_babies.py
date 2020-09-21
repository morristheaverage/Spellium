"""Build list of 200 popular names taken from 
https://www.ssa.gov/oact/babynames/decades/century.html
"""

import requests
from bs4 import BeautifulSoup

def main():
    # Get data
    html = requests.get("https://www.ssa.gov/oact/babynames/decades/century.html").text
    soup = BeautifulSoup(html, "html5lib")

    for row in soup("tr")[2:-1]:
        data = row("td")
        print(data[0].text, data[1].text, data[3].text)

if __name__ == "__main__":
    main()
