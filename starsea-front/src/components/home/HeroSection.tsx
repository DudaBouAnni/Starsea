
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { MapPin, Search, Calendar } from 'lucide-react';

interface CardStackImage {
  src: string;
  alt: string;
  color: string;
  rotation: string;
  zIndex: number;
}

export function HeroSection() {
  const [city, setCity] = useState<string>("São Paulo");
  const [date, setDate] = useState<string>("");
  const [artist, setArtist] = useState<string>("");

  const cardImages: CardStackImage[] = [
    {
      src: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0GyFOPJVxD2tGJng329Valos2FCParRUnvMMK29qVZm9e05EK5Aakg55O&s=10',
      alt: 'Evento 1',
      color: 'from-blue-600 to-blue-800',
      rotation: 'rotate-[-8deg]',
      zIndex: 10
    },
    {
      src: 'https://i.scdn.co/image/ab67616d00001e028db37bc9a58543471bee78c5',
      alt: 'Evento 2',
      color: 'from-pink-500 to-purple-600',
      rotation: 'rotate-[-4deg]',
      zIndex: 20
    },
    {
      src: 'https://i.scdn.co/image/ab6761610000e5ebaadc18cac8d48124357c38e6',
      alt: 'Evento 3',
      color: 'from-green-400 to-teal-500',
      rotation: 'rotate-[0deg]',
      zIndex: 30
    }
  ];

  return (
    <section className="relative bg-[#1a1a1a] px-12 py-16">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

        {/* Texto e busca */}
        <div>
          <h1 className="text-6xl font-extrabold text-white leading-tight mb-3">
            Navegue no mar de eventos
          </h1>

          <p className="text-sm text-gray-400 tracking-widest mb-8 uppercase">
            A música te guia
          </p>

          <div className="space-y-4 mb-6">
            <div className="flex gap-3">
              <div className="flex-1 flex items-center gap-3 px-4 py-3 bg-[#2a2a2a] rounded-lg">
                <MapPin className="w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="São Paulo"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  className="flex-1 bg-transparent text-white placeholder-gray-500 focus:outline-none"
                />
              </div>

              <div className="flex-1 flex items-center gap-3 px-4 py-3 bg-[#2a2a2a] rounded-lg">
                <Search className="w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Artista ou música"
                  value={artist}
                  onChange={(e) => setArtist(e.target.value)}
                  className="flex-1 bg-transparent text-white placeholder-gray-500 focus:outline-none"
                />
              </div>
            </div>

            <div className="flex gap-3">
              <div className="flex-1 flex items-center gap-3 px-4 py-3 bg-[#2a2a2a] rounded-lg">
                <Calendar className="w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Data"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="flex-1 bg-transparent text-white placeholder-gray-500 focus:outline-none"
                />
              </div>

              <Link
                to="/events"
                className="px-10 py-3 bg-gradient-to-r from-violet-500 to-cyan-400 rounded-lg font-bold text-white text-sm hover:opacity-90 transition"
              >
                BUSCAR
              </Link>
            </div>
          </div>

          <div className="flex items-center gap-4 text-xs text-gray-400">
            <span>Conecte para ver shows dos seus artistas:</span>

            <button className="px-4 py-2 bg-[#1DB954] text-white rounded-lg font-medium hover:bg-[#1ed760] transition">
              Spotify
            </button>

            <button className="px-4 py-2 bg-white text-black rounded-lg font-medium hover:bg-gray-200 transition">
              Apple Music
            </button>
          </div>
        </div>

        {/* Imagens dos eventos */}
        <div className="relative h-[400px] flex items-center justify-end">

          <div className="relative w-full h-full translate-x-20 mb-20">

            {cardImages.map((card, index) => (
              <div
                key={index}
                className={`absolute ${
                  index === 0 ? 'right-20 top-8' :
                  index === 1 ? 'right-10 top-16' :
                  'right-0 top-24'
                } w-[480px] h-[360px] rounded-3xl shadow-2xl transform ${card.rotation}`}
                style={{ zIndex: card.zIndex }}
              >
                <img
                  src={card.src}
                  alt={card.alt}
                  className="w-full h-full object-cover rounded-3xl"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';

                    if (target.nextSibling) {
                      (target.nextSibling as HTMLElement).style.display = 'block';
                    }
                  }}
                />

                <div
                  className={`w-full h-full bg-gradient-to-br ${card.color} rounded-3xl hidden`}
                />
              </div>
            ))}

            {/* Texto sobre a última imagem */}
            <div
              className="absolute right-0 top-24 w-[180px] h-[260px] flex items-end p-5 pointer-events-none"
              style={{ zIndex: 40 }}
            >
              <div className="text-white bg-black/30 backdrop-blur-sm rounded-lg p-3">
                <p className="font-bold text-sm">Descubra eventos</p>
                <p className="text-xs opacity-90">na sua cidade</p>
              </div>
            </div>

          </div>
        </div>

      </div>
    </section>
  );
}
