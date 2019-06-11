from bs4 import BeautifulSoup
import requests
from os import path, mkdir
import random
from time import sleep
import json
import html

LINK = "https://www.washington.edu/students/timeschd/AUT2019/"

def main():
    schedule = {}
    content = requests.get(LINK).content
    soup = BeautifulSoup(content, "html.parser")
    items = soup.find_all("li")
    for item in items:
        link = item.find_all("a", href=True)
        if len(link) > 0:
            title = link[0].text
            href = link[0]['href']
            if 'http' not in href and '#' not in href and '--' not in title:
                page_link = LINK + href
                courses = scrape_one_page(LINK + href)
                schedule[title] = courses
                print("done with " + title)
                sleep(1)
    with open("schedule.json", 'w') as file:
        file.write(json.dumps(schedule, indent=4, sort_keys=True))
    print("done!")

def scrape_one_page(link):
    classes = []
    sections = []
    course = ""
    page_response = requests.get(link, timeout=5)
    soup = BeautifulSoup(page_response.content, "html.parser")
    courses = soup.find_all("table")
    counter = 0
    for table in courses[3:]:
        pre = table.find("pre")
        if pre is None:
            if counter != 0:
                class_obj = {
                    'course': course,
                    'sections': sections
                }
                classes.append(class_obj)
            course_text = html.unescape(table.text)
            course_text = course_text.replace("Prerequisites", '')
            # for char in course_text:
            #     if not char.isalpha():
            #         course_text.replace(char, '')
            course_text = course_text.replace('\u00a0', '')
            course = course_text.strip()
            sections = []
            counter += 1
        else:
            options = html.unescape(pre.text).split()
            if options[0] == "Restr" or options[0] == "IS":
                options = options[1:]
            sln = options[0].replace(">", '')
            section_code = options[1]
            credit_or_type = options[2]
            days = options[3]
            times = options[4]
            hall = options[5]
            room = options[6]
            section = {
                'sln': sln,
                'section_code': section_code,
                'credit_or_type': credit_or_type,
                'days': days,
                'times': times,
                'hall': hall,
                'room': room
            }
            sections.append(section)
    return classes

# Restr (skip) SLN SECTION (time area)  HALL ROOM# Instructor(opt)

if __name__ == '__main__':
    main()