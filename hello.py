from telegram import InlineQueryResultGif, InlineQuery, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
from bs4 import BeautifulSoup

def scrape_gifs(query, max_gifs=30):
    print(f"Scraping GIFs for query: {query}")
    base_url = "https://porngipfy.com/"
    search_url = f"{base_url}?s={query}"

    # Send a GET request to the URL
    response = requests.get(search_url)

    gif_urls = []

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all articles containing the GIFs
        articles = soup.find_all('article', {'class': 'thumb-loop'})

        # Ensure we don't download more than max_gifs
        articles = articles[:max_gifs]

        # Get the GIF URLs
        for idx, article in enumerate(articles, start=1):
            gif_url = article.find('img')['data-gif']
            gif_urls.append(gif_url)
            print(f"Found GIF URL {idx}: {gif_url}")

    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

    return gif_urls

def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    print(f"Received inline query: {query}")

    # Scrape the GIFs
    gif_urls = scrape_gifs(query)

    results = []
    for idx, gif_url in enumerate(gif_urls, start=1):
        results.append(
            InlineQueryResultGif(
                id=str(idx),
                gif_url=gif_url,
                thumb_url=gif_url,
            )
        )

    # Answer the inline query
    print(f"Answering inline query with {len(results)} results")
    update.inline_query.answer(results)

def main():
    """Start the bot."""
    print("Starting the bot...")
    updater = Updater("6329559095:AAFZPj5hPMYeMGVpbYx93lAu1NUPGlMKVDM", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(InlineQueryHandler(inlinequery))

    print("Bot started. Waiting for inline queries...")
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
