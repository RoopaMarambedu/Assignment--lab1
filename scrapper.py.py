import requests
from bs4 import BeautifulSoup
import csv
import urllib3
import pandas as pd  

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def scrape_faculty_information(homepage_url):
    faculty_info_list = []

    response = requests.get(homepage_url, verify=False)  
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        faculty_items = soup.select('.row')
        for faculty_item in faculty_items:
            faculty_info = {}

            name_bio_section = faculty_item.select_one('.col-sm-8.right-col')
            faculty_info['name'] = name_bio_section.select_one('.name').text.strip() if name_bio_section and name_bio_section.select_one('.name') else ''
            faculty_info['bio'] = name_bio_section.select_one('.title').text.strip() if name_bio_section and name_bio_section.select_one('.title') else ''
            
            contact_section = faculty_item.select_one('.contact')
            faculty_info['subject'] = contact_section.select_one('.email').text.strip() if contact_section and contact_section.select_one('.email') else ''
            faculty_info['contact'] = contact_section.select_one('.phone').text.strip() if contact_section and contact_section.select_one('.phone') else ''

            faculty_info_list.append(faculty_info)

    return faculty_info_list

# Main function
if __name__ == '__main__':
    homepage_url = 'https://online.pace.edu/graduate-programs/ms-in-computer-science/faculty/'
    faculty_data = scrape_faculty_information(homepage_url)

    csv_filename = 'faculty_info.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Bio', 'Email', 'Contact']  
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for faculty in faculty_data:
            writer.writerow({
                'Name': faculty['name'],
                'Bio': faculty['bio'],
                'Email': faculty['subject'],
                'Contact': faculty['contact']
            })
    df = pd.read_csv(csv_filename)
    df = df.iloc[3:]
    df.to_csv(csv_filename, index=False)

    print(f"Faculty information saved to '{csv_filename}'.")
