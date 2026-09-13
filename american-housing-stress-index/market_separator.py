from bs4 import BeautifulSoup

def innerHTML(element):
    return element.encode_contents()

with open("./resources/markets.html", 'r') as doc:
    soup = BeautifulSoup(doc, "html.parser")
    my_list = soup.find_all('a')
    for x in my_list:
        firstsplit = (str(innerHTML(x)).split('>'))
        print(firstsplit[1].split('<')[0])
    # print(my_list)

