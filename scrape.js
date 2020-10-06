const puppeteer = require('puppeteer');
const path = require("path");

async function main() {
    // Launch browser
    const browser = await puppeteer.launch({
        headless: false,
        userDataDir: path.join(process.cwd(), "ChromeSession")
    });
    const page = await browser.newPage();

    // Go to WhatsApp Web
    await page.goto('https://web.whatsapp.com', {
        waitUntil: 'networkidle0',
        timeout: 0
    });

    // Wait until login using QR Code
    await page.waitForSelector('*[data-icon=chat]',
    {
        polling: 1000,
        timeout: 0
    })
    console.log("Logged in!")

    // Inject API file
    var filepath = path.join(__dirname, "WAPI.js");
    await page.addScriptTag({ path: require.resolve(filepath) });

    // Inject scraper
    filepath = path.join(__dirname, "inject.js");
    await page.addScriptTag({path: require.resolve(filepath)});
};

main();
