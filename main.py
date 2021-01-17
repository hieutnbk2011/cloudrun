import os
import re
from flask import Flask
from unidecode import unidecode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
from lxml.etree import tostring
import html as html_parser
import json
import classifier
app = Flask(__name__)
driver = None

def set_driver():        
    global driver
    if not driver:
        # initialize options
        options = webdriver.ChromeOptions()
        # pass in headless argument to options
        # options.add_argument('--headless')
        prefs = {"profile.managed_default_content_settings.images":2}
        options.add_experimental_option("prefs",prefs)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("window-size=1024,768")
        options.add_argument("--no-sandbox")
        # initialize driver
        driver = webdriver.Chrome(os.path.join(os.getcwd(), "chromedriver"), options=options)
    return driver


def get_text(full_html):
    #We only want text blocks that has actual text in it
    lines_w_text = []
    text_stripped = ''
    lines = full_html.xpath("//*[@id='sq_news_body']//p[position()>1]")
    TAG_RE = re.compile(r'<[^>]+>')
    #TODO : finish this off
    for line in lines:     #should return a list of text bocks we want (may only return one big block)
        # remove tailing line chars if any
        tail = line.tail if line.tail and line.tail != " " else ""
        tail = tail if tail != "" else ""
        html = unidecode(html_parser.unescape(tostring(line).decode("utf-8").replace(tail, "")))
        text = TAG_RE.sub('', html).strip()
        
        if text:                
            proper_text = unidecode(text.strip())
            lines_w_text.append(html)
            text_stripped += " " + proper_text

    return lines_w_text   

@app.route("/")
def handle():
    global driver
    print("Setting up selenium")
    driver = set_driver()
    print("Fetching from url")
    driver.get("https://www.waverley.nsw.gov.au/top_link_pages/news_and_media/council_news/news/a_message_from_the_mayor_this_festive_season")
    page_html = driver.page_source
    tree = etree.HTML(page_html)
    text= get_text(tree)
    print("Fetching tags")
    tags = classifier.tag(text)
    print(tags)
    return json.dumps(tags)


