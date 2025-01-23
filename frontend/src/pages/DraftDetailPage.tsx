import React, { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import LoadingIndicator from '../components/LoadingIndicator'

type TableDraft = {
  name: string
  description: string
  industry?: string
  team?: string
  responsible_person: string
  fields: { name: string; description?: string }[]
  sources_tables?: string[]
}

type Industry = {
  id: string
  name: string
}

type Team = {
  id: string
  name: string
}

export default function DraftDetailPage() {
  const location = useLocation()
  const queryParams = new URLSearchParams(location.search)
  const encodedTableName = queryParams.get('tableName') || ''
  const decodedTableName = decodeURIComponent(encodedTableName)

  const navigate = useNavigate()
  const [drafts, setDrafts] = useState<TableDraft[]>([])
  const [draft, setDraft] = useState<TableDraft | null>(null)
  const [industries, setIndustries] = useState<Industry[]>([])
  const [teams, setTeams] = useState<Team[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isConfirmed, setIsConfirmed] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const userEmail = localStorage.getItem('atlasUserEmail') || ''

  useEffect(() => {
    if (!userEmail) {
      navigate('/login')
      return
    }

    setError(null)

    // 1) Получаем драфты пользователя
    fetch(`http://localhost:8073/api/drafts/?email=${userEmail}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Ошибка при получении драфтов: ${res.status}`)
        }
        return res.json()
      })
      .then((data) => {
        setDrafts(data)
      })
      .catch((err) => {
        console.error('Error fetching drafts:', err)
        setError('Не удалось загрузить драфты')
      })

    // 2) Запрос списка индустрий
    fetch('http://localhost:8073/api/entities/industries')
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Ошибка при получении индустрий: ${res.status}`)
        }
        return res.json()
      })
      .then((data) => {
        setIndustries(data)
      })
      .catch((err) => {
        console.error('Error fetching industries:', err)
        setError('Не удалось загрузить индустрии')
      })

    // 3) Запрос списка команд
    fetch('http://localhost:8073/api/entities/teams')
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Ошибка при получении команд: ${res.status}`)
        }
        return res.json()
      })
      .then((data) => {
        setTeams(data)
      })
      .catch((err) => {
        console.error('Error fetching teams:', err)
        setError('Не удалось загрузить команды')
      })
  }, [userEmail, navigate])

  useEffect(() => {
    const found = drafts.find((d) => d.name === decodedTableName)
    if (found) {
      setDraft(found)
    }
  }, [drafts, decodedTableName])

  function handleIndustryChange(e: React.ChangeEvent<HTMLSelectElement>) {
    if (draft) {
      setDraft({ ...draft, industry: e.target.value })
    }
  }

  function handleTeamChange(e: React.ChangeEvent<HTMLSelectElement>) {
    if (draft) {
      setDraft({ ...draft, team: e.target.value })
    }
  }

  function handleFieldNameChange(index: number, newName: string) {
    if (!draft) return
    const updatedFields = [...draft.fields]
    updatedFields[index] = {
      ...updatedFields[index],
      name: newName
    }
    setDraft({ ...draft, fields: updatedFields })
  }

  function handleFieldDescriptionChange(index: number, newDesc: string) {
    if (!draft) return
    const updatedFields = [...draft.fields]
    updatedFields[index] = {
      ...updatedFields[index],
      description: newDesc
    }
    setDraft({ ...draft, fields: updatedFields })
  }

  function handleRemoveField(index: number) {
    if (!draft) return
    const updatedFields = draft.fields.filter((_, i) => i !== index)
    setDraft({ ...draft, fields: updatedFields })
  }

  function handleRemoveSourceTable(index: number) {
    if (!draft || !draft.sources_tables) return
    const updatedSources = draft.sources_tables.filter((_, i) => i !== index)
    setDraft({ ...draft, sources_tables: updatedSources })
  }

  async function confirmDraft() {
    if (!draft) return
    setIsLoading(true)
    setIsConfirmed(false)
    setError(null)

    try {
      // 1) Создаём сущность Table
      const tableResp = await fetch('http://localhost:8073/api/entities/tables', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: draft.name, description: draft.description })
      })
      if (!tableResp.ok) {
        throw new Error(`Ошибка при создании таблицы: ${tableResp.status}`)
      }

      // 2) Связи с индустрией, командой, ответственным, источниками
      const relPromises: Promise<any>[] = []

      if (draft.industry) {
        relPromises.push(
          fetch('http://localhost:8073/api/relationships/table/belongs_to', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ table_name: draft.name, industry_id: draft.industry })
          }).then((r) => {
            if (!r.ok) throw new Error(`Ошибка belongs_to: ${r.status}`)
          })
        )
      }

      if (draft.team) {
        relPromises.push(
          fetch('http://localhost:8073/api/relationships/table/maintained_by', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ table_name: draft.name, team_id: draft.team })
          }).then((r) => {
            if (!r.ok) throw new Error(`Ошибка maintained_by: ${r.status}`)
          })
        )
      }

      // Связка таблицы с ответственным
      relPromises.push(
        fetch('http://localhost:8073/api/relationships/table/has_responsible', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            table_name: draft.name,
            person_email: userEmail
          })
        }).then((r) => {
          if (!r.ok) throw new Error(`Ошибка has_responsible: ${r.status}`)
        })
      )

      // Источники
      if (draft.sources_tables) {
        draft.sources_tables.forEach((src) => {
          relPromises.push(
            fetch('http://localhost:8073/api/relationships/table/source_of', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                source_name: src,
                target_name: draft.name
              })
            }).then((r) => {
              if (!r.ok) throw new Error(`Ошибка source_of: ${r.status}`)
            })
          )
        })
      }

      await Promise.all(relPromises)

      // 3) Создание полей и связь add_field
      // Для каждого field: создаём, достаём id → создаём связь (table/add_field)
      const fieldPromises = draft.fields.map(async (f) => {
        const createFieldResp = await fetch('http://localhost:8073/api/entities/fields', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: f.name, description: f.description })
        })
        if (!createFieldResp.ok) {
          throw new Error(`Ошибка при создании поля ${f.name}: ${createFieldResp.status}`)
        }
        const fieldData = await createFieldResp.json() // {id, name, description}

        const addFieldRelResp = await fetch('http://localhost:8073/api/relationships/table/add_field', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            table_name: draft.name,
            field_id: fieldData.id
          })
        })
        if (!addFieldRelResp.ok) {
          throw new Error(`Ошибка add_field: ${addFieldRelResp.status}`)
        }
      })

      await Promise.all(fieldPromises)

      // 4) Удаляем драфт
      const deleteResp = await fetch(
        `http://localhost:8073/api/drafts/?email=${userEmail}&table_name=${encodeURIComponent(draft.name)}`,
        { method: 'DELETE' }
      )
      if (!deleteResp.ok) {
        throw new Error(`Ошибка при удалении драфта: ${deleteResp.status}`)
      }

      setIsLoading(false)
      setIsConfirmed(true)
      setTimeout(() => {
        navigate('/drafts')
      }, 1500)
    } catch (err: any) {
      console.error(err)
      setError(`Произошла ошибка: ${err.message}`)
      setIsLoading(false)
    }
  }

  if (error) {
    return (
      <div className="p-4">
        <p className="text-red-600 font-semibold">Ошибка: {error}</p>
        <button
          onClick={() => {
            setError(null)
            navigate('/drafts')
          }}
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
        >
          Вернуться к списку драфтов
        </button>
      </div>
    )
  }

  if (!draft) {
    return (
      <div className="p-4">
        <h1 className="text-xl">Драфт не найден</h1>
      </div>
    )
  }

  if (isLoading) {
    return <LoadingIndicator />
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Драфт: {draft.name}</h1>
      <div className="mb-4">
        <label className="block">Описание</label>
        <textarea className="border w-full p-2" value={draft.description} readOnly />
      </div>
      <div className="mb-4">
        <label className="block mb-1">Industry</label>
        <select
          className={`border p-2 ${!draft.industry ? 'border-red-500' : ''}`}
          value={draft.industry || ''}
          onChange={handleIndustryChange}
        >
          <option value="">Выберите индустрию</option>
          {industries.map((ind) => (
            <option key={ind.id} value={ind.id}>
              {ind.name}
            </option>
          ))}
        </select>
      </div>
      <div className="mb-4">
        <label className="block mb-1">Team</label>
        <select
          className={`border p-2 ${!draft.team ? 'border-red-500' : ''}`}
          value={draft.team || ''}
          onChange={handleTeamChange}
        >
          <option value="">Выберите команду</option>
          {teams.map((t) => (
            <option key={t.id} value={t.id}>
              {t.name}
            </option>
          ))}
        </select>
      </div>
      <div className="mb-4">
        <h2 className="text-lg mb-2">Поля</h2>
        {draft.fields.map((field, i) => (
          <div key={i} className="border p-2 mb-2 border-gray-300">
            <label className="block mb-1 font-semibold">Название поля</label>
            <input
              className={`border w-full p-2 mb-2 ${!field.name ? 'border-red-500' : ''}`}
              type="text"
              value={field.name}
              onChange={(e) => handleFieldNameChange(i, e.target.value)}
            />
            <label className="block mb-1 font-semibold">Описание поля</label>
            <textarea
              className="border w-full p-2 mb-2"
              value={field.description || ''}
              onChange={(e) => handleFieldDescriptionChange(i, e.target.value)}
            />
            <button
              className="bg-red-500 text-white px-3 py-1 rounded"
              onClick={() => handleRemoveField(i)}
            >
              Удалить поле
            </button>
          </div>
        ))}
      </div>
      {/* Новая секция для sources_tables */}
      <div className="mb-4">
        <h2 className="text-lg mb-2">Источники</h2>
        {draft.sources_tables && draft.sources_tables.length > 0 ? (
          <ul>
            {draft.sources_tables.map((src, i) => (
              <li key={i} className="flex items-center justify-between mb-2">
                <span>{src}</span>
                <button
                  className="bg-red-500 text-white px-2 py-1 rounded"
                  onClick={() => handleRemoveSourceTable(i)}
                >
                  Удалить
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p>Нет источников</p>
        )}
      </div>
      <button
        onClick={confirmDraft}
        className="bg-green-600 text-white py-2 px-4 rounded"
      >
        Подтвердить драфт
      </button>
      {isConfirmed && <div className="mt-4 text-green-600 font-bold">Драфт подтверждён</div>}
    </div>
  )
}
