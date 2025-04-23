import React, { useState } from 'react';

const DeadlineForm = ({ onNewDeadline }) => {
  const [text, setText] = useState('');
  const [notify, setNotify] = useState(true);
  const [syncToCalendar, setSyncToCalendar] = useState(false); // ✅ NEW
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
  
    try {
      const response = await fetch('/api/parse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, notify })
      });
  
      const data = await response.json();
  
      if (response.ok) {
        let deadlineData = data;
  
        if (syncToCalendar) {
          const result = await fetch('/sync_event', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              text: data.text,
              parsed_date: data.parsed_date
            })
          });
  
          const resultData = await result.json();
          deadlineData = { ...data, event_link: resultData.link };
        }
  
        onNewDeadline(deadlineData);
        setText('');
      } else {
        setError(data.error || 'Failed to parse deadline');
      }
    } catch (err) {
      setError('Server error');
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder='e.g. "Reply due 14 days after April 1"'
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={loading}
        style={{ padding: '0.5rem', width: '70%' }}
      />
      <label style={{ marginLeft: '0.5rem' }}>
        <input
          type="checkbox"
          checked={notify}
          onChange={(e) => setNotify(e.target.checked)}
        /> Notify Me
      </label>
      <label style={{ marginLeft: '0.5rem' }}>
        <input
          type="checkbox"
          checked={syncToCalendar}
          onChange={(e) => setSyncToCalendar(e.target.checked)}
        /> Sync to Calendar
      </label>
      <button type="submit" disabled={loading} style={{ marginLeft: '0.5rem' }}>
        {loading ? 'Adding...' : 'Add Deadline'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  );
};

export default DeadlineForm;
