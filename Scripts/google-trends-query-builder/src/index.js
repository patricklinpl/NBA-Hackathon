import 'babel-polyfill'
import fs from 'fs'
import mkdirp from 'mkdirp'
import teams from './data/nba-teams'

const buildQueryString = async () => {
  const base = `https://trends.google.com/trends/explore?date=2016-10-01%202017-05-01&q=`
  const atlanta = `%2Fm%2F0jm64,`
  let searchQ = `${base}${atlanta}`
  const queryHolder = ['Google Trends']
  let count = 0
  const nbaTeam = Object.keys(teams)
  for (let i = 0; i < nbaTeam.length; i++) {
    searchQ += `${teams[nbaTeam[i]]},`
    count++
    if (count === 4 || i === nbaTeam.length - 1) {
      searchQ = searchQ.substring(0, searchQ.length - 1)
      queryHolder.push(searchQ)
      searchQ = `${base}${atlanta}`
      count = 0
    }
  }

  if (!fs.existsSync('./results/')) {
    await mkdirp('./results', (err) => {
      if (err) console.error(err)
    })
  }

  await fs.writeFile(`./results/queryTrends.csv`, queryHolder, 'utf8', (err) => {
    if (err) throw err
  })
}

buildQueryString()
