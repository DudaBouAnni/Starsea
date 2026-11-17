import { Link } from "react-router-dom";
import { Header } from "../components/Header";

interface Artist {
  name: string;
  imageSrc: string;
  gradientFallback: string;
}

interface Show {
  name: string;
  date: string;
}

export default function ProfilePage() {
  const topArtists: Artist[] = [
    {
      name: "Doja Cat",
      imageSrc: "https://i.scdn.co/image/ab6761610000e5ebe94f88ff74ae4ddcab961f97",
      gradientFallback: "bg-gradient-to-br from-pink-500 to-purple-600"
    },
    {
      name: "My Chemical Romance",
      imageSrc: "https://i.scdn.co/image/ab6761610000e5eb0c55e74e435910793888f7cf",
      gradientFallback: "bg-gradient-to-br from-gray-800 to-gray-900"
    },
    {
      name: "Kali Uchis",
      imageSrc: "https://poptivo.com.br/wp-content/uploads/2024/06/Kali-uchis.jpeg",
      gradientFallback: "bg-gradient-to-br from-orange-400 to-pink-500"
    },
    {
      name: "Bad Bunny",
      imageSrc: "https://i.scdn.co/image/ab6761610000e5eb81f47f44084e0a09b5f0fa13",
      gradientFallback: "bg-gradient-to-br from-green-400 to-lime-500"
    },
    {
      name: "Rufus du Sol",
      imageSrc: "https://i.scdn.co/image/ab67616d0000b27360e5059dcab339142d7642bb",
      gradientFallback: "bg-gradient-to-br from-blue-500 to-purple-600"
    }
  ];

  const upcomingShows: Show[] = [
    { name: "Doja Cat - Sahal Music Hall", date: "05 fev" },
    { name: "My Chemical Romance - Allianz Parque", date: "06 e 08 fev" },
    { name: "Bad Bunny - Allianz Parque", date: "20 e 21 fev" }
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <Header currentPage="profile" />

      <div className="bg-[#1a1a1a] text-white py-12 px-8">
        <div className="max-w-6xl mx-auto flex items-center gap-8">
          <div className="w-32 h-32 bg-gradient-to-br from-purple-500 to-cyan-400 rounded-full flex items-center justify-center text-6xl font-bold">
            A
          </div>

          <div className="flex-1">
            <h1 className="text-4xl font-bold mb-2">Você</h1>
            <p className="text-gray-400">São Paulo, SP</p>
          </div>

          <div className="flex gap-12 text-center">
            <div>
              <p className="text-4xl font-bold mb-1">12</p>
              <p className="text-gray-400 text-sm">Shows</p>
            </div>
            <div>
              <p className="text-4xl font-bold mb-1">3</p>
              <p className="text-gray-400 text-sm">Ingressos</p>
            </div>
            <div>
              <p className="text-4xl font-bold mb-1">24</p>
              <p className="text-gray-400 text-sm">Favoritos</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-8 py-12 grid grid-cols-3 gap-8">
        <div className="col-span-2 space-y-8">
          <div className="bg-white rounded-xl p-6">
            <h2 className="text-2xl font-bold mb-6">Artistas que você mais ouve</h2>
            
            <div className="flex gap-4">
              {topArtists.map((artist, index) => (
                <div key={index} className="flex-1">
                  <div className="aspect-square rounded-lg mb-2 overflow-hidden relative">
                    <img
                      src={artist.imageSrc}
                      alt={artist.name}
                      className="absolute inset-0 w-full h-full object-cover"
                      onError={(e) => {
                        const target = e.target as HTMLImageElement;
                        target.style.display = "none";
                        if (target.nextSibling) {
                          (target.nextSibling as HTMLElement).style.display = "block";
                        }
                      }}
                    />

                    <div className={`absolute inset-0 ${artist.gradientFallback} hidden`}></div>
                  </div>
                  <p className="text-sm font-medium text-center">{artist.name}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl p-6">
            <h2 className="text-2xl font-bold mb-6">Shows dos seus artistas</h2>
            
            <div className="space-y-4">
              {upcomingShows.map((show, index) => (
                <div key={index} className="flex justify-between items-center py-3 border-b border-gray-200 last:border-0">
                  <p className="font-medium">{show.name}</p>
                  <p className="text-gray-500">{show.date}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 h-fit">
          <h2 className="text-2xl font-bold mb-6">Configurações</h2>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center py-3 border-b border-gray-200">
              <span className="font-medium">Spotify</span>
              <button className="text-purple-500 hover:text-purple-600 text-sm">Conectado</button>
            </div>

            <div className="flex justify-between items-center py-3 border-b border-gray-200">
              <span className="font-medium">Apple Music</span>
              <button className="text-purple-500 hover:text-purple-600 text-sm">Conectar</button>
            </div>

            <div className="flex justify-between items-center py-3 border-b border-gray-200">
              <span className="font-medium">Cidade</span>
              <span className="text-gray-500 text-sm">São Paulo, SP</span>
            </div>

            <div className="flex justify-between items-center py-3 border-b border-gray-200">
              <span className="font-medium">Notificações de shows</span>
              <button className="text-purple-500 hover:text-purple-600 text-sm">Ativadas</button>
            </div>

            <div className="pt-4">
              <button className="text-purple-500 hover:text-purple-600 text-sm">
                Ajuda e suporte
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
