from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://platum.kr/archives/224218', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
og_image = soup.select_one('meta[property="og:image"]')
og_title = soup.select_one('meta[property="og:title"]')
og_desc = soup.select_one('meta[property="og:description"]')

print(og_image)
img = og_image['content']
print(img)
print(og_image.isalnum())