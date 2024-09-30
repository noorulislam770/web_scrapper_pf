
# Candidate Information Web Scraper

This Python project is designed to scrape detailed information about political candidates from the Punjab Assembly's website. It allows the user to enter a candidate's name, navigates to the candidate's profile, and extracts relevant details such as contact information, political affiliation, occupation, and family details. The extracted data is saved in both CSV and JSON formats.

## Features

- Automatically navigates to the Punjab Assembly's members list.
- Extracts key information about a specific candidate.
- Saves data in both JSON and CSV formats.
- User-friendly console prompts and informative messages at each step.

## Prerequisites

- Python 3.7+
- Google Chrome installed on your system.
- [ChromeDriver](https://chromedriver.chromium.org/downloads) installed and the path configured correctly.
  - The ChromeDriver version must match the version of Chrome you have installed.
- `requirements.txt` lists all the Python dependencies.

## Setup Guide

### 1. Clone the Repository

Start by cloning the repository:

```bash
git clone https://github.com/noorulislam770/web_scrapper_pf.git
cd web_scrapper_pf
```

### 2. Install Dependencies

Install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Download and Set Up ChromeDriver

You need to download and install ChromeDriver that matches your version of Google Chrome:

1. Check your Chrome version by navigating to `chrome://settings/help` in your Chrome browser.
2. [Download the corresponding version of ChromeDriver](https://www.chromedriverdownload.com/en/download/chromedriver-129.0.6668.6-win64) and extract it.
3. Place the `chromedriver` executable in a location that's in your system's PATH or specify the path directly in the code (line 22 in `scraper.py` ).

### 4. Running the Web Scraper

You can now run the web scraping tool. It will prompt you to enter the candidate's name and the search URL (or use the default URL for the Punjab Assembly website).

Run the following command to start the script:

```bash
python scraper.py
```

### 5. Saving Data

Once the script runs, the following files will be generated in the `output` directory:

- **JSON File**: Contains structured information about the candidate.
- **CSV File**: Contains the same information in CSV format.

The files will be stored in a subfolder named after the candidate.

## Example

```bash
Enter the candidate's name: Syed Yawar Abbas Bukhari
Enter the search URL:
(default: https://www.pap.gov.pk/members/contactdetails/en/21?bycontact=true) 
```

The script will search for the candidate on the given URL, extract the details, and save the information in the `output/Syed Yawar Abbas Bukhari/` folder as a JSON and CSV file.

## Troubleshooting

- Ensure your ChromeDriver version matches the installed Chrome version.
- If the scraper fails to find the candidate, ensure the spelling of the candidate's name matches the website.

## Future Enhancements

- Handle more dynamic content loading cases.
- Add better error handling and retry logic.
- Improve support for other political websites.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
