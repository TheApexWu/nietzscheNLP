'use client'

import { useState } from 'react'

const translators = ['German', 'Hollingdale', 'Kaufmann', 'Faber', 'Norman', 'Zimmern']

// Similarity matrix data (symmetric)
const matrix = [
  [1.000, 0.833, 0.808, 0.813, 0.798, 0.798], // German
  [0.833, 1.000, 0.886, 0.878, 0.842, 0.851], // Hollingdale
  [0.808, 0.886, 1.000, 0.871, 0.839, 0.844], // Kaufmann
  [0.813, 0.878, 0.871, 1.000, 0.845, 0.852], // Faber
  [0.798, 0.842, 0.839, 0.845, 1.000, 0.806], // Norman
  [0.798, 0.851, 0.844, 0.852, 0.806, 1.000], // Zimmern
]

function getColor(value) {
  // Interpolate from cream (#fdf6e3) to gold (#f4a623) to wine (#722f37)
  if (value >= 0.95) return '#722f37'
  if (value >= 0.88) return '#c9784a'
  if (value >= 0.84) return '#f4a623'
  if (value >= 0.80) return '#e6c87a'
  return '#fdf6e3'
}

export default function HeatmapChart() {
  const [hoveredCell, setHoveredCell] = useState(null)
  const cellSize = 70

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '1rem'
    }}>
      {/* Column headers */}
      <div style={{ display: 'flex', marginLeft: cellSize + 10, marginTop: 40 }}>
        {translators.map((t, i) => (
          <div
            key={t}
            style={{
              width: cellSize,
              height: 100,
              display: 'flex',
              alignItems: 'flex-end',
              justifyContent: 'flex-start',
              paddingBottom: 8,
              transform: 'rotate(-45deg)',
              transformOrigin: 'left bottom',
              fontSize: '0.85rem',
              fontWeight: hoveredCell?.col === i ? 600 : 400,
              color: hoveredCell?.col === i ? '#722f37' : '#2d2418',
              transition: 'all 0.2s ease',
              whiteSpace: 'nowrap'
            }}
          >
            {t}
          </div>
        ))}
      </div>

      {/* Matrix */}
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {matrix.map((row, rowIdx) => (
          <div key={rowIdx} style={{ display: 'flex', alignItems: 'center' }}>
            {/* Row label */}
            <div style={{
              width: cellSize + 10,
              textAlign: 'right',
              paddingRight: 10,
              fontSize: '0.85rem',
              fontWeight: hoveredCell?.row === rowIdx ? 600 : 400,
              color: hoveredCell?.row === rowIdx ? '#722f37' : '#2d2418',
              transition: 'all 0.2s ease'
            }}>
              {translators[rowIdx]}
            </div>

            {/* Cells */}
            {row.map((value, colIdx) => {
              const isHovered = hoveredCell?.row === rowIdx && hoveredCell?.col === colIdx
              const isHighlight = (rowIdx === 0 && colIdx === 1) || (rowIdx === 1 && colIdx === 0) // German-Hollingdale

              return (
                <div
                  key={colIdx}
                  style={{
                    width: cellSize,
                    height: cellSize,
                    backgroundColor: getColor(value),
                    border: isHovered ? '2px solid #722f37' : isHighlight ? '2px solid #f4a623' : '1px solid #e6d5b8',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontFamily: 'monospace',
                    fontSize: '0.8rem',
                    color: value >= 0.88 ? '#fdf6e3' : '#2d2418',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    transform: isHovered ? 'scale(1.05)' : 'scale(1)',
                    zIndex: isHovered ? 10 : 1,
                    position: 'relative'
                  }}
                  onMouseEnter={() => setHoveredCell({ row: rowIdx, col: colIdx, value })}
                  onMouseLeave={() => setHoveredCell(null)}
                >
                  {value.toFixed(2)}
                </div>
              )
            })}
          </div>
        ))}
      </div>

      {/* Tooltip */}
      {hoveredCell && (
        <div style={{
          marginTop: '1rem',
          padding: '0.75rem 1rem',
          background: '#2d2418',
          color: '#fdf6e3',
          borderRadius: '6px',
          fontSize: '0.9rem'
        }}>
          <strong>{translators[hoveredCell.row]}</strong> ↔ <strong>{translators[hoveredCell.col]}</strong>: {hoveredCell.value.toFixed(3)} similarity
        </div>
      )}

      {/* Legend */}
      <div style={{
        display: 'flex',
        gap: '1rem',
        marginTop: '1.5rem',
        fontSize: '0.8rem',
        color: '#5c4a37'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div style={{ width: 16, height: 16, background: '#fdf6e3', border: '1px solid #e6d5b8' }} />
          <span>Low (&lt;0.80)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div style={{ width: 16, height: 16, background: '#f4a623' }} />
          <span>High (0.84+)</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div style={{ width: 16, height: 16, background: '#722f37' }} />
          <span>Very High (0.95+)</span>
        </div>
      </div>
    </div>
  )
}
