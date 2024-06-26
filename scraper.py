import requests
from bs4 import BeautifulSoup

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

url = 'https://calorienbalans.com/FoodInfo'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

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


def optimal_protein(data):
    foods_optimal = {}
    for meal,macroses in data.items():
        if macroses['protein'] and macroses['calories']:
            if float(macroses['protein'])*20>int(macroses['calories']):
                foods_optimal[meal] = food_dict[meal]
                
    # print_dict(foods_optimal)

optimal_protein(food_dict)


def generate_html_table(food_dict):
    html_content = '''<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Document</title>
                        </head>
                        <body><table border="1">\n'''

    html_content += '<tr><th>Food Name</th><th>Protein</th><th>Fat</th><th>Carbohydrate</th><th>Calories</th></tr>\n'
    js = get_the_js('screpeDisplay.js')
    for food_name, data in food_dict.items():
        html_content += f'<tr><td>{food_name}</td><td>{data["protein"]}</td>\
            <td>{data["fat"]}</td><td>{data["carbohydrate"]}</td><td>{data["calories"]}</td></tr>\n'
    
    html_content += f'</table>\n<script>{js}</script>\n</body></html>'
    
    return html_content

def get_the_js(filename):
    try:
        with open(filename, 'r') as file:
            file_text = file.read()
            return file_text
    except FileNotFoundError:
        print("The file '{}' does not exist.".format(filename))
    
print()


def save_html_file(html_content, filename):
    with open(filename, 'w',encoding='utf-8') as file:
        file.write(html_content)

#save the html content to a file
html_table = generate_html_table(food_dict)
# print(html_table)
save_html_file(html_table, 'index.html')

#start a simple http server
import http.server
import socketserver
#change the port each time 
PORT = 8070

def print_link(message, url):
    print(f"\033]8;;{url}\033\\{message}\033]8;;\033\\")

# link for usage(change the port each time):
print_link("Click here to visit the website", f"http://localhost:{PORT}/index.html")
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
