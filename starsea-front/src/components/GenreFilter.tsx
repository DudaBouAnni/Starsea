const genres = [
  'Pop', 'Rock', 'Blues', 'MPB', 'Jazz', 'K-pop', 
  'Gospel', 'Clássica', 'Sertanejo', 'Metal'
];

export function GenreFilter() {
  return (
    <section className="bg-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-4 overflow-x-auto pb-2 scrollbar-hide">
          {genres.map((genre) => (
            <button
              key={genre}
              className="px-6 py-2 rounded-full border-2 border-purple-400 text-purple-600 font-medium whitespace-nowrap hover:bg-purple-500 hover:text-white transition"
            >
              {genre}
            </button>
          ))}
          <button className="px-6 py-2 rounded-full border-2 border-purple-400 text-purple-600 font-medium whitespace-nowrap hover:bg-purple-500 hover:text-white transition">
            →
          </button>
        </div>
      </div>
    </section>
  );
}
