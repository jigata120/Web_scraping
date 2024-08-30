from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://github.com/')

try:
    WebDriverWait(driver, 60).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    page_source = driver.page_source
except TimeoutException:
    print("Timeout: Element or page not loaded in time")
    page_source = driver.page_source
finally:
    driver.quit()

soup = BeautifulSoup(page_source, 'html.parser')

def get_element_level(tag_name):
    tag_levels = {
        'h1': 1, 'h2': 2, 'h3': 3, 'h4': 4, 'h5': 5, 'h6': 6,
        'div': 7, 'span': 8, 'p': 9, 'ul': 10, 'ol': 11, 'li': 12
    }
    return tag_levels.get(tag_name, 13)

def extract_content(element):
    content = []

    for tag in element.find_all(recursive=False):
        level = get_element_level(tag.name)

        if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'span', 'p']:
            section = {
                "title": tag.get_text(strip=True),
                "text": "",
                "children": [],
                "level": level
            }
            if tag.find_all():
                section["children"] = extract_content(tag)
            content.append(section)
        elif tag.name in ['ul', 'ol']:
            list_type = 'unordered' if tag.name == 'ul' else 'ordered'
            list_items = []
            for li in tag.find_all('li', recursive=False):
                list_items.append({
                    "title": li.get_text(strip=True),
                    "text": "",
                    "children": [],
                    "level": level + 1
                })
            content.append({
                "title": list_type,
                "text": "",
                "children": list_items,
                "level": level
            })

    return content

def build_hierarchy(elements):
    stack = []
    root = []

    for element in elements:
        while stack and stack[-1]["level"] >= element["level"]:
            stack.pop()
        if stack:
            stack[-1]["children"].append(element)
        else:
            root.append(element)
        stack.append(element)

    return root

def parse_content(soup):
    data = {
        "objects": []
    }

    content = extract_content(soup.body)

    hierarchical_data = build_hierarchy(content)

    data["objects"] = hierarchical_data

    return data

data = parse_content(soup)

json_data = json.dumps(data, indent=4)

with open('website_data.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

print("Data extracted and saved to website_data.json")
