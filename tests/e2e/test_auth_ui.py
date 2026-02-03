import pytest
import re
from playwright.sync_api import Page, expect

def test_login_redirect(page: Page, frontend_url: str):
    """
    Test that clicking the Login button redirects to Google OAuth.
    This test mocks nothing in the application code.
    It stops at the Google login page because we cannot automate 
    Google login without credentials and 2FA handling.
    """
    print(f"Navigating to {frontend_url}/")
    page.goto(f"{frontend_url}/", timeout=10000)
    
    # Locate the login button (either in header or hero section)
    # In LandingPage it's "Sign Up Now" (cta-button primary)
    # In Header it's "Login" (header-auth-link)
    
    # Let's try the one in the header first as it's consistent
    login_link = page.locator("a.header-auth-link")
    
    # Ensure it's visible
    expect(login_link).to_be_visible()
    
    print("Clicking Login button...")
    # Note: clicking a link that redirects to a new domain might trigger navigation events
    with page.expect_navigation(url=re.compile(r"accounts\.google\.com")):
        login_link.click()
        
    print("Successfully redirected to Google Accounts")
    
    # Verify we are on google.com
    assert "accounts.google.com" in page.url
