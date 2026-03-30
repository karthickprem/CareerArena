import type { Metadata } from "next";
import "./globals.css";
import MobileNav from "@/components/MobileNav";
import ThemeToggle from "@/components/ThemeToggle";
import RouteProgressBar from "@/components/RouteProgressBar";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "CareerArena — AI Panel Interview Platform",
  description:
    "Practice with AI interview panels that cross-question, challenge, and score you. Panel interviews, group discussions, and UPSC board simulations.",
  openGraph: {
    title: "CareerArena — AI Panel Interview Platform",
    description: "The only interview platform with multi-agent panel dynamics.",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="font-sans antialiased min-h-screen bg-ca-bg text-ca-fg">
        <RouteProgressBar />
        <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[100] ca-btn ca-btn-primary text-sm">
          Skip to content
        </a>
        <nav className="sticky top-0 z-50 border-b border-ca-border/80 bg-ca-bg/80 backdrop-blur-xl">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
            {/* Logo */}
            <a href="/" className="flex items-center gap-2.5 group">
              <span className="w-7 h-7 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center text-white text-sm font-bold shadow-sm shadow-indigo-500/20 group-hover:shadow-indigo-500/40 transition-shadow">
                C
              </span>
              <span className="font-bold text-lg tracking-tight">
                Career<span className="text-ca-accent">Arena</span>
              </span>
            </a>

            {/* Desktop nav */}
            <div className="hidden sm:flex items-center gap-5">
              <a href="/interview" className="text-sm text-ca-fg-secondary hover:text-ca-fg transition-colors">
                Interview
              </a>
              <a href="/history" className="text-sm text-ca-fg-secondary hover:text-ca-fg transition-colors">
                History
              </a>
              <ThemeToggle />
              <a
                href="/screening"
                className="ca-btn ca-btn-primary text-sm py-1.5 px-4 shadow-sm shadow-indigo-500/15"
              >
                Start Interview
              </a>
            </div>

            {/* Mobile nav */}
            <div className="sm:hidden flex items-center gap-2">
              <ThemeToggle />
              <a
                href="/screening"
                className="ca-btn ca-btn-primary text-sm py-1.5 px-3 shadow-sm shadow-indigo-500/15"
              >
                Start
              </a>
              <MobileNav />
            </div>
          </div>
        </nav>
        <main id="main-content">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
