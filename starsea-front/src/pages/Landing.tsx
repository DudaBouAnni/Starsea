import { EventCard } from '../components/EventCard';
import { ConnectSection } from '../components/ConnectSection';
import { GenreFilter } from '../components/GenreFilter';
import { NearbyVenues } from '../components/NearbyVenues';
import { FeaturedEvent } from '../components/FeaturedEvent';
import { EventGrid } from '../components/EventGrid';
import { AboutSection } from '../components/AboutSection';
import { Footer } from '../components/Footer';
import Home from './Home';

const featuredEvents = [
  {
    image: 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=600&h=400&fit=crop',
    venue: 'Sesc Belenzinhaaaaaao',
    artist: 'Ebony',
    date: '21 de nov - 20H.',
  },
  {
    image: 'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=600&h=400&fit=crop',
    venue: 'Estádio MorumBis',
    artist: 'Oasis',
    date: '22 e 23 de nov - 19H.',
  },
  {
    image: 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=400&fit=crop',
    venue: 'Cine Joia',
    artist: 'bbno$',
    date: '22 de nov - 21H.',
  },
  {
    image: 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=600&h=400&fit=crop',
    venue: 'Parque Villa Lobos',
    artist: 'Seu Jorge',
    date: '29 de nov - 11H.',
  },
  {
    image: 'https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=600&h=400&fit=crop',
    venue: 'Cine Joia',
    artist: 'Jack & Jack',
    date: '6 de dez - 19H.',
  },
  {
    image: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&h=400&fit=crop',
    venue: 'Audio',
    artist: 'Armandinho',
    date: '13 de dez - 21H.',
  },
];

export function Landing() {
  return (
    <div className="min-h-screen bg-white">
     < Home />

      <section className="bg-gray-100 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredEvents.map((event, index) => (
              <EventCard key={index} {...event} ticketLink="#" />
            ))}
          </div>
        </div>
      </section>

      <ConnectSection />
      
      <GenreFilter />
      
      <NearbyVenues />

     <FeaturedEvent
  logo="/lolla-removebg-preview.png"
  badge="ESTÁ COM A GENTE!"
  posterImage="https://i.ebayimg.com/images/g/dtsAAOSwav1kSazu/s-l1200.jpg"
  socialImage="/STARSEA.png"
  description="Indicados ao Grammy que estarão no LollaBR 2026!"
  artists={[
    "Sabrina Carpenter",
    "Chappell Roan",
    "Doechii",
    "Katseye",
  ]}
  backgroundClassName="bg-gradient-to-r from-violet-500 via-indigo-400 to-cyan-400"
  decorationClassName="bg-lime-400"
  secondaryDecorationClassName="bg-black"
/>

      <FeaturedEvent
  logo="/logorockInrio.png"
  badge="ESTÁ COM A GENTE!"
  posterImage="/STARSEA (1).png"
  socialImage="/STARSEA (2).png"
  description="2026 promete ser um ano inesquecível para o Rock in Rio!"
  artists={[
    "Artista 1",
    "Artista 2",
    "Artista 3",
  ]}
  backgroundClassName="bg-black"
  decorationClassName="bg-[#c65353]"
  secondaryDecorationClassName="bg-gradient-to-r from-violet-500 via-indigo-400 to-cyan-400"
/>

      <EventGrid />
      
      <AboutSection />
      
      <Footer />
    </div>
  );
}
