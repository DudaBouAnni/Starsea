export function Hero() {
  return (
    <section className="relative min-h-screen bg-black flex items-center overflow-hidden pt-16">
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-black to-cyan-900/20" />
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <h1 className="text-6xl sm:text-7xl lg:text-8xl font-bold text-white leading-tight">
              Navegue no mar de eventos
            </h1>
            <p className="text-xl sm:text-2xl text-white/60 uppercase tracking-wider">
              A música te guia
            </p>
            <button className="px-8 py-4 rounded-lg bg-gradient-to-r from-purple-500 to-cyan-500 text-white text-lg font-medium hover:opacity-90 transition transform hover:scale-105">
              BUSCAR
            </button>
          </div>

          <div className="relative hidden lg:block">
            <div className="relative w-full h-[600px]">
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-96 rounded-2xl overflow-hidden shadow-2xl z-10">
                <img 
                  src="https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600&h=800&fit=crop" 
                  alt="Artist"
                  className="w-full h-full object-cover"
                />
              </div>
              
              <div className="absolute top-0 left-0 w-48 h-64 bg-purple-600/20 rounded-lg transform -rotate-6" />
              <div className="absolute bottom-0 right-0 w-56 h-72 bg-cyan-600/20 rounded-lg transform rotate-6" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
