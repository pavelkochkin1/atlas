import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const navigate = useNavigate()

  function handleLogin() {
    if (email.trim()) {
      localStorage.setItem('atlasUserEmail', email.trim())
      navigate('/explore')
    }
  }

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-2xl mb-4">Авторизация</h1>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Введите вашу почту"
        className="border p-2 rounded mb-4"
      />
      <button
        onClick={handleLogin}
        className="bg-blue-600 text-white py-2 px-4 rounded"
      >
        Войти
      </button>
    </div>
  )
}
