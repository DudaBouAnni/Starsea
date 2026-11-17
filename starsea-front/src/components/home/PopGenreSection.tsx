import { Link } from 'react-router-dom';
import { MapPin, Calendar, Heart } from 'lucide-react';

interface EventCard {
  id: number;
  artist: string;
  venue: string;
  date: string;
  imageSrc: string;
  gradientFallback: string;
}

export function PopGenreSection() {
  const genres = ['Todos', 'Pop', 'Rock', 'K-pop', 'MPB', 'Jazz', 'Sertanejo', 'Funk', 'Eletrônica', 'Metal'];
  
  const events: EventCard[] = [
    { 
      id: 4, 
      artist: "Jorge Ben Jor", 
      venue: "Espaço Unimed - 3 km", 
      date: "21 fev - 23h", 
      imageSrc: "https://i.scdn.co/image/ab67616d0000b2737929fff46ec30800c842042d",
      gradientFallback: "from-yellow-400 to-orange-600"
    },
    { 
      id: 5, 
      artist: "Tyler, The Creator", 
      venue: "Allianz Parque - 14 km", 
      date: "15 mar - 21h", 
      imageSrc: "https://i.scdn.co/image/ab6761610000e5eb8278b782cbb5a3963db88ada",
      gradientFallback: "from-pink-500 to-rose-600"
    },
    { 
      id: 6, 
      artist: "Doja Cat", 
      venue: "Sahal Music Hall - 12 km", 
      date: "05 fev - 23h", 
      imageSrc: "https://i.scdn.co/image/ab6761610000e5ebe94f88ff74ae4ddcab961f97",
      gradientFallback: "from-pink-600 to-purple-700"
    },
    { 
      id: 7, 
      artist: "Oasis", 
      venue: "Estádio Alvalade - 16 km", 
      date: "21 e 22 fev - 19h", 
      imageSrc: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjyMH3jCo17OwKw2q6_tOszhm9XPuGtJytcgY19NFfqQ&s=10",
      gradientFallback: "from-blue-700 to-indigo-900"
    },
  ];

  return (
    <section className="bg-white py-16 px-12">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold mb-6">
          Em alta em <span className="text-purple-600">São Paulo</span>
        </h2>

        <div className="flex gap-3 mb-8 overflow-x-auto pb-2">
          {genres.map((genre, index) => (
            <button
              key={genre}
              className={`px-5 py-2 rounded-full text-sm font-medium whitespace-nowrap transition ${
                index === 0
                  ? 'bg-purple-600 text-white'
                  : 'bg-white border-2 border-purple-300 text-purple-600 hover:bg-purple-50'
              }`}
            >
              {genre}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {events.map((event) => (
            <div key={event.id} className="group">
              <Link to={`/event/${event.id}`} className="block relative">
                <div className="aspect-[4/5] rounded-2xl mb-3 shadow-md group-hover:shadow-xl transition relative overflow-hidden">
                  <img
                    src={event.imageSrc}
                    alt={event.artist}
                    className="absolute inset-0 w-full h-full object-cover"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.style.display = 'none';
                      if (target.nextSibling) {
                        (target.nextSibling as HTMLElement).style.display = 'block';
                      }
                    }}
                  />
                  
                  <div className={`absolute inset-0 bg-gradient-to-br ${event.gradientFallback} hidden`}></div>
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>

                  <button className="absolute top-3 right-3 w-8 h-8 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center hover:bg-white/30 transition z-10">
                    <Heart className="w-4 h-4 text-white" />
                  </button>
                  
                  <div className="absolute bottom-3 left-3 z-10">
                    <span className="px-3 py-1 bg-black/70 backdrop-blur-sm text-white text-xs font-bold rounded-lg">
                      Pop
                    </span>
                  </div>
                </div>
                
                <div className="space-y-1">
                  <h3 className="font-bold text-base text-gray-900">{event.artist}</h3>
                  <p className="text-xs text-gray-600 flex items-center gap-1">
                    <MapPin className="w-3 h-3" />
                    {event.venue}
                  </p>
                  <p className="text-xs text-gray-600 flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    {event.date}
                  </p>
                  <p className="text-purple-600 font-bold text-sm mt-2">
                    a partir de R$ 120 <span className="text-xs font-normal text-gray-500">INGRESSOS →</span>
                  </p>
                </div>
              </Link>
            </div>
          ))}
        </div>

        <div className="text-center mt-8">
          <button className="px-8 py-3 border-2 border-gray-300 rounded-full font-medium text-gray-700 hover:border-purple-500 hover:text-purple-600 transition">
            CARREGAR MAIS
          </button>
        </div>
      </div>
    </section>
  );
}
