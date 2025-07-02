import { useState, type ChangeEvent } from 'react'
import './App.css'

import CreateShortenedURLPage from './tabs/CreateShortenedURLPage'

export default function App() {
  // Most actions need to know the URL
  const [url, setUrl] = useState('')
  // I want each action to be its own tab
  const [currentTab, setCurrentTab] = useState(<CreateShortenedURLPage url={url} />)
  const updateTab = (e: ChangeEvent<HTMLInputElement>) => setUrl(e.target.value)

  return (
    <>
      <h1>URL Shortening Service</h1>
      <p>
        <label htmlFor='url'>URL: </label>
        <input type='url' name='url' onChange={updateTab} />
      </p>
      <p className='tabs'>
        <button onClick={() => setCurrentTab(<CreateShortenedURLPage url={url} />)}>
          Create
        </button>
      </p>

      {currentTab}
    </>
  )
}

