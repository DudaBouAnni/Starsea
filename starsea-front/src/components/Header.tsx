import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface HeaderProps {
  currentPage?: string;
}

export function Header({ currentPage }: HeaderProps) {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <header className="bg-[#1a1a1a] text-white py-4 px-8 flex items-center justify-between">
      <Link to="/" className="flex items-center gap-3">
        <img
          src="/sea-logo.png"
          alt="Logo"
          className="h-24 w-auto max-w-[340px] object-contain sm:h-28 sm:max-w-[400px] lg:h-32 lg:max-w-[450px]"
        />
      </Link>

      <nav className="flex items-center gap-8">
        <Link 
          to="/events" 
          className={currentPage === 'events' ? 'text-cyan-400' : 'text-gray-300 hover:text-white'}
        >
          Eventos
        </Link>
        <Link 
          to="/genres" 
          className={currentPage === 'genres' ? 'text-cyan-400' : 'text-gray-300 hover:text-white'}
        >
          Gêneros
        </Link>
        <Link 
          to="/locais" 
          className={currentPage === 'locais' ? 'text-cyan-400' : 'text-gray-300 hover:text-white'}
        >
          Locais
        </Link>
        <Link 
          to="/tickets" 
          className={currentPage === 'tickets' ? 'text-cyan-400' : 'text-gray-300 hover:text-white'}
        >
          Ingressos
        </Link>

        {isAuthenticated ? (
          <>
            <Link 
              to="/profile" 
              className={currentPage === 'profile' ? 'text-cyan-400' : 'text-gray-300 hover:text-white'}
            >
              {user?.name || 'Perfil'}
            </Link>
            <button
              onClick={logout}
              className="px-4 py-2 bg-red-500 hover:bg-red-600 rounded-lg font-medium text-white text-sm transition"
            >
              Sair
            </button>
          </>
        ) : (
          <Link 
            to="/login" 
            className="px-4 py-2 bg-gradient-to-r from-purple-500 to-cyan-400 rounded-lg font-bold hover:opacity-90"
          >
            Entrar
          </Link>
        )}
      </nav>
    </header>
  );
}
