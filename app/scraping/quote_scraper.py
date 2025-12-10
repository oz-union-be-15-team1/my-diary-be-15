import httpx
from bs4 import BeautifulSoup
from app.models.quote import Quote

#명언 스크래핑 후 database에 저장
async def scrape_and_save_quotes(pages: int = 5):
    base_url = "https://saramro.com/quotes"
    saved_count = 0

    async with httpx.AsyncClient() as client:
        for page in range(1, pages + 1):
            url = f"{base_url}?page={page}"
            try:
                response = await client.get(url)

                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, "html.parser")
                quote_elements = soup.select("table tbody tr")

                for el in quote_elements:
                    scraped = el.select_one("td[colspan='5']")
                    if not scraped:
                        continue

                    cont_and_auth = scraped.get_text(strip=True).split("-")
                    content = cont_and_auth[0]
                    author = cont_and_auth[1][1:]

                    # 중복 확인 후 저장
                    exists = await Quote.filter(content=content).exists()
                    if not exists:
                        await Quote.create(content=content, author=author)
                        saved_count += 1

            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                continue

    total_count = await Quote.all().count()
    return {
        "message": f"Scraping completed. Saved {saved_count} new quotes.",
        "total_quotes": total_count,
    }

