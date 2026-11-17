import { Link } from 'react-router-dom';

interface Venue {
  name: string;
  city: string;
  imageSrc: string;
  gradientFallback: string;
}

export function NearbyVenuesSection() {
  const venues: Venue[] = [
    { 
      name: "Allianz Parque", 
      city: "São Paulo - 8 eventos", 
      imageSrc: "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400&h=400&fit=crop",
      gradientFallback: "from-blue-700 to-indigo-900"
    },
    { 
      name: "Espaço Unimed", 
      city: "São Paulo - 12 eventos", 
      imageSrc: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400&h=400&fit=crop",
      gradientFallback: "from-green-500 to-lime-400"
    },
    { 
      name: "Audio", 
      city: "São Paulo - 6 eventos", 
      imageSrc: "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=400&h=400&fit=crop",
      gradientFallback: "from-gray-700 to-gray-900"
    },
    { 
      name: "Anhembi", 
      city: "São Paulo - 4 eventos", 
      imageSrc: "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=400&h=400&fit=crop",
      gradientFallback: "from-orange-500 to-pink-600"
    },
    { 
      name: "Autódromo Interlagos", 
      city: "São Paulo - 3 eventos", 
      imageSrc: "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=400&h=400&fit=crop",
      gradientFallback: "from-teal-600 to-cyan-700"
    },
    { 
      name: "Estádio MorumBis", 
      city: "São Paulo - 5 eventos", 
      imageSrc: "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=400&h=400&fit=crop",
      gradientFallback: "from-purple-600 to-pink-600"
    },
  ];

  return (
    <section className="bg-white py-16 px-12">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold mb-8">Locais próximos de você</h2>
        
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-6">
          {venues.map((venue, index) => (
            <Link key={index} to="/locais" className="group">
              <div className="aspect-square rounded-3xl mb-3 shadow-md group-hover:shadow-xl transition overflow-hidden relative">
                <img
                  src={venue.imageSrc}
                  alt={venue.name}
                  className="absolute inset-0 w-full h-full object-cover"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';
                    if (target.nextSibling) {
                      (target.nextSibling as HTMLElement).style.display = 'block';
                    }
                  }}
                />
                
                <div className={`absolute inset-0 bg-gradient-to-br ${venue.gradientFallback} hidden`}></div>
                <div className="absolute inset-0 bg-black/20"></div>
              </div>
              <h3 className="font-bold text-sm text-gray-900">{venue.name}</h3>
              <p className="text-xs text-gray-600">{venue.city}</p>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
