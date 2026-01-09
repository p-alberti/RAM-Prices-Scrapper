# RAM-Prices-Scrapper
This project explores the challenges of collecting real-world pricing data
for hardware components when no public APIs or up-to-date datasets are available.

The initial focus is on building a reliable and reusable data collection
pipeline that enables future analysis of RAM price trends over time.

The goal of this project is to:

- Collect up-to-date pricing data from e-commerce search pages
- Store historical snapshots for longitudinal analysis
- Practice ethical and responsible web scraping techniques
- Build a reusable and configurable scraping tool

The scraper is designed to be generic and configurable, relying on
HTML selectors rather than hardcoded website logic.

Key design considerations:
- Decoupled extraction logic and website structure
- Rate limiting and request delays
- Safe handling of missing or inconsistent data
- Separation between data collection and analysis stages


This project was developed for educational and personal learning purposes.

The scraper does not target any specific website and is intentionally
kept generic. Users are responsible for ensuring compliance with the
terms of service of any website they choose to scrape.


Planned improvements:
- Keyword-based filtering of irrelevant products
- Price normalization and currency handling
- Automated scheduled scraping
- Exploratory data analysis and visualization

