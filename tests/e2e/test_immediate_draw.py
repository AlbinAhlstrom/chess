import pytest
import re
from playwright.sync_api import Page, expect

def test_immediate_draw_on_creation(page: Page, frontend_url: str):
    # 1. Navigate to the app (OTB mode creates a local game)
    # print(f"Navigating to {frontend_url}/otb")
    page.goto(f"{frontend_url}/otb")
    
    # 2. Wait for game creation and board load
    page.wait_for_url(re.compile(r".*/game/.*"), timeout=5000)
    
    # Capture the GET game state response
    with page.expect_response(lambda response: "/api/game/" in response.url and response.request.method == "GET") as response_info:
        page.wait_for_selector(".board", timeout=5000)
    
    response = response_info.value
    game_state = response.json()
    print(f"Captured Game State: is_over={game_state.get('is_over')}")
    
    page.wait_for_selector(".board", timeout=5000)
    
    # 3. Check for "Draw" text or game over modal
    # Expectation: Should NOT be visible immediately
    # Assuming the UI shows "1/2-1/2" or "Draw" in the result area or modal
    
    # Check history result
    history = page.locator(".move-history")
    expect(history).not_to_contain_text("1/2-1/2")
    expect(history).not_to_contain_text("Draw")
    
    # Check for modal header
    expect(page.locator("h2:has-text('Game Over')")).not_to_be_visible()
    
    # Check for draw indicators on kings
    expect(page.locator(".on-draw-king")).to_have_count(0)
    
