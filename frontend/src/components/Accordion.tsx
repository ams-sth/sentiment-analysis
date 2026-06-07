import { useState } from "react";
import type { ReactNode } from "react";

interface Props {
  title: string;
  children: ReactNode;
  defaultOpen?: boolean;
}

export default function Accordion({ title, children, defaultOpen = false }: Props) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div className="bg-white/10 rounded-2xl border border-white/20 overflow-hidden">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between px-6 py-4 text-white font-semibold hover:bg-white/5 transition-colors text-left"
      >
        <span>{title}</span>
        <span
          className={`text-zinc-500 text-lg leading-none transition-transform duration-200 ${open ? "rotate-180" : ""}`}
        >
          ▾
        </span>
      </button>
      {/* CSS grid trick for smooth height animation */}
      <div
        className="accordion-grid overflow-hidden"
        style={{ gridTemplateRows: open ? "1fr" : "0fr" }}
      >
        <div className="overflow-hidden">
          <div className="px-6 pt-4 pb-6 border-t border-white/10">{children}</div>
        </div>
      </div>
    </div>
  );
}
