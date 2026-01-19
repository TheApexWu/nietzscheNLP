'use client'

import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts'

const data = [
  { section: '§38', variance: 0.323, topic: 'French phrases, cultural critique' },
  { section: '§50', variance: 0.282, topic: 'Virtues of the common man' },
  { section: '§74', variance: 0.251, topic: 'Genius requires gratitude' },
  { section: '§130', variance: 0.250, topic: 'Talent reveals character' },
  { section: '§33', variance: 0.221, topic: 'Origin of freedom' },
  { section: '§15', variance: 0.208, topic: 'Sensualist philosophers' },
  { section: '§117', variance: 0.156, topic: 'Will to overcome emotion' },
  { section: '§119', variance: 0.152, topic: 'Disgust with dirt' },
  { section: '§97', variance: 0.135, topic: 'Great man as actor' },
  { section: '§76', variance: 0.134, topic: 'Self-contempt' },
]

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const item = payload[0].payload
    return (
      <div style={{
        background: '#2d2418',
        border: '1px solid #c9784a',
        borderRadius: '6px',
        padding: '12px 16px',
        color: '#fdf6e3',
        maxWidth: 280
      }}>
        <p style={{ margin: 0, fontWeight: 600, fontSize: '1.1rem' }}>{item.section}</p>
        <p style={{ margin: '8px 0', fontFamily: 'monospace', color: '#f4a623' }}>
          σ = {item.variance.toFixed(3)}
        </p>
        <p style={{ margin: 0, fontSize: '0.9rem', color: '#d4c4a8' }}>
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
                fill={hoveredIndex === index ? '#c9784a' : '#d4a574'}
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
