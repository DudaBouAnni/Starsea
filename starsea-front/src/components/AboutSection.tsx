export function AboutSection() {
  return (
    <section className="bg-gray-50 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <div>
              <p className="text-sm uppercase tracking-wider text-gray-600 mb-2">
                SOBRE NÓS
              </p>
              <h2 className="text-4xl sm:text-5xl font-bold mb-4">
                <span className="bg-gradient-to-r from-purple-500 to-cyan-500 bg-clip-text text-transparent">
                  Starsea, a música te guia
                </span>
              </h2>
              <p className="text-gray-700 text-lg">
                O Starsea conecta você aos seus artistas favoritos de forma única. 
                Com base no que você escuta, avisamos sempre que eles estiverem 
                fazendo shows perto de você.
              </p>
            </div>

            <div>
              <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-500 to-cyan-500 bg-clip-text text-transparent mb-4">
                Onde a música te encontra!
              </h3>
            </div>

            <div className="flex gap-4 overflow-hidden">
              <div className="w-32 h-32 rounded-lg overflow-hidden flex-shrink-0">
                <img 
                  src="https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=200&h=200&fit=crop" 
                  alt="Album 1"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="w-32 h-32 rounded-lg overflow-hidden flex-shrink-0">
                <img 
                  src="https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=200&h=200&fit=crop" 
                  alt="Album 2"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="w-32 h-32 rounded-lg overflow-hidden flex-shrink-0">
                <img 
                  src="https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=200&h=200&fit=crop" 
                  alt="Album 3"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>

          <div className="relative">
            <div className="bg-white rounded-2xl p-8 shadow-xl">
              <img 
                src="https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=600&h=800&fit=crop" 
                alt="Concert"
                className="w-full h-96 object-cover rounded-lg mb-6"
              />
              
              <div className="space-y-4">
                <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-500 to-cyan-500 bg-clip-text text-transparent">
                  O SHOW TE ESPERA
                </h3>
                <p className="text-gray-700">
                  Queremos que você aproveite cada momento da música ao vivo, 
                  seja em grandes palcos ou em shows mais intimistas. Acreditamos 
                  que a música é feita para ser vivida, e estamos aqui para 
                  garantir que você não perca nenhuma oportunidade.
                </p>
                <button className="px-6 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-cyan-500 text-white font-bold uppercase hover:opacity-90 transition">
                  SAIBA MAIS
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
