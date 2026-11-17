import { useState, FormEvent, ChangeEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

interface FormData {
  email: string;
  password: string;
}

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState<FormData>({
    email: "",
    password: ""
  });
  const [error, setError] = useState<string>("");

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    if (login(formData.email, formData.password)) {
      navigate("/profile");
    } else {
      setError("Email ou senha inválidos");
    }
  };

  const handleChange = (field: keyof FormData) => (e: ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [field]: e.target.value });
  };

  return (
    <div className="min-h-screen flex">
      <div className="w-1/2 bg-gradient-to-br from-purple-500 via-blue-400 to-cyan-400 p-12 flex flex-col justify-between">
        <Link to="/" className="flex items-center gap-3">
          <img
            src="/sea-logo.png"
            alt="Logo"
            className="h-20 w-auto max-w-[280px] object-contain"
          />
        </Link>

        <div>
          <h1 className="text-5xl font-bold text-black mb-4">
            Entre e deixe a<br />música te guiar
          </h1>
          <p className="text-lg text-black/80">
            Avisamos quando seus artistas favoritos tocarem perto de<br />você.
          </p>
        </div>

        <p className="text-sm text-black/60">© 2026 Starsea</p>
      </div>

      <div className="w-1/2 bg-[#1a1a1a] p-12 flex items-center justify-center">
        <div className="w-full max-w-md">
          <h2 className="text-4xl font-bold text-white mb-2">Bem-vindo de volta</h2>
          <p className="text-gray-400 mb-8">Entre para ver seus eventos e ingressos.</p>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="p-3 bg-red-500/20 border border-red-500 text-red-400 rounded-lg text-sm">
                {error}
              </div>
            )}

            <div>
              <label className="block text-gray-300 text-sm font-medium mb-2">
                E-MAIL
              </label>
              <input
                type="email"
                placeholder="voce@email.com"
                value={formData.email}
                onChange={handleChange('email')}
                className="w-full px-4 py-3 bg-[#2a2a2a] border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500"
                required
              />
            </div>

            <div>
              <label className="block text-gray-300 text-sm font-medium mb-2">
                SENHA
              </label>
              <input
                type="password"
                placeholder="Sua senha"
                value={formData.password}
                onChange={handleChange('password')}
                className="w-full px-4 py-3 bg-[#2a2a2a] border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500"
              />
              <div className="text-right mt-2">
                <a href="#" className="text-sm text-purple-400 hover:underline">
                  Esqueci minha senha
                </a>
              </div>
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-gradient-to-r from-purple-500 to-cyan-400 text-white font-bold rounded-lg hover:opacity-90 transition"
            >
              ENTRAR
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-400 text-sm mb-3">
              Não tem uma conta?
            </p>
            <Link
              to="/signup"
              className="inline-block w-full py-3 bg-[#2a2a2a] border-2 border-purple-500 text-purple-400 font-bold rounded-lg hover:bg-[#333] transition"
            >
              CADASTRE-SE
            </Link>
          </div>

          <div className="mt-6">
            <p className="text-center text-gray-400 text-sm mb-4">ou continue com</p>

            <div className="grid grid-cols-2 gap-4">
              <button className="px-4 py-3 bg-[#2a2a2a] border border-gray-700 rounded-lg text-white hover:bg-[#333] transition flex items-center justify-center gap-2">
                <span className="text-green-500 font-bold">Spotify</span>
              </button>
              <button className="px-4 py-3 bg-[#2a2a2a] border border-gray-700 rounded-lg text-white hover:bg-[#333] transition">
                Apple Music
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
