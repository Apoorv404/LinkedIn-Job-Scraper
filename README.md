# LinkedIn Job Scraper

A Python-based automation tool that scrapes job listings from LinkedIn based on your specified role and location preferences. The tool features a user-friendly Streamlit interface and saves the scraped data to a CSV file for easy analysis.

## Features

- Web-based interface using Streamlit
- Customizable job role and location search
- Automated LinkedIn login
- Real-time scraping progress updates
- Results saved in CSV format
- Data includes job titles, companies, and other relevant information

## Requirements

- Python 3.x
- Chrome WebDriver
- Required Python packages:
  - streamlit
  - selenium
  - beautifulsoup4
  - pandas
  - python-dotenv

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/LinkedIn-Job-Scraper.git
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your LinkedIn credentials:
   ```
   username=your_linkedin_email
   password=your_linkedin_password
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Enter your desired job role and location in the web interface
3. Click "Run Automation" to start the scraping process
4. Wait for the process to complete - results will be saved in `jobs.csv`

## How it Works

1. The application uses Selenium WebDriver to automate browser interactions
2. Logs into LinkedIn using provided credentials
3. Searches for jobs based on user input
4. Scrapes relevant job information from search results
5. Saves the data in a structured CSV format

## Note

- Ensure you have a stable internet connection
- The tool respects LinkedIn's usage terms and implements appropriate delays
- Keep your LinkedIn credentials secure and never share your `.env` file

