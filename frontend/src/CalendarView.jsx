import React, { useState } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import enUS from 'date-fns/locale/en-US';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const locales = {
  'en-US': enUS,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

const CalendarView = ({ deadlines }) => {
  const [view, setView] = useState('month');
  const [date, setDate] = useState(new Date());

  const events = deadlines.map((d, i) => ({
    id: i,
    title: d.used_ai ? `[AI] ${d.text}` : d.text,
    start: new Date(d.parsed_date),
    end: new Date(d.parsed_date),
    allDay: true,
  }));

  return (
    <div
      style={{
        padding: '1rem',
        marginTop: '2rem',
        borderRadius: '12px',
        backgroundColor: '#ffffff',
        boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
        maxWidth: '100%',
        overflow: 'hidden',
      }}
    >
      <h3 style={{ marginBottom: '1rem', fontSize: '1.4rem' }}>🗓️ Court Calendar</h3>
      <div
        style={{
          height: '75vh',
          minHeight: '500px',
          width: '100%',
        }}
      >
        <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          views={['month', 'week', 'day']}
          view={view}
          date={date}
          onView={setView}
          onNavigate={setDate}
          popup
          toolbar
          style={{ height: '100%', width: '100%' }}
          eventPropGetter={(event) => ({
            style: {
              backgroundColor: event.title.startsWith('[AI]')
                ? '#fff3db'
                : '#d9eaff',
              color: '#000',
              borderRadius: '6px',
              padding: '4px',
              border: 'none',
              fontSize: '0.9rem',
            },
          })}
        />
      </div>
    </div>
  );
};

export default CalendarView;
