"""Screenshot utility module."""
import os
import asyncio
from typing import Optional
from pathlib import Path
from playwright.async_api import async_playwright

async def take_screenshot(
    url: str,
    output_path: Optional[str] = None,
    width: int = 1920,
    height: int = 1080,
    full_page: bool = False,
    wait_for_load: bool = True,
    wait_for_network_idle: bool = True
) -> str:
    """Take a screenshot of a webpage using Playwright."""
    if output_path is None:
        output_path = f"screenshot_{hash(url)}.png"
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Set viewport size
        await page.set_viewport_size({"width": width, "height": height})
        
        # Navigate to the page
        await page.goto(url)
        
        # Wait for the page to load
        if wait_for_load:
            await page.wait_for_load_state("load")
        if wait_for_network_idle:
            await page.wait_for_load_state("networkidle")
        
        # Take the screenshot
        await page.screenshot(
            path=str(output_path),
            full_page=full_page
        )
        
        await browser.close()
    
    return str(output_path)

def take_screenshot_sync(
    url: str,
    output_path: Optional[str] = None,
    **kwargs
) -> str:
    """Synchronous wrapper for take_screenshot."""
    return asyncio.run(take_screenshot(url, output_path, **kwargs)) 