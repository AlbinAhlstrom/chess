import pytest
import re
from playwright.sync_api import Page, expect

def tap_square(page: Page, square: str):
    print(f"Tapping square {square}...")
    board = page.locator(".pieces")
    box = board.bounding_box()
    
    file_map = {c: i for i, c in enumerate("abcdefgh")}
    file_idx = file_map[square[0]]
    rank_idx = 8 - int(square[1])
    
    square_size = box["width"] / 8
    x = box["x"] + file_idx * square_size + square_size / 2
    y = box["y"] + rank_idx * square_size + square_size / 2
    
    page.touchscreen.tap(x, y)

def test_mobile_tap_move(browser, frontend_url):
    # Create a context with touch enabled
    context = browser.new_context(
        viewport={"width": 375, "height": 667},
        has_touch=True,
        is_mobile=True
    )
    page = context.new_page()

    page.on("console", lambda msg: print(f"BROWSER CONSOLE [{msg.type}]: {msg.text}"))
    
    page.goto(f"{frontend_url}/otb")
    
    print("Waiting for redirect...")
    page.wait_for_url(re.compile(r".*/game/.*"), timeout=5000)
    
    page.wait_for_selector(".pieces")
    # Wait for legal moves to load
    page.wait_for_timeout(1000)
    
    # 1. Tap to Select White Pawn at e2
    tap_square(page, "e2")
    
    # 2. Verify Legal Move Dots appear (specifically at e4)
    # The dot for e4 should be clickable
    expect(page.locator(".legal-move-dot")).to_have_count(2) # e3, e4
    
    # 3. Tap e4 to Move
    print("Attempting to move to e4 via tap...")
    tap_square(page, "e4")
    
    # 4. Verify Move Happened
    # The piece should now be at e4
    expect(page.locator("div.piece[data-square='e4']")).to_be_visible()
    # Dots should be gone
    expect(page.locator(".legal-move-dot")).to_have_count(0)
