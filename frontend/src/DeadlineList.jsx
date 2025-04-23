import React, { useState } from 'react';

const DeadlineList = ({ deadlines, onDelete, onEdit }) => {
  const [editingIndex, setEditingIndex] = useState(null);
  const [editedText, setEditedText] = useState('');

  return (
    <div>
      <h3>📅 Saved Deadlines</h3>
      <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
        {deadlines.map((d, index) => {
          const isEditing = editingIndex === index;

          return (
            <li
              key={index}
              style={{
                backgroundColor: d.used_ai ? '#fff4e5' : 'transparent',
                padding: '0.5rem',
                marginBottom: '0.3rem',
                borderLeft: d.used_ai ? '5px solid orange' : '5px solid #ccc',
              }}
            >
              <strong>{d.parsed_date}</strong> —{' '}
              {isEditing ? (
                <input
                  type="text"
                  value={editedText}
                  onChange={(e) => setEditedText(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      onEdit(index, editedText);
                      setEditingIndex(null);
                    }
                  }}
                  style={{ marginRight: '0.5rem' }}
                />
              ) : (
                <em>{d.text}</em>
              )}

              {d.used_ai && (
                <span
                  style={{
                    color: 'orange',
                    fontWeight: 'bold',
                    marginLeft: '0.5rem',
                  }}
                >
                  (AI)
                </span>
              )}

              {/* 📅 Google Calendar Link */}
              {d.event_link && !isEditing && (
                <a
                  href={d.event_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ marginLeft: '0.75rem', fontSize: '0.9rem' }}
                >
                  📅 View
                </a>
              )}

              {/* 🛠️ Action buttons */}
              <span style={{ float: 'right' }}>
                {isEditing ? (
                  <button onClick={() => setEditingIndex(null)}>Cancel</button>
                ) : (
                  <button
                    onClick={() => {
                      setEditedText(d.text);
                      setEditingIndex(index);
                    }}
                  >
                    ✏️ Edit
                  </button>
                )}
                <button
                  onClick={() => {
                    if (window.confirm('Delete this deadline?')) {
                      onDelete(index);
                    }
                  }}
                  style={{ marginLeft: '0.5rem', color: 'red' }}
                >
                  🗑️ Delete
                </button>
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default DeadlineList;
