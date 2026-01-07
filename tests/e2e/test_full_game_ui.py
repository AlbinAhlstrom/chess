import pytest
import re
from playwright.sync_api import Page, expect

def move_piece(page: Page, start_sq: str, end_sq: str):
    """Moves a piece from start_sq to end_sq using low-level mouse actions to avoid interception issues."""
    start_selector = f"div.piece[data-square='{start_sq}']"
    end_selector = f".squares div[data-square='{end_sq}']"
    
    # Locate elements
    start_el = page.locator(start_selector)
    end_el = page.locator(end_selector)
    
    # Get bounding boxes for centers
    start_box = start_el.bounding_box()
    end_box = end_el.bounding_box()
    
    if not start_box or not end_box:
        raise Exception(f"Could not find bounding box for {start_sq} or {end_sq}")

    # Precise mouse movement
    page.mouse.move(start_box["x"] + start_box["width"] / 2, start_box["y"] + start_box["height"] / 2)
    page.mouse.down()
    # Move to destination
    page.mouse.move(end_box["x"] + end_box["width"] / 2, end_box["y"] + end_box["height"] / 2, steps=10)
    page.mouse.up()
    
    # Wait for state update (piece moved)
    page.wait_for_selector(f"div.piece[data-square='{end_sq}']", timeout=10000)

def test_full_game_ui(page: Page, frontend_url: str):
    # Set a decent size for desktop play
    page.set_viewport_size({"width": 1280, "height": 720})
    page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
    page.goto(f"{frontend_url}/otb", timeout=10000)
    
    print("Waiting for redirect to /game/...")
    page.wait_for_url(re.compile(r".*/game/.*"), timeout=10000)
    
    print("Board loading...")
    page.wait_for_selector(".board", timeout=10000)
    
    # Fool's Mate Sequence
    moves = [
        ("f2", "f3"),
        ("e7", "e5"),
        ("g2", "g4"),
        ("d8", "h4")
    ]
    
    for start, end in moves:
        print(f"Moving {start} to {end}...")
        move_piece(page, start, end)
        page.wait_for_timeout(500) 
        
    print("Verifying checkmate result in history...")
    history = page.locator(".move-history")
    expect(history).to_contain_text("0-1", timeout=10000)

def test_undo_ui(page: Page, frontend_url: str):
    """Tests the Undo button which is available in OTB mode."""
    print(f"Navigating to {frontend_url}/otb")
    page.goto(f"{frontend_url}/otb", timeout=10000)
    
    page.wait_for_url(re.compile(r".*/game/.*"), timeout=10000)
    page.wait_for_selector(".board", timeout=10000)
    
    # Make a move
    print("Making a move...")
    move_piece(page, "e2", "e4")
    
    # Verify move in history
    history = page.locator(".move-history")
    expect(history).to_contain_text("e4")
    
    # Click Undo
    print("Clicking Undo...")
    undo_btn = page.locator("button[title='Undo']")
    undo_btn.click()
    
    # Verify move removed from history
    page.wait_for_timeout(1000)
    expect(history).not_to_contain_text("e4")