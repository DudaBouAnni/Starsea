interface VenueCardProps {
  image: string;
  name: string;
  city: string;
}

export function VenueCard({ image, name, city }: VenueCardProps) {
  return (
    <div className="group cursor-pointer">
      <div className="relative h-64 rounded-lg overflow-hidden mb-4">
        <img 
          src={image} 
          alt={name}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
        />
      </div>
      <h3 className="text-2xl font-bold text-black">{name}</h3>
      <p className="text-gray-600">{city}</p>
    </div>
  );
}
