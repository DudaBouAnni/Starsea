import { EventCard } from './EventCard';

const events = [
  {
    image: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&h=400&fit=crop',
    venue: 'Suhai Music Hall',
    artist: 'Doja Cat',
    date: '05 de fev, 2026.',
  },
  {
    image: 'https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=600&h=400&fit=crop',
    venue: 'Allianz Parque',
    artist: 'My Chemical Romance',
    date: '05 e 06 de fev, 2026.',
  },
  {
    image: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop',
    venue: 'Vibra São Paulo',
    artist: 'Kali Uchis',
    date: '08 de fev, 2026.',
  },
  {
    image: 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=600&h=400&fit=crop',
    venue: 'Allianz Parque',
    artist: 'Bad Bunny',
    date: '20 e 21 de fev, 2026.',
  },
  {
    image: 'https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=600&h=400&fit=crop',
    venue: 'Mercado Livre Arena',
    artist: 'Rüfus du Sol',
    date: '25 a 27 de fev, 2026',
  },
  {
    image: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=600&h=400&fit=crop',
    venue: 'Espaço Unimed',
    artist: 'Big Time Rush',
    date: '06 de mar, 2026,',
  },
];

export function EventGrid() {
  return (
    <section className="bg-black py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-4xl sm:text-5xl font-bold mb-12">
          <span className="text-white">Shows em </span>
          <span className="bg-gradient-to-r from-purple-500 to-cyan-500 bg-clip-text text-transparent italic">
            São Paulo 2026
          </span>
        </h2>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {events.map((event, index) => (
            <EventCard key={index} {...event} ticketLink="#" />
          ))}
        </div>

        <div className="text-center">
          <button className="px-8 py-3 rounded-full bg-white text-purple-600 font-bold uppercase hover:bg-gray-100 transition">
            CARREGAR MAIS
          </button>
        </div>
      </div>
    </section>
  );
}
