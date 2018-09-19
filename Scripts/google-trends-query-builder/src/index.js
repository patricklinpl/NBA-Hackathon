import 'babel-polyfill'
import fs from 'fs'
import mkdirp from 'mkdirp'
import teams from './data/nba-teams'

const buildQueryString = async (date) => {
  const base = `https://trends.google.com/trends/explore?date=${date}&geo=US&q=`
  const baseTeam = `%2Fm%2F0jm2v,`
  let searchQ = `${base}${baseTeam}`
  const queryHolder = ['Google Trends']
  let count = 0
  const nbaTeam = Object.keys(teams)
  for (let i = 0; i < nbaTeam.length; i++) {
    if (`${teams[nbaTeam[i]]},` !== baseTeam) {
      searchQ += `${teams[nbaTeam[i]]},`
      count++
      if (count === 2 || i === nbaTeam.length - 1) {
        searchQ = searchQ.substring(0, searchQ.length - 1)
        queryHolder.push(searchQ)
        searchQ = `${base}${baseTeam}`
        count = 0
      }
    }
  }

  if (!fs.existsSync('./results/')) {
    await mkdirp('./results', (err) => {
      if (err) console.error(err)
    })
  }

  await fs.writeFile(`./results/queryTrends${date}.csv`, queryHolder, 'utf8', (err) => {
    if (err) throw err
  })
}

// buildQueryString(`2016-10-01%202017-05-01`)
buildQueryString(`2017-10-01%202018-05-01`)
