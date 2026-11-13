interface EventCardProps {
  image: string;
  venue: string;
  artist: string;
  date: string;
  ticketLink?: string;
}

export function EventCard({ image, venue, artist, date, ticketLink }: EventCardProps) {
  return (
    <div className="group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
      <div className="relative h-64 overflow-hidden">
        <img 
          src={image} 
          alt={artist}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
        />
      </div>

      <div className="p-6 space-y-3">
        <p className="text-sm text-gray-600">{venue}</p>
        <h3 className="text-2xl font-bold text-black">{artist}</h3>
        <p className="text-gray-700">{date}</p>

        {ticketLink && (
          <button className="mt-4 text-purple-600 font-bold uppercase text-sm hover:text-purple-700 transition flex items-center gap-2">
            INGRESSOS
            <span>→</span>
          </button>
        )}
      </div>
    </div>
  );
}
