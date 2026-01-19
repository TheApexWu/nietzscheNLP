'use client'

import { useState, useEffect } from 'react'
import { ScatterChart, Scatter, XAxis, YAxis, ResponsiveContainer, Cell } from 'recharts'

// Generate synthetic UMAP-like clusters based on actual findings
// Each translator forms a distinct cluster, German at center
function generateClusterData() {
  const clusters = {
    German: { cx: 0, cy: 0, color: '#f4a623', count: 226 },
    Hollingdale: { cx: 0.8, cy: 0.3, color: '#722f37', count: 226 },
    Kaufmann: { cx: 1.0, cy: 0.5, color: '#c9784a', count: 226 },
    Faber: { cx: 0.6, cy: 0.8, color: '#8b7355', count: 226 },
    Norman: { cx: -0.5, cy: 0.9, color: '#5c8a4a', count: 226 },
    Zimmern: { cx: -0.8, cy: -0.4, color: '#4a6a8b', count: 226 },
  }

  const points = []

  Object.entries(clusters).forEach(([translator, config]) => {
    for (let i = 0; i < 40; i++) { // Reduced for performance
      // Add gaussian noise around cluster center
      const noise = () => (Math.random() - 0.5) * 0.6
      points.push({
        x: config.cx + noise(),
        y: config.cy + noise(),
        translator,
        color: config.color,
        aphorism: Math.floor(Math.random() * 226) + 1
      })
    }
  })

  return points
}

const COLORS = {
  German: '#f4a623',
  Hollingdale: '#722f37',
  Kaufmann: '#c9784a',
  Faber: '#8b7355',
  Norman: '#5c8a4a',
  Zimmern: '#4a6a8b',
}

// Tooltip removed - aphorism numbers without actual quotes aren't useful

export default function UMAPChart() {
  const [data, setData] = useState([])
  const [hoveredTranslator, setHoveredTranslator] = useState(null)
  const [animationComplete, setAnimationComplete] = useState(false)

  useEffect(() => {
    // Generate data on client side only
    setData(generateClusterData())
    const timer = setTimeout(() => setAnimationComplete(true), 2000)
    return () => clearTimeout(timer)
  }, [])

  // Group data by translator for separate Scatter components
  const groupedData = Object.keys(COLORS).reduce((acc, translator) => {
    acc[translator] = data.filter(d => d.translator === translator)
    return acc
  }, {})

  return (
    <div style={{ width: '100%', height: 500, position: 'relative' }}>
      <ResponsiveContainer>
        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
          <XAxis
            type="number"
            dataKey="x"
            domain={[-1.5, 1.8]}
            tick={false}
            axisLine={{ stroke: '#e6d5b8' }}
          />
          <YAxis
            type="number"
            dataKey="y"
            domain={[-1.2, 1.5]}
            tick={false}
            axisLine={{ stroke: '#e6d5b8' }}
          />
          {Object.entries(groupedData).map(([translator, points]) => (
            <Scatter
              key={translator}
              name={translator}
              data={points}
              fill={COLORS[translator]}
              animationDuration={1500}
              animationEasing="ease-out"
            >
              {points.map((entry, index) => (
                <Cell
                  key={index}
                  fill={COLORS[translator]}
                  fillOpacity={
                    hoveredTranslator === null ? 0.7 :
                    hoveredTranslator === translator ? 0.9 : 0.15
                  }
                  style={{ transition: 'fill-opacity 0.3s ease' }}
                />
              ))}
            </Scatter>
          ))}
        </ScatterChart>
      </ResponsiveContainer>

      {/* Custom legend */}
      <div style={{
        position: 'absolute',
        bottom: 10,
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        gap: '1rem',
        flexWrap: 'wrap',
        justifyContent: 'center',
        background: 'rgba(253, 246, 227, 0.9)',
        padding: '8px 16px',
        borderRadius: '6px',
        border: '1px solid #e6d5b8'
      }}>
        {Object.entries(COLORS).map(([translator, color]) => (
          <div
            key={translator}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              cursor: 'pointer',
              opacity: hoveredTranslator === null || hoveredTranslator === translator ? 1 : 0.4,
              transition: 'opacity 0.3s ease'
            }}
            onMouseEnter={() => setHoveredTranslator(translator)}
            onMouseLeave={() => setHoveredTranslator(null)}
          >
            <div style={{
              width: 12,
              height: 12,
              borderRadius: '50%',
              background: color,
              border: translator === 'German' ? '2px solid #722f37' : 'none'
            }} />
            <span style={{
              fontSize: '0.8rem',
              fontWeight: translator === 'German' ? 600 : 400,
              color: '#2d2418'
            }}>
              {translator}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
