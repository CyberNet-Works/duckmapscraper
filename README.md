```markdown
# DuckDuckGo Maps Scraper

This script scrapes DuckDuckGo Maps for information based on specified search queries and saves the results to a CSV file and prints full HTML to a log file.

## Pip Installs Required

```
pip install selenium
pip install beautifulsoup4
```

## Dependencies

- Selenium
- BeautifulSoup
- Chrome WebDriver
- **JSON FILE WITH LOCATIONS**

## Sample Keywords JSON

```json
[
  {"keyword": "neighborhood1"},
  {"keyword": "neighborhood2"},
  {"keyword": "location1"},
  {"keyword": "location2"}
]
```

## Important Editable Variables

### Line 11: 

Define the text before the keyword in search queries
```python
beginning_query = "Text_Before_Keyword_"
```

### Line 12: 

Define the text after the keyword in search queries
```python
end_query = "Text_After_Keyword_"
```

### Line 26:

Modify the path to your JSON file containing search keywords
```python
keywords_json_path = "C:/Users/USER/Desktop/Code/scanners/duckduckgo_maps_scraper/porto_municipalities.json"
```

### Line 27: 

Change the save path for the CSV output file
```python
output_directory = "C:/Users/USER/Desktop/Code/scanners/duckduckgo_maps_scraper/"
output_filename_prefix = "duckduckgo_maps_scraper_output_"
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"{output_filename_prefix}{timestamp}.csv"
save_path = f"{output_directory}{output_filename}"
```

### Line 28: 

Modify the debug log file path
```python
debug_log_directory = "C:/Users/USER/Desktop/Code/scanners/duckduckgo_maps_scraper/"
debug_log_filename_prefix = "debug_log_"
debug_log_filename = f"{debug_log_filename_prefix}{timestamp}.html"
debug_log_path = f"{debug_log_directory}{debug_log_filename}"
```

### Line 73: 

Adjust the delay time before parsing the data (in seconds)
```python
time.sleep(2)
```

### Line 93:

Adjust the delay time before the next query (in seconds)
```python
time.sleep(10)
```

### Line 107:

Adjust the delay time before quitting the WebDriver (in seconds)
```python
time.sleep(5)
```

