import { Link } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";

export function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <header className="flex h-[70px] w-full items-center justify-between px-12 bg-[#1a1a1a]">
      <Link to="/" className="flex items-center gap-3">
        <img
          src="/sea-logo.png"
          alt="Logo"
          className="h-24 w-auto max-w-[340px] object-contain sm:h-28 sm:max-w-[400px] lg:h-32 lg:max-w-[450px]"
        />
      </Link>

      <nav className="flex items-center gap-8 text-sm font-medium text-gray-300">
        <Link to="/events" className="hover:text-white transition">
          Eventos
        </Link>
        <Link to="/genres" className="hover:text-white transition">
          Gêneros
        </Link>
        <Link to="/locais" className="hover:text-white transition">
          Locais
        </Link>
        <Link to="/tickets" className="hover:text-white transition">
          Ingressos
        </Link>

        {isAuthenticated ? (
          <>
            <Link to="/profile" className="hover:text-white transition">
              {user?.name || "Perfil"}
            </Link>
            <button
              onClick={logout}
              className="px-6 py-2 bg-red-500 hover:bg-red-600 rounded-lg font-bold text-white text-sm transition"
            >
              Sair
            </button>
          </>
        ) : (
          <Link
            to="/login"
            className="px-6 py-2 bg-gradient-to-r from-violet-500 to-cyan-400 rounded-lg font-bold text-white text-sm hover:opacity-90 transition"
          >
            Entrar
          </Link>
        )}
      </nav>
    </header>
  );
}
