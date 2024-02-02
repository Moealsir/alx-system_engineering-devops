from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

import re
import os
import time
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from getpass import getpass
from email_validator import validate_email, EmailNotValidError


css_styles = {
    'panel': '\033[1;48;2;255;255;255;38;2;0;0;0m',
    'title': '\033[38;2;0;0;255m\033[1m',
    'code': '\033[38;2;255;0;0m',
    'name': '\033[38;2;219;62;62m',
    'progress': '\033[38;2;152;163;174m',
    'optional': '\033[38;2;152;163;174m',
    'start': '\033[1m\033[38;2;52;152;219m',
    'end': '\033[1m\033[38;2;52;152;219m',
    'left': '\033[1m',
    'link': '\033[1m\033[38;2;52;152;219m'
}

def apply_style(text, style_key):
    return css_styles.get(style_key, '') + text + '\033[0m'

def user_data():
    global email, password

    # Check if user data file exists
    user_data_file = os.path.expanduser("~/.alx_user_data")
    if os.path.exists(user_data_file):
        with open(user_data_file, "r") as file:
            for line in file:
                if line.startswith('PROJECT_REMINDER_EMAIL='):
                    email = line.split('"')[1]
                elif line.startswith('PROJECT_REMINDER_PASSWORD='):
                    password = line.split('"')[1]
    else:
        while True:
            email_input = input("Enter your email: ")
            try:
                v = validate_email(email_input)
                break
            except EmailNotValidError as e:
                print(f"Error: {str(e)}. Please enter a valid email.")

        password_input = getpass("Enter your password: ")

        with open(user_data_file, "w") as file:
            file.write(f'PROJECT_REMINDER_EMAIL="{email_input}"\n')
            file.write(f'PROJECT_REMINDER_PASSWORD="{password_input}"\n')

        email = email_input
        password = password_input

    print("Please wait...")
    return email, password

def login(email, password):
    global driver

    login_url = "https://intranet.alxswe.com/auth/sign_in"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)

    try:
        driver.get(login_url)

        email_field = driver.find_element(By.CSS_SELECTOR, 'input[name="user[email]"]')
        email_field.send_keys(email)

        password_field = driver.find_element(By.CSS_SELECTOR, 'input[name="user[password]"]')
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(5)

        print("Login successful.")
        os.system('clear')
    except Exception as e:
        print(f"Can't log in. Error: {str(e)}")

def extract_panels(driver):
    global panels
    target_url = "https://intranet.alxswe.com"

    try:
        driver.get(target_url)
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        page = soup.find('div', class_="col-md-6")

        if page:
            # Filter out the unwanted panel
            unwanted_panel = page.find('div', class_="panel panel-default events-card")
            if unwanted_panel:
                unwanted_panel.decompose()  # Remove the unwanted panel from the page

            panels = page.find_all('div', class_="panel panel-default")

            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(str(page))  # Write the content of the 'page' variable to the file

            # print(panels)
            return panels
        else:
            print("Error: Unable to find the target page.")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def extract_future_projects(panel):
    future_projects = []
    title = panel.find('h3', class_='panel-title').text.strip()

    if 'Future team projects' in title:
        projects = panel.find_all('li', class_='list-group-item')

        for project in projects:
            code = project.find('code').text.strip()
            name = project.find('a').text.strip()
            start_time = project.find('div', class_='d-inline-block').find('span', class_='datetime').text
            # print(start_time)
            link = "https://intranet.alxswe.com" + project.find('a')['href'].strip()

            project_info = {
                'code': code,
                'name': name,
                'start_time': start_time,
                'link': link
            }

            future_projects.append(project_info)

    return future_projects



def extract_current_projects(panel):
    current_projects = []
    title = panel.find('h3', class_='panel-title').text.strip()

    if 'Current projects' in title:
        projects = panel.find_all('li', class_='list-group-item')

        for project in projects:
            deadline_class_type = project.get('class')

            if 'in_second_deadline' in deadline_class_type:
                deadline_type = '2ND'
            else:
                deadline_type = '1ST'

            code = project.find('code').text.strip()
            name = project.find('a').text.strip()
            optional = 'Optional' if project.find('span', class_='alert alert-info bpi-advanced') else ''
            progress_element = project.find('div', class_='project_progress_percentage alert alert-info')
            progress = progress_element.text.strip() if progress_element else "Progress not available"
            start_time_element = project.find('div', class_='d-inline-block').find('span', class_='datetime')
            # print(start_time_element)
            start_time = start_time_element.text if start_time_element else None

            # Handling the absence of 'data-react-props'
            deadline_element = start_time_element.find_next('div', class_='d-inline-block').find('span', class_='datetime')
            deadline = deadline_element.text if deadline_element else None

            time_left_match = re.search(r'\((.*?)\)', project.strong.text)
            time_left_ = time_left_match.group(1) if time_left_match else ''
            time_left = f'({time_left_})'
            link = "https://intranet.alxswe.com" + project.find('a')['href'].strip()

            project_info = {
                'code': code,
                'name': name,
                'optional': optional,
                'progress': progress,
                'start_time': start_time,
                'deadline': deadline,
                'time_left': time_left,
                'link': link
            }

            current_projects.append(project_info)

    return current_projects



def extract_datetime_from_element(element):
    if element:
        props_str = element.get('data-react-props', '')

        if props_str:
            try:
                props_dict = json.loads(props_str)
                return datetime.fromisoformat(props_dict.get('value', ''))
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {props_str}")
                return None
        else:
            return None
    else:
        return None


def extract_datetime_from_react_props(props_str):
    props_str = props_str.replace("'", '"')
    props_dict = json.loads(props_str)
    return datetime.fromisoformat(props_dict['value'])


def extracting_details(panels):
    for panel in panels:
        future_projects = extract_future_projects(panel)
        current_projects = extract_current_projects(panel)

        if future_projects:
            print(apply_style("Future Projects:", 'title'))
            for project in future_projects:
                code = apply_style(project['code'], 'code')
                name = apply_style(project['name'], 'name')
                start_time = apply_style(project['start_time'], 'start')
                link = apply_style(project['link'], 'link')

                print(f"{code} {name}\nStart Time: {start_time}\nLink: {link}")
            print()

        if current_projects:
            print(apply_style("Current Projects:", 'title'))
            for project in current_projects:
                code = apply_style(project['code'], 'code')
                name = apply_style(project['name'], 'name')
                optional = apply_style(project['optional'], 'optional')
                progress = apply_style(project['progress'], 'progress')
                start_time = apply_style(project['start_time'], 'start')
                deadline = apply_style(project['deadline'], 'end')
                time_left = apply_style(project['time_left'], 'optional')
                link = apply_style(project['link'], 'link')

                print(f"{code} {name} {optional}{progress}\n"
                      f"Start Time: {start_time}       Deadline: {deadline}\nTime Left: {time_left} \nLink: {link}")
            print()



def main():
    email, password = user_data()
    login(email, password)
    driver.refresh()
    panels = extract_panels(driver)

    extracting_details(panels)


if __name__ == "__main__":
    main()
