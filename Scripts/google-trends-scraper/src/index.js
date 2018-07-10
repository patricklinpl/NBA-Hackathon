import 'babel-polyfill'
import countries from './data/country-code'
import teams from './data/nba-teams'
import puppeteer from 'puppeteer'


const buildQueryString = () => {
    const queryList = []
    const base = `https://trends.google.com/trends/explore?date=2016-10-01%202017-05-01`

    Object.keys(teams).forEach(team => {
        var searchQ = `${base}&geo=`
        var count = 0
        countries.forEach(country => {
            searchQ += `${country['ISO3166-1-Alpha-2']},`
            count++
            break
        })
        searchQ = searchQ.substring(0, searchQ.length - 1)
        for (var i = 0; i < count; i++) {
            searchQ += `&q=${teams[team]},`
        }
        searchQ = searchQ.substring(0, searchQ.length - 1)
        queryList.push(searchQ)
    })
    
    console.log(queryList[0])

}

const scrape = async () => {
    const browser = await puppeteer.launch({headless: false})
    const page = await browser.newPage()
    await page.goto(`https://trends.google.com/trends/explore?date=2016-10-01%202017-05-01&geo=NZ&q=%2Fm%2F04cxw5b`)
    await page.reload()
}

buildQueryString()
console.log('hi')

