// src/components/Brief.tsx

interface BriefProps {
  text: string;
}

export function Brief({ text }: BriefProps) {
  return (
    <div className="brief">
      <span className="brief-label">// AI BRIEF</span>
      <p className="brief-text">{text}</p>
    </div>
  );
}