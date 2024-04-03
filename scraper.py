import requests
from bs4 import BeautifulSoup
url = 'https://calorienbalans.com/FoodInfo'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
def parse_food_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    food_data = {}

    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if cells:
            food_name = cells[0].text.strip()
            protein = cells[1].text.strip()
            fat = cells[2].text.strip()
            carbohydrate = cells[3].text.strip()
            calories = cells[4].text.strip()
            food_data[food_name] = {
                'protein': protein,
                'fat': fat,
                'carbohydrate': carbohydrate,
                'calories': calories
            }

    return food_data


response = requests.get(url, headers=headers)
html_content = response.content

food_dict = parse_food_data(html_content)
# print(food_dict)
def print_dict(dict):
    for meal,macroses in dict.items():
        print(f"{meal} - protein /{macroses['protein']}/ ;\
               fat /{macroses['fat']}/ ; carbohydrate /{macroses['carbohydrate']}/ ;\
                  calories /{macroses['calories']}/")

# print_dict(food_dict)
        
        