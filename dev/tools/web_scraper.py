"""Web scraping utility module."""
import asyncio
from typing import List, Dict, Any, Optional
import aiohttp
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from tqdm import tqdm

async def scrape_urls(
    urls: List[str],
    max_concurrent: int = 5,
    use_playwright: bool = False,
    **kwargs: Any
) -> Dict[str, str]:
    """Scrape multiple URLs concurrently."""
    if use_playwright:
        return await _scrape_with_playwright(urls, max_concurrent, **kwargs)
    else:
        return await _scrape_with_aiohttp(urls, max_concurrent, **kwargs)

async def _scrape_with_aiohttp(
    urls: List[str],
    max_concurrent: int = 5,
    timeout: int = 30,
    **kwargs: Any
) -> Dict[str, str]:
    """Scrape URLs using aiohttp."""
    results = {}
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(
                _fetch_url(session, url, semaphore, timeout)
            )
            tasks.append(task)
        
        for coro in tqdm(
            asyncio.as_completed(tasks),
            total=len(tasks),
            desc="Scraping URLs"
        ):
            url, content = await coro
            if content:
                results[url] = content
    
    return results

async def _fetch_url(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore,
    timeout: int
) -> tuple[str, Optional[str]]:
    """Fetch a single URL using aiohttp."""
    async with semaphore:
        try:
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'lxml')
                    return url, soup.get_text()
                return url, None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return url, None

async def _scrape_with_playwright(
    urls: List[str],
    max_concurrent: int = 5,
    **kwargs: Any
) -> Dict[str, str]:
    """Scrape URLs using Playwright."""
    results = {}
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        tasks = []
        for url in urls:
            task = asyncio.create_task(
                _fetch_with_playwright(browser, url, semaphore)
            )
            tasks.append(task)
        
        for coro in tqdm(
            asyncio.as_completed(tasks),
            total=len(tasks),
            desc="Scraping URLs with Playwright"
        ):
            url, content = await coro
            if content:
                results[url] = content
        
        await browser.close()
    
    return results

async def _fetch_with_playwright(
    browser: Any,
    url: str,
    semaphore: asyncio.Semaphore
) -> tuple[str, Optional[str]]:
    """Fetch a single URL using Playwright."""
    async with semaphore:
        try:
            page = await browser.new_page()
            await page.goto(url)
            content = await page.content()
            soup = BeautifulSoup(content, 'lxml')
            text = soup.get_text()
            await page.close()
            return url, text
        except Exception as e:
            print(f"Error fetching {url} with Playwright: {e}")
            return url, None

def scrape_urls_sync(
    urls: List[str],
    max_concurrent: int = 5,
    **kwargs: Any
) -> Dict[str, str]:
    """Synchronous wrapper for scrape_urls."""
    return asyncio.run(scrape_urls(urls, max_concurrent, **kwargs)) 