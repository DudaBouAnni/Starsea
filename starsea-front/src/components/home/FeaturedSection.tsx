import { Link } from 'react-router-dom';

interface EventCard {
  id: number;
  artist: string;
  venue: string;
  matchPercentage: string;
  imageSrc: string;
  gradientFallback: string;
}

export function FeaturedSection() {
  const events: EventCard[] = [
    { 
      id: 1, 
      artist: "Doja Cat", 
      venue: "Sahal Music Hall - 05 fev", 
      matchPercentage: "Match 93%", 
      imageSrc: "https://i.scdn.co/image/ab6761610000e5eb8a0644455ebfa7d3976f5101",
      gradientFallback: "from-pink-500 to-purple-600"
    },
    { 
      id: 2, 
      artist: "My Chemical Romance", 
      venue: "Allianz Parque - 06 e 08 fev", 
      matchPercentage: "Match 87%", 
      imageSrc: "https://i.scdn.co/image/ab6761610000e5eb0c55e74e435910793888f7cf",
      gradientFallback: "from-gray-700 to-gray-900"
    },
    { 
      id: 3, 
      artist: "Kali Uchis", 
      venue: "Vibra São Paulo - 08 fev", 
      matchPercentage: "Match 81%", 
      imageSrc: "https://poptivo.com.br/wp-content/uploads/2024/06/Kali-uchis.jpeg",
      gradientFallback: "from-orange-400 to-purple-600"
    },
  ];

  return (
    <section className="bg-gray-50 py-16 px-12">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-baseline gap-2">
            <h2 className="text-3xl font-bold text-gray-900">Porque você ouve</h2>
            <span className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-500 bg-clip-text text-transparent">
              Ariana Grande
            </span>
            <span className="text-3xl font-bold text-gray-900">e mais</span>
          </div>
          <Link to="/events" className="text-purple-600 font-semibold hover:underline text-sm">
            Ver tudo →
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {events.map((event) => (
            <Link
              key={event.id}
              to={`/event/${event.id}`}
              className="group relative aspect-[3/4] rounded-3xl overflow-hidden shadow-md hover:shadow-2xl transition"
            >
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
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
              
              <div className="absolute top-4 left-4 z-10">
                <span className="px-3 py-1 bg-black/70 backdrop-blur-sm text-white text-xs font-bold rounded-full">
                  {event.matchPercentage}
                </span>
              </div>

              <div className="absolute bottom-0 left-0 right-0 p-6 z-10">
                <h3 className="text-white font-bold text-2xl mb-2">{event.artist}</h3>
                <p className="text-white/90 text-sm">{event.venue}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
