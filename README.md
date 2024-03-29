# Contact Scraper

A simple pair of scripts to help the user to scrape a large amount of contact info from a website in relatively little time

1. `contact_scraper.py`: scrape all the email addresses and phone numbers from a list of URLs (such as the ones collected with the below script)

2. `get_all_links_console_function.js`: collect a list of URLs from a webpage

Email address and phone numbers are scraped by searching each webpage for `mailto` and `tel` links inside anchor tags. Such tags could look like the two examples below:

```html
<a href="tel:555-1234">Call us</a>
<a href="mailto:ollie@example.com">Email us</a>
```

## `contact_scraper.py`

### Features

* Extracts emails and phone numbers from web pages.
* Handles multiple URLs concurrently.
* Supports output as JSON or CSV.
* Validates extracted email addresses.

### Usage

1. Install required libraries:

   ```bash
   pip install beautifulsoup4 grequests grequests urllib3
   ```

2. Run the script:

   ```bash
   python scrape_contacts.py [-o] <URL1> <URL2> ...
   ```
  
   * Replace `<URL1>`, `<URL2>`, ... with the URLs you want to scrape.
   * Use `-o <OUTPUT_FILE>` to specify the output file.
      * If the file extension is `.json`, the output will be JSON.
      * If the file extension is `.csv`, the output will be CSV. Please note that only the first email address and phone number scraped from each page will be saved to CSV, to store all data scraped use a JSON file.
      * If no output file is specified, the results will be pretty printed to the console as JSON.

### Example

```bash
python scrape_contacts.py https://example.com https://another.com -o contacts.json
```

This will extract contact information from both URLs and save it to the file `contacts.csv`.

### Limitations

* The script currently does not validate phone numbers. This functionality is marked as TODO and needs to be implemented.
* The script does not perform cross-page deduplication (i.e. no checking for contact info that appears across multiple pages)

## `get_all_links_console_function.js`

### Features

* Collect a list of URLs from a webpage.
* Deduplicate the links collected.
* Out the links as a string with a custom separator.

### Usage

Copy and paste this file's contents into your browsers console and call the `scapeLinks()` function with appropriate parameters to scrape all the links from the current webpage.