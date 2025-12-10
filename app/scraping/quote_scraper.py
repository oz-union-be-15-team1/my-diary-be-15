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
                # saramro.com 구조에 맞춰 선택자 수정 필요 (예시 구조 사용)
                # 실제 사이트 구조 확인 후 .quote-content, .quote-author 등의 클래스명 조정 필요
                quote_elements = soup.select(".quote-card")  # 가상 클래스명

                for el in quote_elements:
                    content_el = el.select_one(".quote-text")
                    author_el = el.select_one(".quote-author")

                    if not content_el:
                        continue

                    content = content_el.get_text(strip=True)
                    author = author_el.get_text(strip=True) if author_el else "Unknown"

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

