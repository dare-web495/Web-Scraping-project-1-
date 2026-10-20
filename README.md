Book Web Scraper

Welcome! This is my first project focused on web scraping, built solely for practice purposes.

📌 Overview

This script automates the extraction of book information from a website. The codebase is organized into four main functions to keep the execution clean and easy to follow.

🛠 Function Breakdown

main()

Serves as the main entry point for the script. Keeps top-level execution code minimal to enhance readability.

scrape_all()

Connects the parsing functions together and automates the web scraping process across all books on the site.

parse_listing()

Extracts initial book information directly from the main listing/landing page.

parse_detail()

Navigates into individual book pages to extract any detailed or missing information.
