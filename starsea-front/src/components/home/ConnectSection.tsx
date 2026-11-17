export function ConnectSection() {
  return (
    <section className="bg-[#1a1a1a] py-16 px-12">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-3xl font-bold text-white mb-3">Conecte-se</h2>
        <p className="text-gray-400 text-sm mb-8">
          Fique por dentro de concertos e festivais de artistas que você realmente escuta.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button className="px-8 py-3 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-lg transition">
            CONECTAR SPOTIFY
          </button>
          <button className="px-8 py-3 bg-white hover:bg-gray-100 text-black font-bold rounded-lg transition">
            CONECTAR APPLE MUSIC
          </button>
        </div>
      </div>
    </section>
  );
}
