// NOTE: By contributing to this repository, you agree to the terms outlined in the private license agreement.
// Please contact the project lead for the full agreement document.


import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
