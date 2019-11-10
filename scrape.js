const puppeteer = require('puppeteer');
var path = require("path");

async function main() {
    const browser = await puppeteer.launch({
        headless: false,
        userDataDir: path.join(process.cwd(), "ChromeSession")
    });
    const page = await browser.newPage();
    await page.goto('https://web.whatsapp.com', {
        waitUntil: 'networkidle0',
        timeout: 0
    });

    await page.waitForSelector('*[data-icon=chat]',
    {
        polling: 1000,
        timeout: 0
    })

    console.log("Logged in!")
    var filepath = path.join(__dirname, "WAPI.js");
    await page.addScriptTag({ path: require.resolve(filepath) });

    filepath = path.join(__dirname, "inject.js");
    await page.addScriptTag({path: require.resolve(filepath)});

    //await browser.close();
};

// async function checkLogin(page) {
//     console.log("Page is loading");
//     await new Promise(resolve => setTimeout(resolve, 10000));
//     var output = await page.evaluate("localStorage['last-wid']");

//     if (output) {
//         console.log("You are already logged in!");
//     } else {
//         console.log("You are not logged in. Please scan the QR code.");
//     }
//     return output;
// }

main();
