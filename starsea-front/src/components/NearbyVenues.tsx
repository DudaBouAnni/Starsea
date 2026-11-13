import { VenueCard } from './VenueCard';

const venues = [
  {
    image: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=600&h=400&fit=crop',
    name: 'Allianz Parque',
    city: 'São Paulo',
  },
  {
    image: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&h=400&fit=crop',
    name: 'Espaço Unimed',
    city: 'São Paulo',
  },
  {
    image: 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=600&h=400&fit=crop',
    name: 'Audio',
    city: 'São Paulo',
  },
  {
    image: 'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=600&h=400&fit=crop',
    name: 'Anhembi Sambadrome',
    city: 'São Paulo',
  },
  {
    image: 'https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=600&h=400&fit=crop',
    name: 'Autódromo Interlagos',
    city: 'São Paulo',
  },
  {
    image: 'https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=600&h=400&fit=crop',
    name: 'Estádio MorumBis',
    city: 'São Paulo',
  },
];

export function NearbyVenues() {
  return (
    <section className="bg-gray-50 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-4xl sm:text-5xl font-bold text-black mb-12">
          Locais próximos de você
        </h2>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {venues.map((venue, index) => (
            <VenueCard key={index} {...venue} />
          ))}
        </div>
      </div>
    </section>
  );
}
