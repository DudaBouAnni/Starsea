import { useState } from "react";
import { Link } from "react-router-dom";
import { Header } from "../components/Header";

interface Event {
  id: number;
  name: string;
  artist: string;
  date: string;
  venue: string;
  city: string;
  image: string;
  genre: string;
}

export default function EventsPage() {
  const [searchTerm, setSearchTerm] = useState<string>('');

  const events: Event[] = [
    {
      id: 1,
      name: "Doja Cat",
      artist: "Doja Cat",
      date: "05 de fevereiro",
      venue: "Sahal Music Hall",
      city: "São Paulo",
      image: "https://i.scdn.co/image/ab6761610000e5eb8a0644455ebfa7d3976f5101",
      genre: "Pop"
    },
    {
      id: 2,
      name: "Oasis Reunion Tour",
      artist: "Oasis",
      date: "22 de novembro",
      venue: "Estádio Alvalade",
      city: "Lisboa",
      image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRFxNWry7lPuLtL9NoRM5qAlUxPTDaUYDnq8m17j0HN6K2IUCs-4xJpxPtD&s=10",
      genre: "Rock"
    },
    {
      id: 3,
      name: "My Chemical Romance",
      artist: "My Chemical Romance",
      date: "06 e 08 de fevereiro",
      venue: "Allianz Parque",
      city: "São Paulo",
      image: "https://i.scdn.co/image/ab6761610000e5eb0c55e74e435910793888f7cf",
      genre: "Rock"
    }
  ];

  const filteredEvents = events.filter(event =>
    event.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    event.artist.toLowerCase().includes(searchTerm.toLowerCase()) ||
    event.city.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <Header currentPage="events" />

      <div className="max-w-7xl mx-auto px-8 py-12">
        <div className="mb-12">
          <div className="relative max-w-2xl">
            <input
              type="text"
              placeholder="Buscar eventos, artistas ou cidades..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-6 py-4 rounded-full border-2 border-gray-300 focus:border-purple-500 focus:outline-none text-lg"
            />
            <button className="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2 bg-gradient-to-r from-purple-500 to-cyan-400 rounded-full text-white font-bold hover:opacity-90">
              Buscar
            </button>
          </div>
        </div>

        <div className="flex gap-3 mb-8 flex-wrap">
          <button className="px-6 py-2 bg-gradient-to-r from-purple-500 to-cyan-400 text-white rounded-full font-medium hover:opacity-90">
            Todos
          </button>
          <button className="px-6 py-2 bg-white text-gray-700 rounded-full font-medium hover:bg-gray-100">
            Pop
          </button>
          <button className="px-6 py-2 bg-white text-gray-700 rounded-full font-medium hover:bg-gray-100">
            Rock
          </button>
          <button className="px-6 py-2 bg-white text-gray-700 rounded-full font-medium hover:bg-gray-100">
            Hip Hop
          </button>
          <button className="px-6 py-2 bg-white text-gray-700 rounded-full font-medium hover:bg-gray-100">
            Eletrônica
          </button>
          <button className="px-6 py-2 bg-white text-gray-700 rounded-full font-medium hover:bg-gray-100">
            São Paulo
          </button>
          <button className="px-6 py-2 bg-white text-gray-700 rounded-full font-medium hover:bg-gray-100">
            Rio de Janeiro
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredEvents.map((event) => (
            <Link
              key={event.id}
              to={`/event/${event.id}`}
              className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition group"
            >
              <div className="relative aspect-square overflow-hidden bg-gradient-to-br from-purple-500 to-cyan-400">
                <img
                  src={event.image}
                  alt={event.name}
                  className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                />

                <div className="absolute top-4 left-4">
                  <span className="px-3 py-1 bg-white/90 backdrop-blur-sm rounded-full text-sm font-medium text-gray-800">
                    {event.genre}
                  </span>
                </div>
              </div>

              <div className="p-6">
                <h3 className="text-2xl font-bold mb-2 text-gray-900">{event.name}</h3>

                <div className="space-y-2 text-gray-600">
                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span>{event.date}</span>
                  </div>

                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span>{event.venue}</span>
                  </div>

                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                    </svg>
                    <span>{event.city}</span>
                  </div>
                </div>

                <button className="mt-4 w-full py-3 bg-gradient-to-r from-purple-500 to-cyan-400 text-white rounded-lg font-bold hover:opacity-90 transition">
                  Ver ingressos
                </button>
              </div>
            </Link>
          ))}
        </div>

        {filteredEvents.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg">Nenhum evento encontrado</p>
          </div>
        )}
      </div>
    </div>
  );
}
