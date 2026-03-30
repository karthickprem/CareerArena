"use client";

import { useEffect, useState, useCallback } from "react";
import { usePathname } from "next/navigation";

export default function RouteProgressBar() {
  const pathname = usePathname();
  const [progress, setProgress] = useState(0);
  const [visible, setVisible] = useState(false);

  const startProgress = useCallback(() => {
    setVisible(true);
    setProgress(0);
    // Quickly ramp to ~85%
    let p = 0;
    const tick = () => {
      p += (85 - p) * 0.1;
      setProgress(p);
      if (p < 84) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, []);

  const completeProgress = useCallback(() => {
    setProgress(100);
    setTimeout(() => {
      setVisible(false);
      setProgress(0);
    }, 300);
  }, []);

  // Intercept link clicks
  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      const anchor = (e.target as HTMLElement).closest("a");
      if (!anchor) return;
      const href = anchor.getAttribute("href");
      if (href && href.startsWith("/") && href !== pathname) {
        startProgress();
      }
    };
    document.addEventListener("click", handleClick, true);
    return () => document.removeEventListener("click", handleClick, true);
  }, [pathname, startProgress]);

  // Complete on pathname change
  useEffect(() => {
    completeProgress();
  }, [pathname, completeProgress]);

  if (!visible) return null;

  return (
    <div className="fixed top-0 left-0 right-0 z-[100] h-0.5">
      <div
        className="h-full rounded-r-full transition-all duration-200 ease-out"
        style={{
          width: `${progress}%`,
          background: "linear-gradient(90deg, #6366f1, #8b5cf6, #10b981)",
        }}
      />
    </div>
  );
}
