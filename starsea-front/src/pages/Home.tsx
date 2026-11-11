
import { Search } from "lucide-react";

type NavigationItem = {
  label: string;
  href: string;
};

type ArtistImage = {
  src: string;
  alt: string;
};

const navigationItems: NavigationItem[] = [
  { label: "Eventos", href: "#eventos" },
  { label: "Gêneros", href: "#generos" },
  { label: "Fazer Login", href: "#login" },
];

const artistImages: ArtistImage[] = [
  {
    src:"https://i.scdn.co/image/ab67616d0000b273684ecc5bc1b724d0106ad694",
    alt: "Artista em destaque",
  },
  {
    src: "https://i.scdn.co/image/ab67616d0000b2738baf677ee2d8dda6cc9fcbd7?w=400",
    alt: "Retrato de artista",
  },
  
];

function Navbar() {
  return (
    <header className="flex h-[72px] items-center justify-between px-[5%]">
      <a href="/" className="flex items-center gap-2 text-white">
        <span className="h-8 w-8 rounded-full bg-gradient-to-br from-violet-500 to-cyan-400" />
        <span className="text-sm font-bold">Starsea</span>
      </a>

      <nav className="flex items-center gap-5 text-xs font-semibold text-white">
        <a href="#buscar" aria-label="Buscar">
          <Search size={15} />
        </a>

        {navigationItems.map((item, index) => (
          <div key={item.label} className="flex items-center gap-5">
            {index === 2 && (
              <span className="h-4 w-px bg-neutral-600" />
            )}

            <a
              href={item.href}
              className="transition-opacity hover:opacity-70"
            >
              {item.label}
            </a>
          </div>
        ))}

        <a
          href="#cadastro"
          className="rounded-full bg-gradient-to-r from-violet-500 to-cyan-400 px-4 py-2"
        >
          Cadastre-se
        </a>
      </nav>
    </header>
  );
}

function ArtistCollage() {
  return (
    <div className="relative h-[540px] w-full max-w-[950px]">
      {/* Imagem de fundo */}
      <div className="absolute left-[3%] top-0 z-0 h-[85%] w-[82%] overflow-hidden">
        <img
          src={artistImages[0].src}
          alt={artistImages[0].alt}
          className="h-full w-full object-cover"
        />
      </div>

      {/* Imagem intermediária */}
      <div className="absolute left-[15%] top-[18%] z-10 h-[89%] w-[82%] overflow-hidden">
        <img
          src={artistImages[1].src}
          alt={artistImages[1].alt}
          className="h-full w-full object-cover grayscale"
        />
      </div>

      {/* Imagem em destaque */}
    
    </div>
  );
}

function Hero() {
  return (
    <main className="flex min-h-[calc(100vh-72px)] items-center justify-between gap-8 px-[5%]">
      <section className="z-30 w-[45%]">
        <h1 className="text-5xl font-extrabold leading-[1.04] tracking-tight text-white md:text-6xl lg:text-7xl">
          Navegue no
          <br />
          mar de
          <br />
          eventos
        </h1>

        <p className="mb-7 mt-6 text-lg font-bold text-white">
          A MÚSICA TE GUIA
        </p>

        <a
          href="#eventos"
          className="flex h-11 w-[260px] max-w-full items-center justify-center rounded-md bg-gradient-to-r from-violet-500 to-cyan-400 text-xs font-extrabold text-white transition-transform hover:-translate-y-1"
        >
          BUSCAR
        </a>
      </section>

      <section className="w-[50%]">
        <ArtistCollage />
      </section>
    </main>
  );
}

export default function Home() {
  return (
    <div className="min-h-screen overflow-hidden bg-[#191919]">
      <Navbar />
      <Hero />
    </div>
  );
}
