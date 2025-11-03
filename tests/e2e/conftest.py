"""
Configuration for end-to-end tests
"""

import pytest
import asyncio
import os
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

# E2E test configuration
BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:3000")
TEST_TIMEOUT = 30000  # 30 seconds
SCREENSHOT_ON_FAILURE = True

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def browser():
    """Launch browser for E2E tests"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()

@pytest.fixture
async def page(browser: Browser):
    """Create a new page for each test"""
    context = await browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True
    )
    page = await context.new_page()
    page.set_default_timeout(TEST_TIMEOUT)

    yield page

    if SCREENSHOT_ON_FAILURE:
        # Take screenshot on failure
        try:
            await page.screenshot(full_page=True)
        except:
            pass

    await context.close()

@pytest.fixture
async def authenticated_page(browser: Browser):
    """Create an authenticated page for tests that require login"""
    context = await browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True
    )
    page = await context.new_page()
    page.set_default_timeout(TEST_TIMEOUT)

    # Login with test credentials
    await page.goto(f"{BASE_URL}/empleados")
    await page.fill('input[type="email"]', "admin@pylink.com")
    await page.fill('input[type="password"]', "admin123")
    await page.click('button[type="submit"]')

    # Wait for login to complete
    await page.wait_for_url(f"{BASE_URL}/empleados/dashboard")

    yield page

    await context.close()

@pytest.fixture
async def admin_page(browser: Browser):
    """Create an authenticated admin page for admin tests"""
    context = await browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True
    )
    page = await context.new_page()
    page.set_default_timeout(TEST_TIMEOUT)

    # Login as admin
    await page.goto(f"{BASE_URL}/empleados")
    await page.fill('input[type="email"]', "admin@pylink.com")
    await page.fill('input[type="password"]', "admin123")
    await page.click('button[type="submit"]')

    # Wait for login and navigate to admin panel
    await page.wait_for_url(f"{BASE_URL}/empleados/dashboard")
    # Navigate to admin panel if available
    admin_link = await page.query_selector('a[href*="admin"]')
    if admin_link:
        await admin_link.click()
        await page.wait_for_load_state("networkidle")

    yield page

    await context.close()

# Test data fixtures
@pytest.fixture
def test_user_data():
    """Test user credentials"""
    return {
        "email": "admin@pylink.com",
        "password": "admin123",
        "name": "Admin User",
        "role": "admin"
    }

@pytest.fixture
def test_employee_data():
    """Test employee credentials"""
    return {
        "email": "juan@pylink.com",
        "password": "emp123",
        "name": "Juan Employee",
        "role": "desarrollador"
    }

@pytest.fixture
def test_project_data():
    """Test project data"""
    return {
        "name": "E2E Test Project",
        "description": "Project created during E2E testing",
        "client": "E2E Test Client",
        "budget": 15000.0
    }

@pytest.fixture
def test_task_data():
    """Test task data"""
    return {
        "title": "E2E Test Task",
        "description": "Task created during E2E testing",
        "priority": "alta"
    }

@pytest.fixture
def test_contact_data():
    """Test contact form data"""
    return {
        "name": "E2E Test User",
        "email": "e2e@test.com",
        "subject": "E2E Test Message",
        "message": "This is a test message sent during E2E testing."
    }

# Custom markers for E2E tests
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "auth: mark test as requiring authentication"
    )
    config.addinivalue_line(
        "markers", "admin: mark test as requiring admin privileges"
    )

# Skip E2E tests if environment is not set up
def pytest_collection_modifyitems(config, items):
    skip_e2e = pytest.mark.skip(reason="E2E tests disabled or environment not ready")

    # Check if we should run E2E tests
    run_e2e = os.getenv("RUN_E2E_TESTS", "false").lower() == "true"

    if not run_e2e:
        for item in items:
            if "e2e" in item.keywords:
                item.add_marker(skip_e2e)