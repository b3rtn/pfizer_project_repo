#author Bertin B. 

import requests
import json
import time
import smtplib
import ssl
from email.message import EmailMessage
from constants import *

class WhoisAPI:
    def __init__(self, domain):
        self.domain = domain
        
    def query_api(self):
        # API request , the API KEY is located in constants.py file 
        print("[+] Querying the API")
        url = f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={API_KEY}&domainName={self.domain}&outputFormat=JSON"
        response = requests.get(url)
        return response.json()

    def parse_data(self, whois_data):
        try:
            print("[+] Parsing the Data")
            # Parsing CreatedDate, UpdatedDate, ExpiresDate
            audit = whois_data['WhoisRecord']['audit']
            created_date = audit.get('createdDate', None)
            updated_date = audit.get('updatedDate', None)
            record = whois_data['WhoisRecord']
            created_date = record.get('createdDate', created_date)
            updated_date = record.get('updatedDate', updated_date)
            expires_date = record.get('expiresDate', None)
            email = record.get('contactEmail', None)
            domain = record.get('domainName', None)
            result = {'domain': domain,'created_date': created_date,'updated_date': updated_date,'expires_date': expires_date,'email': email}
            print(json.dumps(result))
            return result
        except Error as e:
            print("Something wrong")
			
			
class WhoisChangeChecker:
    def __init__(self, domains):
        self.domains = domains
        self.previous_results = None
        
    def check_changes(self):
        #Function to check the changes in While loop  
        print("[+] Checking Changes")
        while True:
            results = []
            for domain in self.domains:
                api = WhoisAPI(domain)
                whois_data = api.query_api()
                result = api.parse_data(whois_data)
                results.append(result)

            if self.previous_results is not None:
                changed_domains = []
                for i, result in enumerate(results):
                    previous_result = self.previous_results[i]
                    if result['created_date'] != previous_result['created_date'] or result['updated_date'] != previous_result['updated_date'] or result['expires_date'] != previous_result['expires_date'] or result['email'] != previous_result['email']:
                        print(f"{result['domain']} CHANGED!")
                        changed_domains.append(result['domain'])
                        
                if changed_domains:
                    # Create JSON file with changed results
                    with open('whois_changes.json', 'w') as f:
                        json.dump(results, f)
                    # Send email with JSON file attached
                    em = EmailMessage()
                    em['From'] = email_sender
                    em['To'] = email_receiver
                    em['Subject'] = subject
                    em.set_content(body)
                    #read the json file 
                    with open('whois_changes.json', 'rb') as f:
                        file_data = f.read()
                        file_name = 'whois_changes.json'
                    em.add_attachment(file_data, maintype='application', subtype='json', filename=file_name)
                    # Add SSL (layer of security)
                    context = ssl.create_default_context()
                    # Log in and send the email
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string())
                        
            self.previous_results = results
            print("[+] Waiting for the next check... go outside")
            # time sleep that defines how much time is going to be checked again 
            time.sleep(30)

checker = WhoisChangeChecker(DOMAINS)
checker.check_changes()
