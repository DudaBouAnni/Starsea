import { useState } from "react";
import { Link } from "react-router-dom";
import { Header } from "../components/Header";

interface Genre {
  id: number;
  name: string;
  image: string;
  eventCount: number;
}

export default function GenresPage() {
  const [searchTerm, setSearchTerm] = useState<string>('');

  const genres: Genre[] = [
    {
      id: 1,
      name: "Pop",
      image: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819",
      eventCount: 24
    },
    {
      id: 2,
      name: "Rock",
      image: "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee",
      eventCount: 18
    },
    {
      id: 3,
      name: "Hip Hop",
      image: "https://images.unsplash.com/photo-1501386761578-eac5c94b800a",
      eventCount: 15
    },
    {
      id: 4,
      name: "Eletrônica",
      image: "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3",
      eventCount: 32
    },
    {
      id: 5,
      name: "Indie",
      image: "https://images.unsplash.com/photo-1524368535928-5b5e00ddc76b",
      eventCount: 12
    },
    {
      id: 6,
      name: "R&B",
      image: "https://images.unsplash.com/photo-1516280440614-37939bbacd81",
      eventCount: 9
    },
    {
      id: 7,
      name: "Jazz",
      image: "https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f",
      eventCount: 7
    },
    {
      id: 8,
      name: "Reggae",
      image: "https://images.unsplash.com/photo-1524368535928-5b5e00ddc76b",
      eventCount: 5
    },
    {
      id: 9,
      name: "Metal",
      image: "https://images.unsplash.com/photo-1506157786151-b8491531f063",
      eventCount: 11
    },
    {
      id: 10,
      name: "Funk",
      image: "https://images.unsplash.com/photo-1540039155733-5bb30b53aa14",
      eventCount: 14
    },
    {
      id: 11,
      name: "Sertanejo",
      image: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
      eventCount: 22
    },
    {
      id: 12,
      name: "MPB",
      image: "https://images.unsplash.com/photo-1510915361894-db8b60106cb1",
      eventCount: 8
    }
  ];

  const filteredGenres = genres.filter(genre =>
    genre.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <Header currentPage="genres" />

      <div className="max-w-7xl mx-auto px-8 py-12">
        <h1 className="text-4xl font-bold mb-8">Gêneros musicais</h1>

        <div className="mb-12">
          <div className="relative max-w-2xl">
            <input
              type="text"
              placeholder="Buscar gêneros..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-6 py-4 rounded-full border-2 border-gray-300 focus:border-purple-500 focus:outline-none text-lg"
            />
            <button className="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2 bg-gradient-to-r from-purple-500 to-cyan-400 rounded-full text-white font-bold hover:opacity-90">
              Buscar
            </button>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {filteredGenres.map((genre) => (
            <Link
              key={genre.id}
              to={`/events?genre=${genre.name}`}
              className="group relative aspect-square rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition"
            >
              <div
                className="absolute inset-0 bg-cover bg-center transition-transform group-hover:scale-110 duration-300"
                style={{ backgroundImage: `url(${genre.image})` }}
              />

              <div className="absolute inset-0 bg-black/40 group-hover:bg-black/50 transition" />

              <div className="relative h-full flex flex-col items-center justify-center p-6 text-white">
                <h3 className="text-3xl font-bold mb-2 text-center">
                  {genre.name}
                </h3>
                <p className="text-white/80 text-sm">
                  {genre.eventCount} eventos
                </p>
              </div>
            </Link>
          ))}
        </div>

        {filteredGenres.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg">
              Nenhum gênero encontrado
            </p>
          </div>
        )}
      </div>
    </div>
  );
}