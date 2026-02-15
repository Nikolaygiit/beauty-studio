from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on("console", lambda msg: print(f"Console: {msg.text}"))

        try:
            page.goto("http://localhost:8000")

            # Wait for modal to be active (initial state)
            page.wait_for_selector("#settings-modal.active", timeout=5000)
            print("Modal found active.")

            # Take screenshot of initial modal
            page.screenshot(path="verification/initial_modal.png")

            # Close modal using the correct selector (id or class)
            page.click("#close-modal")

            # Wait for modal to disappear (remove 'active' class)
            page.wait_for_function("!document.querySelector('#settings-modal').classList.contains('active')")

            # Wait for welcome message
            page.wait_for_selector(".welcome-message")
            print("Welcome message found.")

            # Take screenshot of welcome screen
            page.screenshot(path="verification/welcome.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")

        browser.close()

if __name__ == "__main__":
    run()
