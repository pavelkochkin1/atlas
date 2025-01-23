import React from 'react'
import { Routes, Route, Navigate, Link } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import DraftsPage from './pages/DraftsPage'
import DraftDetailPage from './pages/DraftDetailPage'
import ExplorePage from './pages/ExplorePage'

export default function App() {
  return (
    <div className="min-h-screen">
      <nav className="bg-gray-800 text-white p-4 flex space-x-4">
        <Link to="/drafts" className="hover:text-gray-300">Драфты</Link>
        <Link to="/explore" className="hover:text-gray-300">Explore</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/drafts" element={<DraftsPage />} />
        <Route path="/draft-detail" element={<DraftDetailPage />} />
        <Route path="/explore" element={<ExplorePage />} />
      </Routes>
    </div>
  )
}
