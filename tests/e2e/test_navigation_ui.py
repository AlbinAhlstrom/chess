import pytest
import re
from playwright.sync_api import Page, expect

def move_piece(page: Page, start_sq: str, end_sq: str):
    start_selector = f"div.piece[data-square='{start_sq}']"
    end_selector = f".squares div[data-square='{end_sq}']"
    page.wait_for_selector(start_selector, timeout=5000)
    page.wait_for_selector(end_selector, timeout=5000)
    start_box = page.locator(start_selector).bounding_box()
    end_box = page.locator(end_selector).bounding_box()
    page.mouse.move(start_box["x"] + start_box["width"] / 2, start_box["y"] + start_box["height"] / 2)
    page.mouse.down()
    page.mouse.move(end_box["x"] + end_box["width"] / 2, end_box["y"] + end_box["height"] / 2, steps=5)
    page.mouse.up()
    page.wait_for_selector(f"div.piece[data-square='{end_sq}']", timeout=5000)

def test_history_navigation_ui(page: Page, frontend_url: str):
    page.set_viewport_size({"width": 375, "height": 667})
    page.on("console", lambda msg: print(f"BROWSER CONSOLE [{msg.type}]: {msg.text}"))
    page.on("request", lambda request: print(f"REQUEST: {request.method} {request.url}"))
    page.on("requestfailed", lambda request: print(f"REQUEST FAILED: {request.url} - {request.failure}"))
    page.on("response", lambda response: print(f"RESPONSE: {response.status} {response.url}"))
    
    print(f"Navigating to {frontend_url}/otb")
    page.goto(f"{frontend_url}/otb", timeout=5000)

    print("Waiting for page content...")
    try:
        # Check if we are stuck on loading screen
        loading = page.locator(".loading-screen")
        if loading.is_visible():
            print("Detected loading screen...")
            
        page.wait_for_selector(".pieces", timeout=5000)
        print(f"Current URL after load: {page.url}")
    except Exception as e:
        page.screenshot(path="nav_fail.png")
        print(f"Current URL on failure: {page.url}")
        # Log HTML for debugging
        content = page.content()
        print(f"Page Content Snippet: {content[:500]}")
        raise e
    # 1. Make some moves
    print("Making moves...")
    move_piece(page, "e2", "e4")
    page.wait_for_timeout(500)
    move_piece(page, "e7", "e5")
    page.wait_for_timeout(500)
    
    # 2. Check history bar items
    print("Checking history items...")
    history_bar = page.locator(".mobile-history-scroll")
    expect(history_bar).to_be_visible()
    items = history_bar.locator(".history-item")
    expect(items).to_have_count(2)
    
    # 3. Go back to Start
    print("Navigating back to Start...")
    # There is no "Start" item in the scroll, use First Move button
    first_btn = page.locator(".mobile-history-bar button[title='First Move']")
    first_btn.click()
    page.wait_for_timeout(500)
    expect(page.locator("div.piece[data-square='e2']")).to_be_visible()
    
    # 4. Verify board is disabled
    print("Verifying board is disabled...")
    board = page.locator(".board")
    expect(board).to_have_css("pointer-events", "none")
    
    # 5. Use navigation buttons
    print("Testing navigation buttons...")
    next_btn = page.locator(".mobile-history-bar button[title='Next']")
    next_btn.click()
    page.wait_for_timeout(500)
    expect(page.locator("div.piece[data-square='e4']")).to_be_visible()
    
    # 6. Go to latest
    print("Returning to latest...")
    last_btn = page.locator(".mobile-history-bar button[title='Last Move']")
    last_btn.click()
    page.wait_for_timeout(500)
    expect(board).to_have_css("pointer-events", "auto")
    
    # 7. Make another move
    print("Making another move...")
    move_piece(page, "g1", "f3")
    expect(items).to_have_count(3)