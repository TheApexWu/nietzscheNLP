'use client'

import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts'

const data = [
  { section: '§35', variance: 0.305, topic: 'Voltaire, truth-seeking, embedded French' },
  { section: '§28', variance: 0.288, topic: 'Meta-aphorism about translation itself', highlight: true },
  { section: '§59', variance: 0.281, topic: 'Human superficiality as survival instinct' },
  { section: '§102', variance: 0.233, topic: 'Discovering reciprocated love (short)' },
  { section: '§83', variance: 0.226, topic: 'Instinct — house fire aphorism' },
  { section: '§4', variance: 0.218, topic: 'Danger of philosophy' },
  { section: '§12', variance: 0.212, topic: 'Soul atomism critique' },
  { section: '§52', variance: 0.205, topic: 'Philosophers and their prejudices' },
  { section: '§203', variance: 0.198, topic: 'The herd instinct' },
  { section: '§269', variance: 0.191, topic: 'What is noble' },
]

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const item = payload[0].payload
    return (
      <div style={{
        background: '#2d2418',
        border: item.highlight ? '2px solid #f4a623' : '1px solid #c9784a',
        borderRadius: '6px',
        padding: '12px 16px',
        color: '#fdf6e3',
        maxWidth: 280
      }}>
        <p style={{ margin: 0, fontWeight: 600, fontSize: '1.1rem' }}>{item.section}</p>
        <p style={{ margin: '8px 0', fontFamily: 'monospace', color: '#f4a623' }}>
          σ = {item.variance.toFixed(3)}
        </p>
        <p style={{ margin: 0, fontSize: '0.9rem', color: '#d4c4a8', fontStyle: item.highlight ? 'italic' : 'normal' }}>
          {item.topic}
        </p>
      </div>
    )
  }
  return null
}

export default function DivergenceChart() {
  const [hoveredIndex, setHoveredIndex] = useState(null)

  return (
    <div style={{ width: '100%', height: 400 }}>
      <ResponsiveContainer>
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 50, bottom: 20 }}
        >
          <XAxis
            dataKey="section"
            tick={{ fill: '#2d2418', fontSize: 12, fontFamily: 'monospace' }}
            tickLine={{ stroke: '#e6d5b8' }}
            axisLine={{ stroke: '#e6d5b8' }}
          />
          <YAxis
            domain={[0, 0.35]}
            tick={{ fill: '#5c4a37', fontSize: 12 }}
            tickLine={{ stroke: '#e6d5b8' }}
            axisLine={{ stroke: '#e6d5b8' }}
            label={{
              value: 'Translator Divergence (σ)',
              angle: -90,
              position: 'insideLeft',
              style: { fill: '#5c4a37', fontSize: 12 }
            }}
          />
          <ReferenceLine
            y={0.25}
            stroke="#722f37"
            strokeDasharray="5 5"
            label={{ value: 'High divergence threshold', fill: '#722f37', fontSize: 10 }}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(244, 166, 35, 0.1)' }} />
          <Bar
            dataKey="variance"
            radius={[4, 4, 0, 0]}
            animationDuration={1800}
            animationEasing="ease-out"
          >
            {data.map((entry, index) => (
              <Cell
                key={entry.section}
                fill={entry.highlight ? '#f4a623' : hoveredIndex === index ? '#c9784a' : '#d4a574'}
                stroke={entry.highlight ? '#722f37' : 'none'}
                strokeWidth={entry.highlight ? 2 : 0}
                style={{ cursor: 'pointer', transition: 'fill 0.3s ease' }}
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
