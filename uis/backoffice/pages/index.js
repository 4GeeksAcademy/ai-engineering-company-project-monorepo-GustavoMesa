import { useEffect, useState } from 'react';

const BACKEND_URL = process.env.BACKEND_URL || 'http://services:8000';

export default function Backoffice() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/status`)
      .then((res) => res.json())
      .then((data) => {
        setStatus(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', maxWidth: 640, margin: '4rem auto', padding: '0 1rem' }}>
      <h1>🍖 Brasaland — Backoffice</h1>
      <p style={{ color: '#666' }}>Panel de administración interna</p>

      <h2>Estado del Sistema</h2>

      {loading && <p>Consultando backend…</p>}

      {error && (
        <div style={{ padding: '1rem', background: '#fdd', borderRadius: 8 }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {status && (
        <table style={{ borderCollapse: 'collapse', width: '100%' }}>
          <tbody>
            <tr>
              <td style={{ padding: '0.5rem', borderBottom: '1px solid #ddd' }}>API</td>
              <td style={{ padding: '0.5rem', borderBottom: '1px solid #ddd', fontWeight: 'bold', color: status.status === 'ok' ? '#090' : '#900' }}>
                {status.status}
              </td>
            </tr>
            <tr>
              <td style={{ padding: '0.5rem', borderBottom: '1px solid #ddd' }}>Base de datos</td>
              <td style={{ padding: '0.5rem', borderBottom: '1px solid #ddd', fontWeight: 'bold', color: status.database === 'connected' ? '#090' : '#900' }}>
                {status.database}
              </td>
            </tr>
            <tr>
              <td style={{ padding: '0.5rem', borderBottom: '1px solid #ddd' }}>Versión</td>
              <td style={{ padding: '0.5rem', borderBottom: '1px solid #ddd' }}>{status.version}</td>
            </tr>
            <tr>
              <td style={{ padding: '0.5rem' }}>Uptime</td>
              <td style={{ padding: '0.5rem' }}>{status.uptime_seconds}s</td>
            </tr>
          </tbody>
        </table>
      )}

      <hr style={{ margin: '2rem 0' }} />
      <p style={{ color: '#999', fontSize: '0.9rem' }}>
        Backoffice — solo para administradores
      </p>
    </div>
  );
}