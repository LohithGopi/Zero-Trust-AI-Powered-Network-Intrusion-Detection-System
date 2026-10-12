import React, { useRef, useState } from 'react';
import { cyberAudio } from '../utils/cyberAudio';

export const SpatialTiltCard = ({ 
  children, 
  className = '', 
  tiltDegree = 8, 
  glare = true,
  onClick = undefined,
  ...props 
}) => {
  const cardRef = useRef(null);
  const [rotX, setRotX] = useState(0);
  const [rotY, setRotY] = useState(0);
  const [glarePos, setGlarePos] = useState({ x: 50, y: 50, opacity: 0 });

  const handleMouseMove = (e) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    
    const rY = ((x - centerX) / centerX) * tiltDegree;
    const rX = -((y - centerY) / centerY) * tiltDegree;
    
    setRotX(rX);
    setRotY(rY);
    
    if (glare) {
      setGlarePos({
        x: (x / rect.width) * 100,
        y: (y / rect.height) * 100,
        opacity: 0.15
      });
    }
  };

  const handleMouseEnter = () => {
    cyberAudio.playHover();
  };

  const handleMouseLeave = () => {
    setRotX(0);
    setRotY(0);
    setGlarePos(prev => ({ ...prev, opacity: 0 }));
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={(e) => {
        cyberAudio.playClick();
        if (onClick) onClick(e);
      }}
      style={{
        transform: `perspective(1000px) rotateX(${rotX}deg) rotateY(${rotY}deg)`,
        transition: 'transform 0.15s ease-out, box-shadow 0.2s ease-out'
      }}
      className={`relative overflow-hidden ${className}`}
      {...props}
    >
      {glare && (
        <div
          className="pointer-events-none absolute inset-0 z-20 transition-opacity duration-300"
          style={{
            background: `radial-gradient(circle at ${glarePos.x}% ${glarePos.y}%, rgba(255,255,255,0.25) 0%, rgba(59,130,246,0.15) 30%, transparent 70%)`,
            opacity: glarePos.opacity
          }}
        />
      )}
      {children}
    </div>
  );
};
