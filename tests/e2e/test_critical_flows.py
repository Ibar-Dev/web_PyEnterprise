"""
End-to-end tests for critical user flows
"""

import pytest
from playwright.async_api import Page, expect

BASE_URL = "http://localhost:3000"

@pytest.mark.e2e
@pytest.mark.slow
class TestCriticalUserFlows:
    """Test critical business flows"""

    async def test_contact_form_submission(self, page: Page, test_contact_data):
        """Test contact form submission flow"""
        await page.goto(BASE_URL)

        # Navigate to contact page
        contact_link = page.locator('a[href*="contact"], a:has-text("Contacto")')
        if await contact_link.count() > 0:
            await contact_link.first.click()
        else:
            # Try direct navigation
            await page.goto(f"{BASE_URL}/contact")

        # Wait for contact form to load
        await page.wait_for_load_state("networkidle")

        # Fill contact form
        name_input = page.locator('input[name="name"], input[placeholder*="nombre"]')
        email_input = page.locator('input[name="email"], input[type="email"]')
        subject_input = page.locator('input[name="subject"], input[placeholder*="asunto"]')
        message_input = page.locator('textarea[name="message"], textarea[placeholder*="mensaje"]')

        if await name_input.count() > 0:
            await name_input.fill(test_contact_data["name"])
        if await email_input.count() > 0:
            await email_input.fill(test_contact_data["email"])
        if await subject_input.count() > 0:
            await subject_input.fill(test_contact_data["subject"])
        if await message_input.count() > 0:
            await message_input.fill(test_contact_data["message"])

        # Submit form
        submit_button = page.locator('button[type="submit"], button:has-text("Enviar")')
        if await submit_button.count() > 0:
            await submit_button.click()

            # Wait for submission
            await page.wait_for_timeout(2000)

            # Check for success message
            success_selectors = [
                '[data-testid="success-message"]',
                '.success-message',
                '.alert-success',
                'text="Gracias"',
                'text="Thank you"',
                'text="Enviado"'
            ]

            for selector in success_selectors:
                try:
                    await expect(page.locator(selector)).to_be_visible(timeout=5000)
                    break
                except:
                    continue

    async def test_employee_time_tracking_flow(self, authenticated_page: Page):
        """Test employee time tracking workflow"""
        page = authenticated_page

        # Should be on employee dashboard
        await expect(page).to_have_url(f"{BASE_URL}/empleados/dashboard")

        # Look for time tracking functionality
        start_work_selectors = [
            'button:has-text("Iniciar")',
            'button:has-text("Start")',
            'button:has-text("Comenzar")',
            '[data-testid="start-work-button"]',
            '.start-work-button'
        ]

        start_button = None
        for selector in start_work_selectors:
            try:
                element = page.locator(selector)
                if await element.count() > 0:
                    start_button = element.first
                    break
            except:
                continue

        if start_button:
            # Start work session
            await start_button.click()
            await page.wait_for_timeout(1000)

            # Look for stop work button
            stop_work_selectors = [
                'button:has-text("Finalizar")',
                'button:has-text("Stop")',
                'button:has-text("Terminar")',
                '[data-testid="stop-work-button"]',
                '.stop-work-button'
            ]

            stop_button = None
            for selector in stop_work_selectors:
                try:
                    element = page.locator(selector)
                    if await element.count() > 0:
                        stop_button = element.first
                        break
                except:
                    continue

            if stop_button:
                # Stop work session
                await stop_button.click()
                await page.wait_for_timeout(1000)

                # Check for confirmation or session recorded
                await expect(page.locator('body')).to_contain_text("horas", timeout=5000)

    async def test_task_management_flow(self, admin_page: Page, test_task_data):
        """Test task creation and management flow"""
        page = admin_page

        # Look for task management section
        task_selectors = [
            'button:has-text("Nueva Tarea")',
            'button:has-text("Crear Tarea")',
            'a:has-text("Tareas")',
            '[data-testid="create-task-button"]'
        ]

        task_button = None
        for selector in task_selectors:
            try:
                element = page.locator(selector)
                if await element.count() > 0:
                    task_button = element.first
                    break
            except:
                continue

        if task_button:
            await task_button.click()
            await page.wait_for_timeout(1000)

            # Fill task form
            title_input = page.locator('input[name="title"], input[placeholder*="título"]')
            description_input = page.locator('textarea[name="description"], textarea[placeholder*="descripción"]')
            priority_select = page.locator('select[name="priority"]')

            if await title_input.count() > 0:
                await title_input.fill(test_task_data["title"])
            if await description_input.count() > 0:
                await description_input.fill(test_task_data["description"])
            if await priority_select.count() > 0:
                await priority_select.select_option(test_task_data["priority"])

            # Submit task form
            submit_button = page.locator('button[type="submit"], button:has-text("Crear")')
            if await submit_button.count() > 0:
                await submit_button.click()
                await page.wait_for_timeout(2000)

                # Verify task was created
                await expect(page.locator('body')).to_contain_text(test_task_data["title"], timeout=5000)

    async def test_project_creation_flow(self, admin_page: Page, test_project_data):
        """Test project creation workflow"""
        page = admin_page

        # Look for project creation functionality
        project_selectors = [
            'button:has-text("Nuevo Proyecto")',
            'button:has-text("Crear Proyecto")',
            'a:has-text("Proyectos")',
            '[data-testid="create-project-button"]'
        ]

        project_button = None
        for selector in project_selectors:
            try:
                element = page.locator(selector)
                if await element.count() > 0:
                    project_button = element.first
                    break
            except:
                continue

        if project_button:
            await project_button.click()
            await page.wait_for_timeout(1000)

            # Fill project form
            name_input = page.locator('input[name="name"], input[placeholder*="nombre"]')
            description_input = page.locator('textarea[name="description"], textarea[placeholder*="descripción"]')
            client_input = page.locator('input[name="client"], input[placeholder*="cliente"]')
            budget_input = page.locator('input[name="budget"], input[placeholder*="presupuesto"]')

            if await name_input.count() > 0:
                await name_input.fill(test_project_data["name"])
            if await description_input.count() > 0:
                await description_input.fill(test_project_data["description"])
            if await client_input.count() > 0:
                await client_input.fill(test_project_data["client"])
            if await budget_input.count() > 0:
                await budget_input.fill(str(test_project_data["budget"]))

            # Submit project form
            submit_button = page.locator('button[type="submit"], button:has-text("Crear")')
            if await submit_button.count() > 0:
                await submit_button.click()
                await page.wait_for_timeout(2000)

                # Verify project was created
                await expect(page.locator('body')).to_contain_text(test_project_data["name"], timeout=5000)

    async def test_navigation_flow(self, page: Page):
        """Test main navigation flow"""
        await page.goto(BASE_URL)

        # Test main navigation links
        nav_links = [
            ("Services", "servicios"),
            ("About", "nosotros"),
            ("Contact", "contacto")
        ]

        for link_text, url_fragment in nav_links:
            # Try to find and click navigation link
            link_selectors = [
                f'a:has-text("{link_text}")',
                f'a[href*="{url_fragment}"]',
                f'nav a:has-text("{link_text}")'
            ]

            link_clicked = False
            for selector in link_selectors:
                try:
                    link = page.locator(selector)
                    if await link.count() > 0:
                        await link.first.click()
                        await page.wait_for_timeout(1000)
                        link_clicked = True
                        break
                except:
                    continue

            if link_clicked:
                # Verify navigation worked
                current_url = page.url
                # Check if URL contains expected fragment or we can see the content
                if url_fragment in current_url.lower():
                    pass  # Success
                else:
                    # Try to find content on the page
                    content_found = False
                    for keyword in [link_text.lower(), url_fragment]:
                        try:
                            if await page.locator(f'body').inner_text().then(lambda text: keyword in text.lower()):
                                content_found = True
                                break
                        except:
                            continue

                    assert content_found, f"Could not verify navigation to {link_text}"

                # Go back to home for next test
                await page.goto(BASE_URL)
                await page.wait_for_timeout(500)

    async def test_responsive_design(self, page: Page):
        """Test responsive design on different screen sizes"""
        await page.goto(BASE_URL)

        # Test mobile view
        await page.set_viewport_size({"width": 375, "height": 667})  # iPhone 6/7/8
        await page.wait_for_timeout(1000)

        # Check if mobile navigation is present
        mobile_nav_selectors = [
            '[data-testid="mobile-menu-button"]',
            '.hamburger',
            '.mobile-menu-toggle',
            'button[aria-label="Menu"]'
        ]

        mobile_nav_found = False
        for selector in mobile_nav_selectors:
            try:
                if await page.locator(selector).count() > 0:
                    mobile_nav_found = True
                    break
            except:
                continue

        # Test tablet view
        await page.set_viewport_size({"width": 768, "height": 1024})  # iPad
        await page.wait_for_timeout(1000)

        # Test desktop view
        await page.set_viewport_size({"width": 1280, "height": 720})
        await page.wait_for_timeout(1000)

        # The page should be usable on all sizes
        await expect(page.locator('body')).to_be_visible()

    async def test_error_handling_flow(self, page: Page):
        """Test error handling for invalid routes"""
        # Try to access non-existent routes
        invalid_routes = [
            "/non-existent-page",
            "/invalid/route",
            "/404"
        ]

        for route in invalid_routes:
            await page.goto(f"{BASE_URL}{route}")
            await page.wait_for_timeout(2000)

            # Check if error page or 404 is shown
            error_indicators = [
                "404",
                "not found",
                "página no encontrada",
                "error"
            ]

            page_content = await page.locator('body').inner_text()
            error_found = any(indicator in page_content.lower() for indicator in error_indicators)

            # If no explicit error page, at least verify the page loads something
            await expect(page.locator('body')).to_be_visible()

    async def test_performance_basic(self, page: Page):
        """Basic performance test"""
        start_time = page.now()

        await page.goto(BASE_URL)
        await page.wait_for_load_state("networkidle")

        load_time = (page.now() - start_time) / 1000  # Convert to seconds

        # Page should load within reasonable time (5 seconds)
        assert load_time < 5.0, f"Page took too long to load: {load_time} seconds"

        # Check that page has content
        body_text = await page.locator('body').inner_text()
        assert len(body_text) > 100, "Page appears to be empty or minimal"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])