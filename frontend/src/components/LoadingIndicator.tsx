import React from 'react'

export default function LoadingIndicator() {
  return (
    <div className="flex items-center justify-center space-x-2 p-4">
      <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-blue-700"></div>
      <span>Загрузка...</span>
    </div>
  )
}
