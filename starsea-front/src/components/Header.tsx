import { Search } from 'lucide-react';

export function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-md border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center">
              <span className="text-white font-bold text-lg">S</span>
            </div>
            <span className="text-xl font-bold text-white">Starsea</span>
          </div>

          <nav className="hidden md:flex items-center gap-8">
            <button className="flex items-center gap-2 text-white/80 hover:text-white transition">
              <Search className="w-5 h-5" />
            </button>
            <a href="#eventos" className="text-white/80 hover:text-white transition">
              Eventos
            </a>
            <a href="#generos" className="text-white/80 hover:text-white transition">
              Gêneros
            </a>
            <span className="text-white/40">|</span>
            <a href="#login" className="text-white/80 hover:text-white transition">
              Fazer login
            </a>
            <button className="px-6 py-2 rounded-full bg-gradient-to-r from-purple-500 to-cyan-500 text-white font-medium hover:opacity-90 transition">
              Cadastre-se
            </button>
          </nav>

          <button className="md:hidden text-white">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
}
