import pytest
from playwright.sync_api import Page, expect

def select_square(page: Page, square: str):
    print(f"Selecting square {square}...")
    # Calculate coordinates relative to the board
    board = page.locator(".pieces")
    box = board.bounding_box()
    
    file_map = {c: i for i, c in enumerate("abcdefgh")}
    file_idx = file_map[square[0]]
    rank_idx = 8 - int(square[1])
    
    square_size = box["width"] / 8
    x = box["x"] + file_idx * square_size + square_size / 2
    y = box["y"] + rank_idx * square_size + square_size / 2
    
    # Always click the board at these coordinates
    page.mouse.click(x, y)

import re

def test_selection_logic(page: Page, frontend_url: str):
    page.on("console", lambda msg: print(f"BROWSER CONSOLE [{msg.type}]: {msg.text}"))
    page.goto(f"{frontend_url}/otb")
    
    # Wait for redirect
    print("Waiting for redirect...")
    page.wait_for_url(re.compile(r".*/game/.*"), timeout=5000)
    
    page.wait_for_selector(".pieces")
    # Wait for legal moves to load (API call)
    page.wait_for_timeout(1000)
    
    # 1. Select by Click
    select_square(page, "e2")
    
    # 3. Visual Feedback (Selected Highlight & Dots)
    # expect() will wait up to 5s
    expect(page.locator(".legal-move-dot")).to_have_count(2)
    
    # 4. Deselect (Click same piece)
    select_square(page, "e2")
    expect(page.locator(".legal-move-dot")).to_have_count(0)
    
    # 5. Switch Selection
    select_square(page, "e2")
    expect(page.locator(".legal-move-dot")).to_have_count(2)
    
    select_square(page, "d2")
    expect(page.locator(".legal-move-dot")).to_have_count(2) 
    
    # 7. Empty Square Deselect
    select_square(page, "a5")
    expect(page.locator(".legal-move-dot")).to_have_count(0)

def move_piece_by_drag(page: Page, start_sq: str, end_sq: str, expect_dots=True):
    print(f"Dragging {start_sq} to {end_sq}...")
    # Use coordinates to avoid interception issues
    board = page.locator(".pieces")
    box = board.bounding_box()
    square_size = box["width"] / 8
    file_map = {c: i for i, c in enumerate("abcdefgh")}
    
    s_f, s_r = file_map[start_sq[0]], 8 - int(start_sq[1])
    e_f, e_r = file_map[end_sq[0]], 8 - int(end_sq[1])
    
    start_x = box["x"] + s_f * square_size + square_size / 2
    start_y = box["y"] + s_r * square_size + square_size / 2
    end_x = box["x"] + e_f * square_size + square_size / 2
    end_y = box["y"] + e_r * square_size + square_size / 2
    
    page.mouse.move(start_x, start_y)
    page.mouse.down()
    # Trigger drag threshold (8px)
    page.mouse.move(start_x, start_y - 20)
    
    # Small wait for React state update
    page.wait_for_timeout(100)
    
    # Verify dots appear during drag (Requirement 10 clarification)
    if expect_dots:
        expect(page.locator(".legal-move-dot")).not_to_have_count(0)
    else:
        expect(page.locator(".legal-move-dot")).to_have_count(0)
    
    page.mouse.move(end_x, end_y, steps=10)
    page.mouse.up()

def test_drag_interaction(page: Page, frontend_url: str):
    page.on("console", lambda msg: print(f"BROWSER CONSOLE [{msg.type}]: {msg.text}"))
    page.goto(f"{frontend_url}/otb")
    
    # Wait for redirect
    print("Waiting for redirect...")
    page.wait_for_url(re.compile(r".*/game/.*"), timeout=5000)
    
    page.wait_for_selector(".pieces")
    # Wait for legal moves to load
    page.wait_for_timeout(1000)
    
    # 10. Drag Unselected -> Selects immediately
    move_piece_by_drag(page, "e2", "e4")
    
    # Verify move completed
    expect(page.locator(".legal-move-dot")).to_have_count(0)
    expect(page.locator("div.piece[data-square='e4']")).to_be_visible()
    
    # 2. Drag back to start -> Counts as click (Selects)
    # Knight at g1 is unselected. Dragging it and dropping back should select it.
    # It is Black's turn (after e2e4), so g1 (white) should have NO dots (Requirement 6)
    move_piece_by_drag(page, "g1", "g1", expect_dots=False) 
    expect(page.locator(".legal-move-dot")).to_have_count(0) 

def test_opponent_selection(page: Page, frontend_url: str):
    page.on("console", lambda msg: print(f"BROWSER CONSOLE [{msg.type}]: {msg.text}"))
    page.goto(f"{frontend_url}/otb")
    
    # Wait for redirect
    print("Waiting for redirect...")
    page.wait_for_url(re.compile(r".*/game/.*"), timeout=5000)
    
    page.wait_for_selector(".pieces")
    # Wait for legal moves to load
    page.wait_for_timeout(1000)
    
    # 6. Opponent Selection
    select_square(page, "e7")
    expect(page.locator(".legal-move-dot")).to_have_count(0)
    expect(page.locator(".highlight-square")).to_have_count(1)
