import React, { useState, useEffect, useRef } from 'react';

export default function ExplorePage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatEndRef = useRef(null);

  // Функция для прокрутки чата вниз
  const scrollToBottom = () => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Обработка отправки сообщения
  const sendMessage = async () => {
    if (input.trim() === '') return;

    // Добавляем сообщение пользователя
    const userMessage = { sender: 'user', text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // Сохраняем текущий ввод и очищаем поле
    const question = input;
    setInput('');

    try {
      // Отправка запроса к API
      const response = await fetch(`http://localhost:8053/?question=${encodeURIComponent(question)}`, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Ошибка сети');
      }

      const data = await response.json();

      // Добавляем ответ бота
      const botMessage = { sender: 'bot', text: data.result };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Ошибка при получении ответа от бота:', error);
      const errorMessage = { sender: 'bot', text: 'Извините, произошла ошибка при обработке вашего запроса.' };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  // Обработка нажатия Enter для отправки сообщения
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Data Exploration</h1>
      <div className="flex flex-row w-full h-96 border">
        {/* Область чата */}
        <div className="w-1/2 border-r flex flex-col p-2">
          <h2 className="text-lg mb-2">Чат с ботом</h2>
          <div className="flex-1 overflow-y-auto mb-2">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`mb-2 flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`p-2 rounded ${
                    msg.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-300 text-black'
                  } max-w-xs`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>
          <div className="flex">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1 border rounded-l px-2 py-1"
              placeholder="Введите ваш вопрос..."
            />
            <button
              onClick={sendMessage}
              className="bg-blue-500 text-white px-4 py-1 rounded-r"
            >
              Отправить
            </button>
          </div>
        </div>

        {/* Область графа знаний */}
        <div className="w-1/2 p-2">
          <h2 className="text-lg mb-2">Граф знаний</h2>
          {/* Здесь будет ваш граф знаний */}
          <div className="h-full bg-gray-100 flex items-center justify-center">
            Граф знаний (заглушка)
          </div>
        </div>
      </div>
    </div>
  );
}
