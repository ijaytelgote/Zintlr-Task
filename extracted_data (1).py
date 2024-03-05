import requests
from bs4 import BeautifulSoup
import json

class ProfileScraper:
    def __init__(self, html_content):
        """
        Initialized the ProfileScraper object with the provided HTML content.
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')  # Created a BeautifulSoup object
        self.profile_data = {}  # Initialized an empty dictionary to store profile data

    def extract_full_name(self):
        """
        Extracted full name from the HTML content.
        """
        full_name_tag = self.soup.find('div', class_='name')  # Found the tag containing the full name
        if full_name_tag:
            full_name = full_name_tag.text.strip()  # Got the text content and removed leading/trailing whitespace
            self.profile_data['full_name'] = full_name  # Added full name to profile data dictionary
            self.profile_data['first_name'], self.profile_data['last_name'] = full_name.split(maxsplit=1)  # Split full name into first and last names

    def extract_industry(self):
        """
        Extracted industry information from the HTML content.
        """
        industry_tag = self.soup.find('div', class_='OesXg')  # Found the tag containing industry information
        if industry_tag:
            self.profile_data['industry'] = industry_tag.text.strip()  # Added industry information to profile data dictionary

    def extract_annual_salary(self):
        """
        Extracted annual salary information from the HTML content.
        """
        salary_element = self.soup.find('div', class_='vOrcj')  # Found the element containing annual salary
        if salary_element:
            self.profile_data['annual_salary'] = salary_element.text.strip()  # Added annual salary to profile data dictionary

    def extract_education(self):
        """
        Extracted education information from the HTML content.
        """
        education_elements = self.soup.find_all('div', class_='edu-label')  # Found all education elements
        education_info = []

        for edu_element in education_elements:
            education_dict = {}
            degree_year = edu_element.find('div', class_='desig').text.strip()  # Extracted degree and year
            education_dict['degree'] = degree_year.split(',')[0].strip()
            education_dict['major'] = degree_year.split(',')[1].strip()
            education_dict['year'] = degree_year.split(',')[2].strip()
            institute = edu_element.find('span', class_='hlite-inherit').text.strip()  # Extracted institute name
            education_dict['institute'] = institute
            education_info.append(education_dict)

        self.profile_data['education'] = education_info  # Added education information to profile data dictionary

    def extract_work_experience(self):
        """
        Extracted work experience information from the HTML content.
        """
        work_experience_section = self.soup.find('div', class_='work-exp')
        work_experience = []

        if work_experience_section:
            work_exp_cards = work_experience_section.find_all('div', class_='work-exp-card')
            for card in work_exp_cards:
                exp_head = card.find('div', class_='exp-head')
                if exp_head:
                    exp_icon = exp_head.find('div', class_='exp-icon')
                    if exp_icon:
                        exp_img = exp_icon.find('img')
                        if exp_img:
                            company_logo_url = exp_img.get('data-src', '')
                            company_name = exp_img.get('alt', '')
                    exp_label = exp_head.find('div', class_='exp-label')
                    if exp_label:
                        desig = exp_label.find('div', class_='desig').text.strip()
                        dates = exp_label.find('div', class_='dates').text.strip()
                    desc = card.find('div', class_='desc').text.strip()
                    work_experience.append({
                        'company_logo_url': company_logo_url,
                        'company_name': company_name,
                        'designation': desig,
                        'dates': dates,
                        'description': desc
                    })

        self.profile_data['work_experience'] = work_experience

    def extract_skills(self):
        """
        Extracted skills information from the HTML content.
        """
        skills_elements = self.soup.find_all('div', class_='skills')
        if skills_elements:
            skills = [item.text.strip() for item in skills_elements]
            self.profile_data['skills'] = skills

    def extract_work_summary(self):
        """
        Extracted work summary information from the HTML content.
        """
        work_summary_section = self.soup.find('div', class_='_2NDnc')
        work_summary = ''

        if work_summary_section:
            work_summary = work_summary_section.find('div', class_='Ju-0N').text.strip()

        self.profile_data['work_summary'] = work_summary

    def extract_it_skills(self):
        """
        Extracted IT skills information from the HTML content.
        """
        it_skills_section = self.soup.find('div', class_='cv-prev-it-skills')
        it_skills_info = []

        if it_skills_section:
            it_skills_rows = it_skills_section.find_all('div', class_='table-tuple')

            for row in it_skills_rows:
                skill_elem = row.find('div', class_='data-cell skills')
                version_elem = row.find('div', class_='data-cell version')
                last_used_elem = row.find('div', class_='data-cell lastUsed')
                exp_elem = row.find('div', class_='data-cell exp')

                if skill_elem and version_elem and last_used_elem and exp_elem:
                    skill = skill_elem.text.strip()
                    version = version_elem.text.strip()
                    last_used = last_used_elem.text.strip()
                    experience = exp_elem.text.strip()

                    it_skill_data = {
                        'skill': skill,
                        'version': version,
                        'last_used': last_used,
                        'experience': experience
                    }

                    it_skills_info.append(it_skill_data)

        self.profile_data['it_skills'] = it_skills_info

    def extract_other_details(self):
        """
        Extracted other details such as languages known, personal details, and desired job details from the HTML content.
        """
        other_details_section = self.soup.find('div', class_='YQo1I')
        other_details = {}

        if other_details_section:
            languages_known = {}
            languages_section = other_details_section.find('div', class_='_88wuB')
            if languages_section:
                languages_items = languages_section.find_all('div', class_='_9FKxR')
                for item in languages_items:
                    language_name = item.text.strip().split(' - ')[0]
                    proficiency = item.find('span', class_='_5F2Uo').text.strip()
                    languages_known[language_name] = proficiency
            other_details['languages_known'] = languages_known

            personal_details = {}
            personal_details_section = other_details_section.find('div', class_='nqhGZ')
            if personal_details_section:
                personal_info_rows = personal_details_section.find_all('div', class_='tr')
                for row in personal_info_rows:
                    details = row.find_all('div', class_='table-cell')
                    if len(details) == 2:
                        key = details[0].text.strip()
                        value = details[1].text.strip()
                        personal_details[key] = value
            other_details['personal_details'] = personal_details

            desired_job_details = {}
            desired_job_section = other_details_section.find('div', class_='hmFnB')
            if desired_job_section:
                job_info_rows = desired_job_section.find_all('div', class_='tr')
                for row in job_info_rows:
                    details = row.find_all('div', class_='table-cell')
                    if len(details) == 2:
                        key = details[0].text.strip()
                        value = details[1].text.strip()
                        desired_job_details[key] = value
            other_details['desired_job_details'] = desired_job_details

        self.profile_data['other_details'] = other_details

    def scrape_profile(self):
        """
        Scraped profile information using all extraction methods.
        """
        self.extract_full_name()
        self.extract_industry()
        self.extract_annual_salary()
        self.extract_education()
        self.extract_work_experience()
        self.extract_skills()
        self.extract_work_summary()
        self.extract_it_skills()
        self.extract_other_details()

        return self.profile_data

def main():
    with open(r"C:\Users\jayma\Downloads\Naukri Sample HTML 1.txt", 'r') as file:
        raw_html = file.read()  # Read HTML content from file

    # Initialized ProfileScraper object with HTML content
    scraper = ProfileScraper(raw_html)

    # Scraped profile information
    profile_data = scraper.scrape_profile()

    # Converted dictionary to JSON format
    json_data = json.dumps(profile_data, indent=4)  # Converted dictionary to JSON string with indentation
    print(json_data)  # Printed JSON data

# Executed main function if the script was run directly
if __name__ == "__main__":
    main()




 
    '''
List of approaches, techniques, and packages used in the code:

Object-Oriented Programming (OOP) Technique
   - The code uses the object-oriented programming (OOP) paradigm to encapsulate related functionality within classes (`ProfileScraper`).
   - Methods are defined within the class to perform specific tasks related to profile scraping.

HTML Parsing Techniqu
   - The code uses BeautifulSoup, a Python library, for parsing HTML documents (`BeautifulSoup`).
   - BeautifulSoup is used to navigate and search through the HTML content to locate specific elements containing the desired information.

Data Extraction Technique
   - The code utilizes various data extraction techniques to extract specific pieces of information from the HTML content.
   - These techniques include finding elements by class name (`find` and `find_all` methods) and extracting text content (`text` attribute).

Data Storage Technique
   - The extracted profile data is stored in a dictionary (`profile_data`) within the `ProfileScraper` class.
   - The dictionary structure allows for easy organization and retrieval of profile information.

JSON Serialization Technique
   - The code uses the `json` package to serialize the extracted profile data into JSON format.
   - JSON serialization allows for easy storage, transmission, and interchange of data in a structured format.

HTTP Request Technique
   - Although not explicitly shown in the provided code, web scraping often involves making HTTP requests to fetch HTML content from web pages.
   - The `requests` library is commonly used for making HTTP requests in Python.

File I/O Technique
   - The code reads HTML content from a file using file input/output operations (`open` function).
   - This allows for scraping data from locally stored HTML files.

Printing Technique
   - The extracted profile data in JSON format is printed to the console using the `print` function.

Package Used
    - `requests`: Used for making HTTP requests to fetch HTML content from web pages.
    - `BeautifulSoup`: Used for parsing HTML documents and navigating the HTML tree structure to extract specific elements.
    - `json`: Used for serializing Python objects (in this case, the profile data dictionary) into JSON format.
'''