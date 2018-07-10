import 'babel-polyfill'
import puppeteer from 'puppeteer'

const scrape = async () => {
    const browser = await puppeteer.launch({headless: false})
    const page = await browser.newPage()
    await page.goto(`https://trends.google.com/trends/explore?date=2016-10-01%202017-05-01&geo=NZ&q=%2Fm%2F04cxw5b`)
    await page.reload()
}

scrape()
console.log('hi')

