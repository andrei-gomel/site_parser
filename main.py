from bs4 import BeautifulSoup
from datetime import date, datetime
import requests

st_accept = "text/html" # говорим веб-серверу, 
                        # что хотим получить html
# имитируем подключение через браузер Mozilla на macOS
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"

# Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
# формируем хеш заголовков
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}

vacansi = 'программист'
res = requests.get(f'https://belmeta.com/vacansii?q={vacansi}&df=3&sort=date')

page = BeautifulSoup(res.text, 'html.parser')
# print(page.prettify())
jobs = page.find_all(class_="job no-logo")

results = []

for item in jobs:
	# print(item)
	vacansi = item.find(class_="job-title").get_text()
	print('Вакансия: ' + item.find(class_="job-title").get_text())
	company = item.find(class_="job-data company").get_text()
	print('Кампания: ' + item.find(class_="job-data company").get_text())

	city = item.find(class_="job-data region").get_text(strip=True) if item.find(class_="job-data region") is not None else ""
	if city:
		print('Город: ' + city)

	sal = item.find(class_="job-data salary").get_text() if item.find(class_="job-data salary") is not None else ""
	if sal:
		print('Зарплата: ' + sal)
	link = str(item.a.get('href'))
	print('Ссылка: ' + 'https://belmeta.com' + str(item.a.get('href')))
	print('\n####################\n')

	results.append({
		'vacansi': vacansi,
		'company': company,
		'city': city,
		'sal': sal,
		'link': link,
		})


f = open('vacansi.txt', 'w', encoding='utf-8')

for item in results:
	f.write(f'Вакансия: {item["vacansi"]}\nКампания: {item["company"]}\nГород: {item["city"]}\n')
	if item["sal"]:
		f.write(f'{item["sal"]}\n')
	f.write(f'Ссылка: https://belmeta.com{item["link"]}\n\n####################\n\n')


now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#today = date.today()
f.write(f'Создано: {dt_string}')
f.close()
print(f'Создано: {dt_string}')