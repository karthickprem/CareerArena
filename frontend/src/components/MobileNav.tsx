"use client";

import { useState } from "react";

export default function MobileNav() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setOpen(!open)}
        className="ca-btn ca-btn-ghost p-1.5"
        aria-label="Toggle menu"
        aria-expanded={open}
      >
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
          {open ? (
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
          )}
        </svg>
      </button>

      {open && (
        <div className="absolute top-14 left-0 right-0 border-b border-ca-border bg-ca-bg/95 backdrop-blur-xl z-40">
          <div className="px-4 py-3 space-y-1">
            <a
              href="/screening"
              onClick={() => setOpen(false)}
              className="block px-3 py-2.5 text-sm font-medium text-ca-fg rounded-lg hover:bg-ca-accent/5 transition-colors"
            >
              Start Interview
            </a>
            <a
              href="/interview"
              onClick={() => setOpen(false)}
              className="block px-3 py-2.5 text-sm text-ca-fg-secondary rounded-lg hover:bg-ca-accent/5 transition-colors"
            >
              Quick Interview
            </a>
            <a
              href="/history"
              onClick={() => setOpen(false)}
              className="block px-3 py-2.5 text-sm text-ca-fg-secondary rounded-lg hover:bg-ca-accent/5 transition-colors"
            >
              History
            </a>
          </div>
        </div>
      )}
    </>
  );
}
