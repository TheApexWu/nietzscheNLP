'use client'

import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

// Updated with corrected corpus data
const data = [
  { translator: 'Hollingdale', similarity: 0.806, fullName: 'R.J. Hollingdale (1973)' },
  { translator: 'Faber', similarity: 0.791, fullName: 'Marion Faber (1998)' },
  { translator: 'Kaufmann', similarity: 0.787, fullName: 'Walter Kaufmann (1966)' },
  { translator: 'Norman', similarity: 0.780, fullName: 'Judith Norman (2002)' },
  { translator: 'Zimmern', similarity: 0.779, fullName: 'Helen Zimmern (1906)' },
]

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const item = payload[0].payload
    return (
      <div style={{
        background: '#2d2418',
        border: '1px solid #f4a623',
        borderRadius: '6px',
        padding: '12px 16px',
        color: '#fdf6e3'
      }}>
        <p style={{ margin: 0, fontWeight: 600 }}>{item.fullName}</p>
        <p style={{ margin: '4px 0 0', fontFamily: 'monospace', color: '#f4a623' }}>
          Similarity: {item.similarity.toFixed(3)}
        </p>
      </div>
    )
  }
  return null
}

export default function SimilarityChart() {
  const [hoveredIndex, setHoveredIndex] = useState(null)

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 30, left: 100, bottom: 10 }}
        >
          <XAxis
            type="number"
            domain={[0.76, 0.82]}
            tick={{ fill: '#5c4a37', fontSize: 12 }}
            tickLine={{ stroke: '#e6d5b8' }}
            axisLine={{ stroke: '#e6d5b8' }}
          />
          <YAxis
            type="category"
            dataKey="translator"
            tick={{ fill: '#2d2418', fontSize: 14, fontWeight: 500 }}
            tickLine={false}
            axisLine={false}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(244, 166, 35, 0.1)' }} />
          <Bar
            dataKey="similarity"
            radius={[0, 4, 4, 0]}
            animationDuration={1500}
            animationEasing="ease-out"
          >
            {data.map((entry, index) => (
              <Cell
                key={entry.translator}
                fill={index === 0 ? '#f4a623' : hoveredIndex === index ? '#c9784a' : '#d4a574'}
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
