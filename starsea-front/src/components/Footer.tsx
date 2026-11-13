export function Footer() {
  return (
    <footer className="bg-gradient-to-br from-purple-600 via-purple-500 to-cyan-400 py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-2 gap-12">
          <div className="space-y-8">
            <div className="flex items-center gap-3">
              <div className="w-16 h-16 rounded-full bg-white flex items-center justify-center">
                <span className="text-2xl font-bold bg-gradient-to-br from-purple-600 to-cyan-500 bg-clip-text text-transparent">S</span>
              </div>
            </div>

            <div className="space-y-4 text-white">
              <div>
                <p className="text-sm mb-1">E-mail</p>
                <a href="mailto:starsea@gmail.com" className="text-xl font-bold hover:underline">
                  STARSEA@GMAIL.COM
                </a>
              </div>

              <div>
                <p className="text-sm mb-1">Endereço</p>
                <p className="font-bold">
                  AVENIDA VIDA NOVA, 166, BAIRRO<br />
                  MARIA ROSA
                </p>
              </div>

              <div>
                <p className="text-sm mb-1">Telefone</p>
                <a href="tel:1234567890" className="text-xl font-bold hover:underline">
                  (12) 3456-7890
                </a>
              </div>
            </div>
          </div>

          <div className="space-y-8">
            <h2 className="text-4xl sm:text-5xl font-bold text-black">
              Dúvidas ou<br />comentários?
            </h2>

            <div className="flex flex-wrap gap-8 text-white font-medium">
              <a href="#sobre" className="hover:underline">Sobre</a>
              <a href="#shows" className="hover:underline">Shows</a>
              <a href="#locais" className="hover:underline">Locais</a>
              <a href="#ajuda" className="hover:underline">Ajuda</a>
            </div>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-white/20 text-center text-white/80 text-sm space-y-2">
          <p>Copyright 2025 Starsea</p>
          <div className="flex justify-center gap-4 flex-wrap">
            <a href="#termos" className="hover:underline">Termos de Uso</a>
            <span>|</span>
            <a href="#privacidade" className="hover:underline">Política de privacidade</a>
            <span>|</span>
            <a href="#cookies" className="hover:underline">Política de cookies</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
