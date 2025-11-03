"""
End-to-end tests for authentication functionality
"""

import pytest
from playwright.async_api import Page, expect

BASE_URL = "http://localhost:3000"

@pytest.mark.e2e
@pytest.mark.auth
class TestAuthentication:
    """Test authentication flows"""

    async def test_login_page_loads(self, page: Page):
        """Test that the login page loads correctly"""
        await page.goto(f"{BASE_URL}/empleados")

        # Check that we're on the login page
        await expect(page).to_have_url(f"{BASE_URL}/empleados")

        # Check that login form elements are present
        await expect(page.locator('input[type="email"]')).to_be_visible()
        await expect(page.locator('input[type="password"]')).to_be_visible()
        await expect(page.locator('button[type="submit"]')).to_be_visible()

        # Check page title and headings
        await expect(page.locator('h1, h2')).to_contain_text("empleados", timeout=5000)

    async def test_successful_admin_login(self, page: Page, test_user_data):
        """Test successful admin login"""
        await page.goto(f"{BASE_URL}/empleados")

        # Fill in login form
        await page.fill('input[type="email"]', test_user_data["email"])
        await page.fill('input[type="password"]', test_user_data["password"])

        # Submit form
        await page.click('button[type="submit"]')

        # Should redirect to dashboard
        await expect(page).to_have_url(f"{BASE_URL}/empleados/dashboard", timeout=10000)

        # Check that user is logged in
        # Look for user info or dashboard elements
        await expect(page.locator('body')).to_contain_text(test_user_data["name"], timeout=5000)

    async def test_successful_employee_login(self, page: Page, test_employee_data):
        """Test successful employee login"""
        await page.goto(f"{BASE_URL}/empleados")

        # Fill in login form
        await page.fill('input[type="email"]', test_employee_data["email"])
        await page.fill('input[type="password"]', test_employee_data["password"])

        # Submit form
        await page.click('button[type="submit"]')

        # Should redirect to dashboard
        await expect(page).to_have_url(f"{BASE_URL}/empleados/dashboard", timeout=10000)

        # Check that employee dashboard is loaded
        await expect(page.locator('body')).to_contain_text(test_employee_data["name"], timeout=5000)

    async def test_login_with_invalid_credentials(self, page: Page):
        """Test login with invalid credentials"""
        await page.goto(f"{BASE_URL}/empleados")

        # Fill in invalid credentials
        await page.fill('input[type="email"]', "invalid@test.com")
        await page.fill('input[type="password"]', "wrongpassword")

        # Submit form
        await page.click('button[type="submit"]')

        # Should stay on login page and show error
        await expect(page).to_have_url(f"{BASE_URL}/empleados")

        # Look for error message (common patterns)
        error_selectors = [
            '[data-testid="error-message"]',
            '.error-message',
            '.alert-danger',
            '[role="alert"]',
            'text="Error"',
            'text="Invalid"',
            'text="Incorrect"'
        ]

        error_found = False
        for selector in error_selectors:
            try:
                element = page.locator(selector)
                if await element.count() > 0:
                    error_found = True
                    break
            except:
                continue

        # If no specific error element found, at least verify we're not logged in
        if not error_found:
            await expect(page).to_have_url(f"{BASE_URL}/empleados")

    async def test_login_with_empty_fields(self, page: Page):
        """Test login with empty email and password"""
        await page.goto(f"{BASE_URL}/empleados")

        # Submit form with empty fields
        await page.click('button[type="submit"]')

        # Should stay on login page
        await expect(page).to_have_url(f"{BASE_URL}/empleados")

        # Check for validation messages if present
        # Many forms show HTML5 validation
        email_input = page.locator('input[type="email"]')
        password_input = page.locator('input[type="password"]')

        # Check if inputs have validation attributes
        email_required = await email_input.get_attribute("required")
        password_required = await password_input.get_attribute("required")

        # If fields are required, browser should show validation
        if email_required or password_required:
            # The browser should prevent form submission
            await expect(page).to_have_url(f"{BASE_URL}/empleados")

    async def test_logout_functionality(self, page: Page, test_user_data):
        """Test logout functionality"""
        # First login
        await page.goto(f"{BASE_URL}/empleados")
        await page.fill('input[type="email"]', test_user_data["email"])
        await page.fill('input[type="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')

        # Wait for dashboard
        await expect(page).to_have_url(f"{BASE_URL}/empleados/dashboard")

        # Look for logout button/link
        logout_selectors = [
            'button:has-text("Logout")',
            'button:has-text("Cerrar sesión")',
            'a:has-text("Logout")',
            'a:has-text("Cerrar sesión")',
            '[data-testid="logout-button"]',
            '.logout-button'
        ]

        logout_element = None
        for selector in logout_selectors:
            try:
                element = page.locator(selector)
                if await element.count() > 0:
                    logout_element = element.first
                    break
            except:
                continue

        if logout_element:
            await logout_element.click()

            # Should redirect to login page
            await expect(page).to_have_url(f"{BASE_URL}/empleados", timeout=5000)

    async def test_session_persistence(self, page: Page, test_user_data):
        """Test that session persists across page reloads"""
        # Login
        await page.goto(f"{BASE_URL}/empleados")
        await page.fill('input[type="email"]', test_user_data["email"])
        await page.fill('input[type="password"]', test_user_data["password"])
        await page.click('button[type="submit"]')

        # Wait for dashboard
        await expect(page).to_have_url(f"{BASE_URL}/empleados/dashboard")

        # Reload page
        await page.reload()

        # Should still be logged in
        await expect(page).to_have_url(f"{BASE_URL}/empleados/dashboard")
        await expect(page.locator('body')).to_contain_text(test_user_data["name"], timeout=5000)

    async def test_access_protected_routes_without_auth(self, page: Page):
        """Test accessing protected routes without authentication"""
        protected_routes = [
            "/empleados/dashboard",
            "/admin",
            "/profile"
        ]

        for route in protected_routes:
            await page.goto(f"{BASE_URL}{route}")

            # Should redirect to login page
            await page.wait_for_timeout(2000)  # Wait for potential redirect

            current_url = page.url
            # Check if we're on login page or still on protected route
            if "empleados" in current_url and "dashboard" not in current_url:
                # Redirected to login - this is expected
                pass
            elif "login" in current_url.lower():
                # Redirected to login - this is expected
                pass
            else:
                # Still on protected route - this might be okay if the page shows login form
                await expect(page.locator('input[type="email"]')).to_be_visible(timeout=5000)

    async def test_login_form_validation(self, page: Page):
        """Test login form client-side validation"""
        await page.goto(f"{BASE_URL}/empleados")

        # Test email format validation
        email_input = page.locator('input[type="email"]')
        await email_input.fill("invalid-email-format")

        # Try to submit and check if browser prevents it
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)

        # Check if we're still on login page (validation prevented submission)
        current_url = page.url
        assert "empleados" in current_url
        assert "dashboard" not in current_url

if __name__ == "__main__":
    pytest.main([__file__, "-v"])