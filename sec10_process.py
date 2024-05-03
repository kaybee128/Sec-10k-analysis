import re
import unicodedata
from bs4 import BeautifulSoup as bs
import requests


# parse 10K filings to retrieve individual sections
def parse_10k_filing(content, section):

    if section not in [0, 1, 2, 3]:
        print("Not a valid section")
        return

    def get_text(content):
        html = bs(content, "html.parser")
        text = html.get_text()
        text = unicodedata.normalize("NFKD", text).encode('ascii', 'ignore').decode('utf8')
        text = text.split("\n")
        text = " ".join(text)
        return(text)

    def extract_text(text, item_start, item_end):
        item_start = item_start
        item_end = item_end
        starts = [i.start() for i in item_start.finditer(text)]
        ends = [i.start() for i in item_end.finditer(text)]
        positions = list()
        for s in starts:
            control = 0
            for e in ends:
                if control == 0:
                    if s < e:
                        control = 1
                        positions.append([s,e])
        item_length = 0
        item_position = list()
        for p in positions:
            if (p[1]-p[0]) > item_length:
                item_length = p[1]-p[0]
                item_position = p

        item_text = text[item_position[0]:item_position[1]]

        return(item_text)

    text = get_text(content)

    if section == 1 or section == 0:
        try:
            item1_start = re.compile("item\s*[1][\.\;\:\-\_]*\s*\\b", re.IGNORECASE)
            item1_end = re.compile("item\s*1a[\.\;\:\-\_]\s*Risk|item\s*2[\.\,\;\:\-\_]\s*Prop", re.IGNORECASE)
            businessText = extract_text(text, item1_start, item1_end)
        except:
            businessText = "Something went wrong!"

    if section == 2 or section == 0:
        try:
            item1a_start = re.compile("(?<!,\s)item\s*1a[\.\;\:\-\_]\s*Risk", re.IGNORECASE)
            item1a_end = re.compile("item\s*2[\.\;\:\-\_]\s*Prop|item\s*[1][\.\;\:\-\_]*\s*\\b", re.IGNORECASE)
            riskText = extract_text(text, item1a_start, item1a_end)
        except:
            riskText = "Something went wrong!"

    if section == 3 or section == 0:
        try:
            item7_start = re.compile("item\s*[7][\.\;\:\-\_]*\s*\\bM", re.IGNORECASE)
            item7_end = re.compile("item\s*7a[\.\;\:\-\_]\sQuanti|item\s*8[\.\,\;\:\-\_]\s*", re.IGNORECASE)
            mdaText = extract_text(text, item7_start, item7_end)
        except:
            mdaText = "Something went wrong!"

    if section == 0:
        data = [businessText, riskText, mdaText]
    elif section == 1:
        data = [businessText]
    elif section == 2:
        data = [riskText]
    elif section == 3:
        data = [mdaText]
    return(data)



def retrieve_section(html,section):
    res = parse_10k_filing(html, section)[0]
    paragraphs = list(map(lambda s: s.strip(), filter(lambda s: len(s) > 10, res.split('  '))))
    return paragraphs

# take ticket input download 10k file parse in this doc, call openai api to create summary

def analyse_text(text, section, company_name):
    ans= openai.chat.completions.create(
     model="gpt-3.5-turbo",
     messages=[
                        {"role": "system", "content": f"name of the company is {company_name} and use the given data to output an important data regarding {section} of the company. Make the line precise and to the point.Write it in 30 words. "}, #The system instruction tells the bot how it is supposed to behave
                        {"role": "user", "content": f"'{text}'"} #This provides the text to be analyzed.
                    ],
    temperature=0.2, 
    max_tokens=50
    )
    result = ''
    for choice in ans.choices:
        result += choice.message.content
        
    return result


import os

def find_txt_files(folder_path):
    txt_files = []
    # Iterate through all files and directories in the specified folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file has a .txt extension
            if file.endswith('.txt'):
                # Construct the full path of the .txt file
                txt_files.append(os.path.join(root, file))
    return txt_files


# iterates over the txt files to find the correct 10k file for the company
def return_path(ticker):
    folder_path = 'Downloads/'
    txt_files = find_txt_files(folder_path)
    for txt_file in txt_files:
        if(ticker in txt_file):
            return txt_file

from sec_edgar_downloader import Downloader
def download_sec10(ticker):
    dl = Downloader("MyCompanyName", "my.email@domain.com", "Downloads/")
    file= dl.get("10-K", f"{ticker}", limit=1,download_details=False)
    x= open(return_path(ticker),"r")
    html = x.read()
    return html

def get_section_name(number):
    section_names = {1: "business", 2: "risk", 3: "MDA"}
    return section_names.get(number, "Unknown")


import openai
from openai import OpenAI
OPENAI_API_KEY="sk-proj-**********"
openai.api_key=OPENAI_API_KEY


# MAIN LOOP IT FIRSTS DOWNLOADS THE SEC 10K FILING, 
# RETRIEVE SECTIONS WHICH IS NEEDED
# ANALYSES THE TEXT AND RETURNS INSIGHTS


def find_insights(ticker, number):
    text_file=download_sec10(ticker)
    section=retrieve_section(text_file,number)
    text= analyse_text(section,get_section_name(number),ticker)
    return text

# find_insights("MSFT",2)


