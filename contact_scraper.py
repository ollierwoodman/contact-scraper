#!/usr/bin/env python
import grequests
from bs4 import BeautifulSoup
import csv
import re
import json
from urllib.parse import urlparse, unquote
import sys

def is_valid_url(string):
  try:
    result = urlparse(string)
    return all([result.scheme, result.netloc])
  except:
    return False
def is_valid_email_address(string):
  email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
  return email_pattern.fullmatch(string) != None

def is_valid_phone_number(string):
  #TODO
  return True

def deduplicate_list_preserve_order(seq):
  return list(dict.fromkeys(seq))

def extract_email_address(soup):
  # Find all 'mailto:' links
  anchors_with_mailto_links = soup.find_all('a', href=re.compile(r'^mailto:'))

  # Extract email addresses from 'mailto:' links
  email_addresses = []
  for anchor in anchors_with_mailto_links:
    mailto_link = anchor['href']
    parsed_link = urlparse(mailto_link, "mailto")
    
    email = parsed_link.path
    email = unquote(email)
    email = email.strip()
    
    if is_valid_email_address(email):
      email_addresses.append(email)

  return deduplicate_list_preserve_order(email_addresses)

def extract_phone_numbers(soup):
  # Find all 'mailto:' links
  anchors_with_mailto_links = soup.find_all('a', href=re.compile(r'^tel:'))

  # Extract email addresses from 'mailto:' links
  phone_numbers = []
  for anchor in anchors_with_mailto_links:
    mailto_link = anchor['href']
    parsed_link = urlparse(mailto_link, "tel")
    
    phone = parsed_link.path
    phone = phone.strip()
    
    if is_valid_phone_number(phone):
      phone_numbers.append(phone)

  return deduplicate_list_preserve_order(phone_numbers)

def scrape_contacts_from_urls(urls):
  requests = (grequests.get(u) for u in urls)

  contacts = []
  for response in grequests.imap(requests, size=10):
    soup = BeautifulSoup(response.content, 'html.parser')
    
    email_addresses = extract_email_address(soup)
    phone_numbers = extract_phone_numbers(soup)
    
    contacts.append({
      "title":  soup.title.string,
      "source": response.url,
      "emails": email_addresses,
      "phones": phone_numbers,
    })

  return contacts

def write_contacts_to_csv(contacts, filename):
  with open(filename, 'w+') as f:
    fieldnames = [
      'Title', 
      'Source', 
      'Email', 
      'Phone'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n', delimiter=',')
    writer.writeheader()

    for id, contact in enumerate(contacts):
      writer.writerow({
        'Title': contact['title'], 
        'Source': contact['source'], 
        'Email': contact['emails'][0] if contact['emails'] else "", 
        'Phone': contact['phones'][0] if contact['phones'] else "", 
      })

if __name__ == '__main__':
  import argparse
  
  parser = argparse.ArgumentParser()
  parser.add_argument("urls", nargs='+', type=str, help="URL or URLs to scrape from")
  parser.add_argument("-o", "--out", type=str, help="path to file where scraped data is saved, supports json and csv")
  args = parser.parse_args()
  
  contacts = scrape_contacts_from_urls(args.urls)
  
  if not args.out:
    print(json.dumps(contacts, indent=2))
    
  with open(args.out, 'w+') as f:
    if args.out.endswith('.json'):
      json.dump(contacts, f, indent=2)
    elif args.out.endswith('.csv'):
      write_contacts_to_csv(contacts, args.out)