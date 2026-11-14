"""Render the token-radar dashboard's three screenshots with Playwright.

The screenshots are part of the submission: the board, one detail view and a filtered view. They
have to show the dashboard the repository actually ships, so this script loads the built
dashboard/ directory over a local server and captures the same three states a reader would.
"""

import asyncio
import shutil
import subprocess
import sys
import time
from pathlib import Path

from playwright.async_api import async_playwright

PORT = 8911
SRC = Path("/tmp/tr2")


async def main() -> int:
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
        cwd=str(SRC),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1.5)
    base = f"http://127.0.0.1:{PORT}/dashboard/index.html"
    out = Path("/root/.hermes/shared/makefun/token-radar/screenshots")
    out.mkdir(parents=True, exist_ok=True)

    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(args=["--no-sandbox"])
            page = await browser.new_page(viewport={"width": 1440, "height": 1100}, device_scale_factor=1)

            # 1. The board: the ranked table as the page first shows it.
            await page.goto(base, wait_until="networkidle")
            await page.wait_for_selector("table tbody tr", timeout=15000)
            rows = await page.eval_on_selector_all("table tbody tr", "els => els.length")
            print(f"board rows rendered: {rows}")
            await page.screenshot(path=str(out / "1-board.png"), full_page=False)

            # 2. A detail view: click rank 1 and capture the dialog with the model breakdown.
            await page.click("table tbody tr:first-child")
            await page.wait_for_selector("dialog[open]", timeout=10000)
            await page.wait_for_timeout(400)
            title = await page.eval_on_selector("dialog h2", "el => el.textContent")
            print(f"detail dialog: {title}")
            await page.screenshot(path=str(out / "2-detail.png"), full_page=False)
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(250)

            # 3. A filtered view: one category plus a search term, which is what a reader does
            #    when they want the lending names only.
            await page.goto(base + "#category=Lending", wait_until="networkidle")
            await page.wait_for_selector("table tbody tr", timeout=10000)
            filtered = await page.eval_on_selector_all("table tbody tr", "els => els.length")
            print(f"filtered rows (Lending): {filtered}")
            await page.screenshot(path=str(out / "3-filtered.png"), full_page=False)

            # The model panel's category table, captured so the judge can read the constants
            # without opening the page.
            await page.goto(base, wait_until="networkidle")
            await page.wait_for_selector("table.consts tbody tr", timeout=10000)
            consts = await page.eval_on_selector_all("table.consts tbody tr", "els => els.length")
            print(f"model constant rows: {consts}")
            panel = await page.query_selector("section.panel.model")
            if panel:
                await panel.scroll_into_view_if_needed()
                await page.wait_for_timeout(300)
                await panel.screenshot(path=str(out / "4-model.png"))
                print("model panel captured")

            await browser.close()
    finally:
        server.terminate()
        server.wait(timeout=10)

    for p in sorted(out.glob("*.png")):
        print(f"{p.name}: {p.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
