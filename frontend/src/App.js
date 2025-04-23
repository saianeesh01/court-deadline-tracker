import React, { useEffect, useState } from 'react';
import DeadlineForm from './DeadlineForm';
import DeadlineList from './DeadlineList';
import CalendarView from './CalendarView';
import './index.css';

function App() {
  const [deadlines, setDeadlines] = useState([]);
  const [filter, setFilter] = useState('all'); // 'all', 'ai', 'upcoming', 'ai-upcoming'

  const fetchDeadlines = async () => {
    const response = await fetch('/api/deadlines');
    const data = await response.json();
    console.log('Loaded deadlines:', data);
    setDeadlines(data);
  };

  useEffect(() => {
    fetchDeadlines();
  }, []);

  const handleNewDeadline = (newDeadline) => {
    setDeadlines((prev) => [...prev, newDeadline]);
  };

  const handleDeleteDeadline = (indexToDelete) => {
    setDeadlines((prev) => prev.filter((_, index) => index !== indexToDelete));
  };

  const handleEditDeadline = (indexToEdit, updatedText) => {
    setDeadlines((prev) =>
      prev.map((d, i) =>
        i === indexToEdit ? { ...d, text: updatedText } : d
      )
    );
  };

  // ✅ Filter logic
  const filteredDeadlines = deadlines.filter((d) => {
    const today = new Date();
    const parsedDate = new Date(d.parsed_date);
    const isUpcoming = parsedDate >= today;

    if (filter === 'ai') return d.used_ai;
    if (filter === 'upcoming') return isUpcoming;
    if (filter === 'ai-upcoming') return d.used_ai && isUpcoming;
    return true; // 'all'
  });

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Court Deadline Tracker</h1>
      <DeadlineForm onNewDeadline={handleNewDeadline} />

      {/* 🔍 Filter Dropdown */}
      <div style={{ margin: '1rem 0' }}>
        <label style={{ fontWeight: 'bold', marginRight: '0.5rem' }}>Filter:</label>
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">All Deadlines</option>
          <option value="ai">AI Only</option>
          <option value="upcoming">Upcoming Only</option>
          <option value="ai-upcoming">AI + Upcoming</option>
        </select>
      </div>

      <DeadlineList
        deadlines={filteredDeadlines}
        onDelete={handleDeleteDeadline}
        onEdit={handleEditDeadline}
      />
      <CalendarView deadlines={filteredDeadlines} />
    </div>
  );
}

export default App;
