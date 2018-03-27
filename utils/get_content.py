import BeautifulSoup as bs
import requests
def get_content():
    url='https://www.wenku1.com/list/%E5%A4%A7%E5%AD%A6%E7%94%9F%E8%8A%82%E8%83%BD%E5%87%8F%E6%8E%92%E6%96%87%E7%AB%A0/'
    re=requests.get(url=url)
    print(re.text)

    s=bs.BeautifulSoup(re.text,'html.parser')
    s.findAll('fieldset')
    print(s)
get_content()