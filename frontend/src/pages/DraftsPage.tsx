import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

type TableDraft = {
  name: string
  description: string
  industry?: string
  team?: string
  responsible_person: string
  fields: { name: string; description?: string }[]
  sources_tables?: string[]
}

export default function DraftsPage() {
  const navigate = useNavigate()
  const [drafts, setDrafts] = useState<TableDraft[]>([])
  const userEmail = localStorage.getItem('atlasUserEmail') || ''

  useEffect(() => {
    if (!userEmail) {
      navigate('/login')
    } else {
      fetch(`http://localhost:8073/api/drafts/?email=${userEmail}`)
        .then((res) => res.json())
        .then((data) => {
          setDrafts(data)
        })
        .catch(() => {})
    }
  }, [userEmail, navigate])

  function goToDraftDetail(tableName: string) {
    navigate(`/draft-detail?tableName=${encodeURIComponent(tableName)}`)
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Драфты для проверки</h1>
      <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {drafts.map((draft) => (
          <div
            key={draft.name}
            className="bg-white p-4 rounded shadow cursor-pointer hover:bg-gray-100"
            onClick={() => goToDraftDetail(draft.name)}
          >
            <h2 className="text-lg font-bold">{draft.name}</h2>
            <p className="text-sm text-gray-600">{draft.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
