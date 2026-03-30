import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[55vh] text-center px-4">
      <span className="text-6xl mb-6 inline-block animate-swim">🐙</span>
      <p className="text-xs font-semibold uppercase tracking-[0.25em] text-violet-300/40 mb-4">Error 404</p>
      <h1 className="text-5xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-violet-400 to-cyan-400 mb-4">
        Lost in the deep
      </h1>
      <p className="text-violet-300/50 max-w-md mb-10 leading-relaxed">
        This page doesn&apos;t exist — even our octopus couldn&apos;t find it. Head back to the surface.
      </p>
      <Link
        href="/"
        className="ca-btn-primary ca-shine inline-flex items-center justify-center px-8 py-3 rounded-[var(--radius-md)] text-sm font-semibold"
      >
        Back to surface
      </Link>
    </div>
  );
}
