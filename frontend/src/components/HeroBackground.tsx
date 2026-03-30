"use client";

import { motion } from "framer-motion";

// Constellation nodes — positioned as percentages
const nodes = [
  { x: 12, y: 18 }, { x: 28, y: 8 }, { x: 45, y: 25 },
  { x: 62, y: 12 }, { x: 78, y: 22 }, { x: 88, y: 8 },
  { x: 8, y: 55 }, { x: 35, y: 48 }, { x: 55, y: 58 },
  { x: 72, y: 45 }, { x: 92, y: 52 }, { x: 20, y: 82 },
];

// Connections between nodes (indices)
const edges: [number, number][] = [
  [0, 1], [1, 2], [2, 3], [3, 4], [4, 5],
  [0, 6], [2, 7], [7, 8], [8, 9], [9, 10],
  [6, 7], [6, 11], [3, 9], [1, 7],
];

export default function HeroBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
      <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
        {/* Edges */}
        {edges.map(([a, b], i) => (
          <motion.line
            key={`e${i}`}
            x1={nodes[a].x}
            y1={nodes[a].y}
            x2={nodes[b].x}
            y2={nodes[b].y}
            stroke="var(--accent)"
            strokeWidth="0.15"
            strokeOpacity="0.12"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 1.5, delay: i * 0.08, ease: "easeOut" }}
          />
        ))}
        {/* Nodes */}
        {nodes.map((n, i) => (
          <motion.circle
            key={`n${i}`}
            cx={n.x}
            cy={n.y}
            r="0.4"
            fill="var(--accent)"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0.15, 0.35, 0.15] }}
            transition={{
              duration: 3,
              delay: i * 0.15,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />
        ))}
      </svg>

      {/* Floating shape */}
      <div className="floating-shape" />
    </div>
  );
}
