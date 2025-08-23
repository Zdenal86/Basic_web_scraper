from src import WebScraper

def main():
    webscraper = WebScraper("https://quotes.toscrape.com/")
    title = webscraper.check_website()
    if title:
        print(f"Website title: {title}")
    else:
        print("Failed to scrape website")

if __name__ == "__main__":
    main()