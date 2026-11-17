import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

export default function OnboardingMusicPage() {
  const navigate = useNavigate();
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);

  const genres: string[] = [
    "Pop", "Rock", "K-pop", "MPB", "Jazz",
    "Sertanejo", "Funk", "Eletrônica", "Rap", "Metal"
  ];

  const toggleGenre = (genre: string): void => {
    if (selectedGenres.includes(genre)) {
      setSelectedGenres(selectedGenres.filter(g => g !== genre));
    } else {
      setSelectedGenres([...selectedGenres, genre]);
    }
  };

  const handleContinue = (): void => {
    console.log("Gêneros selecionados:", selectedGenres);
    navigate("/");
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
            Quase lá. Conte o<br />que você ouve
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
              <div className="h-1 flex-1 bg-gradient-to-r from-purple-500 to-cyan-400 rounded"></div>
              <div className="h-1 flex-1 bg-gray-700 rounded"></div>
            </div>
            <p className="text-gray-400 text-sm">Passo 2 de 3</p>
          </div>

          <h2 className="text-4xl font-bold text-white mb-2">Conecte sua música</h2>
          <p className="text-gray-400 mb-8">Recomendamos shows com base no que você ouve.</p>

          <div className="space-y-4 mb-8">
            <button className="w-full px-6 py-4 bg-[#2a2a2a] border border-gray-700 rounded-lg text-white hover:bg-[#333] transition flex items-center justify-between">
              <span className="text-green-500 font-bold">Spotify</span>
              <span className="text-gray-400">Conectar</span>
            </button>

            <button className="w-full px-6 py-4 bg-[#2a2a2a] border border-gray-700 rounded-lg text-white hover:bg-[#333] transition flex items-center justify-between">
              <span>Apple Music</span>
              <span className="text-gray-400">Conectar</span>
            </button>
          </div>

          <p className="text-center text-gray-400 text-sm mb-6">ou escolha seus gêneros</p>

          <div className="flex flex-wrap gap-3 mb-8">
            {genres.map((genre) => (
              <button
                key={genre}
                onClick={() => toggleGenre(genre)}
                className={`px-6 py-2 rounded-full font-medium transition ${
                  selectedGenres.includes(genre)
                    ? "bg-gradient-to-r from-purple-500 to-cyan-400 text-white"
                    : "bg-[#2a2a2a] text-gray-300 hover:bg-[#333]"
                }`}
              >
                {genre}
              </button>
            ))}
          </div>

          <button 
            onClick={handleContinue}
            className="w-full py-3 bg-gradient-to-r from-purple-500 to-cyan-400 text-white font-bold rounded-lg hover:opacity-90 transition"
          >
            CONTINUAR
          </button>

          <p className="text-center text-gray-400 text-sm mt-4">
            <button onClick={() => navigate("/")} className="hover:underline">Pular por agora</button>
          </p>
        </div>
      </div>
    </div>
  );
}
