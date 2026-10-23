from playwright.sync_api import sync_playwright
import os
D=os.path.dirname(os.path.abspath(__file__))+'/../res/'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':512,'height':512})
    for n in ['full','fg']:
        pg.goto('file://'+D+n+'.svg');pg.screenshot(path=D+n+'.png',omit_background=(n=='fg'))
    b.close()
