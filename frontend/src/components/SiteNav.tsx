"use client";

import type { ComponentType } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { IconHistory } from "@/components/icons";

type NavLink = {
  href: string;
  label: string;
  icon?: ComponentType<{ className?: string }>;
};

const links: NavLink[] = [
  { href: "/", label: "New query" },
  { href: "/history", label: "History", icon: IconHistory },
];

export default function SiteNav() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 border-b border-violet-500/10 bg-[var(--nav-blur)] backdrop-blur-xl backdrop-saturate-150">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-6">
        <Link
          href="/"
          className="flex items-center gap-3 group shrink-0 rounded-lg"
        >
          <span className="text-2xl transition-transform duration-300 group-hover:scale-110">🐙</span>
          <div className="flex flex-col leading-tight">
            <span className="font-bold text-base tracking-tight text-[var(--foreground)]">
              Octopus<span className="text-transparent bg-clip-text bg-gradient-to-r from-violet-400 to-cyan-400">AI</span>
            </span>
            <span className="text-[10px] text-violet-300/60 font-medium tracking-widest uppercase">
              Career Intelligence
            </span>
          </div>
        </Link>

        <nav className="flex items-center gap-1 sm:gap-2" aria-label="Main">
          {links.map(({ href, label, icon: Icon }) => {
            const active = pathname === href || (href !== "/" && pathname.startsWith(href));
            return (
              <Link
                key={href}
                href={href}
                className={`
                  relative flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors duration-200
                  ${
                    active
                      ? "text-cyan-300 bg-cyan-500/10"
                      : "text-[var(--muted)] hover:text-cyan-300/80 hover:bg-violet-500/5"
                  }
                `}
              >
                {Icon && <Icon className="h-4 w-4 opacity-80" />}
                <span>{label}</span>
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
