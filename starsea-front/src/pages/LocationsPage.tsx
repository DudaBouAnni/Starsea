import { useState } from "react";
import { Link } from "react-router-dom";
import { Header } from "../components/Header";

interface Location {
  id: number;
  name: string;
  city: string;
  state: string;
  capacity: number;
  image: string;
  eventCount: number;
}

export default function LocationsPage() {
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedCity, setSelectedCity] = useState<string>('all');

  const locations: Location[] = [
    {
      id: 1,
      name: "Sahal Music Hall",
      city: "São Paulo",
      state: "SP",
      capacity: 3000,
      image: "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=400",
      eventCount: 12
    },
    {
      id: 2,
      name: "Allianz Parque",
      city: "São Paulo",
      state: "SP",
      capacity: 55000,
      image: "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400",
      eventCount: 18
    },
    {
      id: 3,
      name: "Estádio Alvalade",
      city: "Lisboa",
      state: "Portugal",
      capacity: 50000,
      image: "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=400",
      eventCount: 8
    },
    {
      id: 4,
      name: "Tokio Marine Hall",
      city: "São Paulo",
      state: "SP",
      capacity: 7000,
      image: "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=400",
      eventCount: 15
    },
    {
      id: 5,
      name: "Jeunesse Arena",
      city: "Rio de Janeiro",
      state: "RJ",
      capacity: 18000,
      image: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400",
      eventCount: 22
    },
    {
      id: 6,
      name: "Espaço das Américas",
      city: "São Paulo",
      state: "SP",
      capacity: 10000,
      image: "https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=400",
      eventCount: 10
    },
    {
      id: 7,
      name: "Audio Club",
      city: "São Paulo",
      state: "SP",
      capacity: 1500,
      image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWfEBja_5XBgiFiXyYAO1fVWsA_2c0OF6q0J21jExEMs5V6nYPhE8xlN2y&s=10",
      eventCount: 25
    },
    {
      id: 8,
      name: "Vibra São Paulo",
      city: "São Paulo",
      state: "SP",
      capacity: 9000,
      image: "https://images.unsplash.com/photo-1506157786151-b8491531f063?w=400",
      eventCount: 14
    }
  ];

  const cities = ["all", ...Array.from(new Set(locations.map(loc => loc.city)))];

  const filteredLocations = locations.filter(location => {
    const matchesSearch =
      location.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      location.city.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCity = selectedCity === "all" || location.city === selectedCity;
    return matchesSearch && matchesCity;
  });

  return (
    <div className="min-h-screen bg-gray-100">
      <Header currentPage="locais" />

      <div className="max-w-7xl mx-auto px-8 py-12">
        <h1 className="text-4xl font-bold mb-8">Locais de eventos</h1>

        <div className="mb-8">
          <div className="relative max-w-2xl">
            <input
              type="text"
              placeholder="Buscar locais..."
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
          {cities.map((city) => (
            <button
              key={city}
              onClick={() => setSelectedCity(city)}
              className={`px-6 py-2 rounded-full font-medium transition ${
                selectedCity === city
                  ? "bg-gradient-to-r from-purple-500 to-cyan-400 text-white"
                  : "bg-white text-gray-700 hover:bg-gray-100"
              }`}
            >
              {city === "all" ? "Todas as cidades" : city}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredLocations.map((location) => (
            <Link
              key={location.id}
              to={`/events?venue=${location.name}`}
              className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition group"
            >
              <div className="relative aspect-video overflow-hidden bg-gray-300">
                <img
                  src={location.image}
                  alt={location.name}
                  className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                />

                <div className="absolute top-4 right-4">
                  <span className="px-3 py-1 bg-black/70 backdrop-blur-sm rounded-full text-sm font-medium text-white">
                    {location.eventCount} eventos
                  </span>
                </div>
              </div>

              <div className="p-6">
                <h3 className="text-2xl font-bold mb-2 text-gray-900">{location.name}</h3>

                <div className="space-y-2 text-gray-600">
                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span>{location.city}, {location.state}</span>
                  </div>

                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    <span>Capacidade: {location.capacity.toLocaleString("pt-BR")}</span>
                  </div>
                </div>

                <button className="mt-4 w-full py-3 bg-gradient-to-r from-purple-500 to-cyan-400 text-white rounded-lg font-bold hover:opacity-90 transition">
                  Ver eventos
                </button>
              </div>
            </Link>
          ))}
        </div>

        {filteredLocations.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg">Nenhum local encontrado</p>
          </div>
        )}
      </div>
    </div>
  );
}
