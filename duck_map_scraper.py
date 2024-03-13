import json
import datetime
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv

# Define the search queries
beginning_query = "Text_Before_Keyword_"
end_query = "Text_After_Keyword_"

def read_keywords_from_json(json_file):
    keywords = []
    with open(json_file, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            keywords.append(data['keyword'])
    return keywords

def scrape_duckduckgo(beginning_query, end_query):
    # Print initial timestamp
    print(f"{datetime.datetime.now()} - Initiating script")

    # Generate the output filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"duckduckgo_maps_scraper_output_{timestamp}.csv"
    debug_log_filename = f"debug_log_{timestamp}.html"
    save_path = f"C:/Users/USER/Desktop/Code/scanners/duckduckgo_maps_scraper/{output_filename}"
    debug_log_path = f"C:/Users/USER/Desktop/Code/scanners/duckduckgo_maps_scraper/{debug_log_filename}"

    driver = webdriver.Chrome()  # You need to have Chrome WebDriver installed

    # Open CSV file for writing
    with open(save_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Title', 'Address', 'City', 'Neighborhood', 'Image_URL', 'Note']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        keywords = read_keywords_from_json("C:/Users/USER/Desktop/Code/scanners/duckduckgo_maps_scraper/porto_municipalities.json")
        keywords_count = len(keywords)

        for keyword in keywords:
            # Read keywords from JSON file and concatenate with the search query
            full_query = "+".join([beginning_query, keyword, end_query])
            query_url = f"https://duckduckgo.com/?va=e&t=hq&q={full_query}&ia=web&iaxm=maps"

            # Print the URL it's going to
            print(f"{datetime.datetime.now()} - Navigating to:", query_url)

            # Write URL to debug log
            with open(debug_log_path, 'a') as debug_log:
                debug_log.write(f"URL: {query_url}\n\n")

            driver.get(query_url)

            # Check if the page loaded successfully
            if "duckduckgo.com" not in driver.current_url:
                print(f"{datetime.datetime.now()} - Failed to load the page\n")
                continue

            # Write HTML content to debug log
            with open(debug_log_path, 'a', encoding='utf-8') as debug_log:
                debug_log.write(driver.page_source)

            # Wait for a moment before parsing the data
            time.sleep(2)  # Adjust the delay time as needed

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find all place list items
            place_items = soup.find_all('div', class_='module__section place-list-item js-place-list-item')

            # Print searching message
            print(f"{datetime.datetime.now()} - Searching for module__section place-list-item js-place-list-item for {keyword} ...")

            if place_items:
                print(f"{datetime.datetime.now()} - Found {len(place_items)} items for {keyword}")
            else:
                print(f"{datetime.datetime.now()} - No items found for {keyword}")
                continue

            places_count = 0

            for item in place_items:
                title_full = item.find('h2', class_='place-list-item__title').text.strip()
                
                # Extract only the name portion from the title
                title = title_full.split('. ')[-1].strip()  # Assuming the numbering format is "1. Name"

                address_info = item.find_all('li', class_='place-list-item__info__item')

                # Check if address_info contains at least two elements before accessing them
                if len(address_info) >= 2:
                    address = address_info[0].text.strip()
                    city = address_info[1].text.strip()
                else:
                    # Make a note in the CSV file indicating that the page has a different structure
                    writer.writerow({'Title': title, 'Address': 'N/A', 'City': 'N/A', 'Neighborhood': keyword.replace('+', ' '), 'Image_URL': 'N/A', 'Note': 'Different page structure'})
                    continue  # Move to the next item

                # Attempt to retrieve the image URL
                try:
                    image_url = item.find('div', class_='place-list-item__image js-place-list-item-image').find('img')['src']
                except AttributeError:
                    image_url = None  # Set image_url to None if no image URL is found

                # Print what it sees
                print(f"{datetime.datetime.now()} - Title: {title}\nAddress: {address}\nCity: {city}\nImage URL: {image_url}\n")

                # Write information to CSV
                writer.writerow({'Title': title, 'Address': address, 'City': city, 'Neighborhood': keyword.replace('+', ' '), 'Image_URL': image_url, 'Note': ''})

                places_count += 1

            # Introduce a delay before the next query
            time.sleep(10)  # Delay before next query (adjust as needed)

    # Introduce a delay before quitting the WebDriver
    time.sleep(5)  # Delay before quitting
    driver.quit()

    # Print final timestamp and statistics
    print(f"{datetime.datetime.now()} - Script Complete")
    duration = datetime.datetime.now() - start_time
    print(f"Duration: {duration}")
    print(f"Keywords searched: {keywords_count}")
    print(f"Places found: {places_count}")
    print(f"path of keywords json: C:/Users/USER/Desktop/Code/scanners/duckduckgo_maps_scraper/porto_municipalities.json")
    print(f"path of output: {save_path}")
    print(f"path of log: {debug_log_path}")


# Start time
start_time = datetime.datetime.now()

# Perform the search
scrape_duckduckgo(beginning_query, end_query)
