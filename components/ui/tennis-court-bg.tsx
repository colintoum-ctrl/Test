export default function TennisCourtBg({ className = '', color }: { className?: string; color?: string }) {
  return (
    <svg
      className={`absolute inset-0 w-full h-full pointer-events-none ${className}`}
      style={color ? { color } : undefined}
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <defs>
        <pattern id="tennis-court" x="0" y="0" width="120" height="80" patternUnits="userSpaceOnUse">
          {/* Outer rectangle */}
          <rect x="4" y="4" width="112" height="72" fill="none" stroke="currentColor" strokeWidth="0.5" />
          {/* Center line vertical */}
          <line x1="60" y1="4" x2="60" y2="76" stroke="currentColor" strokeWidth="0.5" />
          {/* Service boxes horizontal */}
          <line x1="4" y1="28" x2="116" y2="28" stroke="currentColor" strokeWidth="0.5" />
          <line x1="4" y1="52" x2="116" y2="52" stroke="currentColor" strokeWidth="0.5" />
          {/* Net line */}
          <line x1="4" y1="40" x2="116" y2="40" stroke="currentColor" strokeWidth="0.8" strokeDasharray="3,2" />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#tennis-court)" />
    </svg>
  )
}
