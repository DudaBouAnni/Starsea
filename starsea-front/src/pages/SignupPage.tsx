import { useState, FormEvent, ChangeEvent } from "react";
import { Link, useNavigate } from "react-router-dom";

interface FormData {
  name: string;
  email: string;
  password: string;
  birthdate: string;
}

export default function SignupPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    password: "",
    birthdate: ""
  });

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Cadastro:", formData);
    navigate("/onboarding/connect-music");
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
            Crie sua conta em 3<br />passos
          </h1>
          <p className="text-lg text-black/80">
            Avisamos quando seus artistas favoritos tocarem perto de<br />você.
          </p>
        </div>

        <p className="text-sm text-black/60">© 2026 Starsea</p>
      </div>

      <div className="w-1/2 bg-[#1a1a1a] p-12 flex items-center justify-center">
        <div className="w-full max-w-md">
          <div className="mb-8">
            <div className="flex gap-2 mb-2">
              <div className="h-1 flex-1 bg-gradient-to-r from-purple-500 to-cyan-400 rounded"></div>
              <div className="h-1 flex-1 bg-gray-700 rounded"></div>
              <div className="h-1 flex-1 bg-gray-700 rounded"></div>
            </div>
            <p className="text-gray-400 text-sm">Passo 1 de 3</p>
          </div>

          <h2 className="text-4xl font-bold text-white mb-2">Crie sua conta</h2>
          <p className="text-gray-400 mb-8">Leva menos de um minuto.</p>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-gray-300 text-sm font-medium mb-2">
                NOME
              </label>
              <input
                type="text"
                placeholder="Seu nome"
                value={formData.name}
                onChange={handleChange('name')}
                className="w-full px-4 py-3 bg-[#2a2a2a] border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500"
              />
            </div>

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
              />
            </div>

            <div>
              <label className="block text-gray-300 text-sm font-medium mb-2">
                SENHA
              </label>
              <input
                type="password"
                placeholder="Mínimo 8 caracteres"
                value={formData.password}
                onChange={handleChange('password')}
                className="w-full px-4 py-3 bg-[#2a2a2a] border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500"
              />
            </div>

            <div>
              <label className="block text-gray-300 text-sm font-medium mb-2">
                DATA DE NASCIMENTO
              </label>
              <input
                type="text"
                placeholder="DD/MM/AAAA"
                value={formData.birthdate}
                onChange={handleChange('birthdate')}
                className="w-full px-4 py-3 bg-[#2a2a2a] border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500"
              />
            </div>

            <p className="text-xs text-gray-400">
              Ao continuar, você aceita os <a href="#" className="text-purple-400 hover:underline">Termos de uso</a> e a <a href="#" className="text-purple-400 hover:underline">Política de privacidade</a>.
            </p>

            <button
              type="submit"
              className="w-full py-3 bg-gradient-to-r from-purple-500 to-cyan-400 text-white font-bold rounded-lg hover:opacity-90 transition"
            >
              CONTINUAR
            </button>
          </form>

          <p className="text-center text-gray-400 text-sm mt-8">
            Já tem conta? <Link to="/login" className="text-purple-400 hover:underline">Entrar</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
