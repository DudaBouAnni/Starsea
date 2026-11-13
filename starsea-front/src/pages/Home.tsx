
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
  { label: "Fazer login", href: "#login" },
];

const artistImages: ArtistImage[] = [
  {
    src: "https://i.scdn.co/image/ab67616d0000b273684ecc5bc1b724d0106ad694",
    alt: "Artista ao fundo",
  },
  {
    src: "https://i.scdn.co/image/ab67616d0000b2738baf677ee2d8dda6cc9fcbd7?w=400",
    alt: "Retrato de artista",
  },
  {
    src: "https://i.scdn.co/image/ab67616d0000b2738baf677ee2d8dda6cc9fcbd7?w=400",
    alt: "Artista em destaque",
  },
  {
    src: "https://i.scdn.co/image/ab67616d0000b273684ecc5bc1b724d0106ad694",
    alt: "Artista principal",
  },
];

function Navbar() {
  return (
    <header className="flex h-[110px] w-full items-center justify-between px-[3.7%] max-lg:h-[90px] max-md:h-auto max-md:min-h-[80px] max-md:px-5">


 <a href="/" className="flex shrink-0 items-center gap-3 text-white">
  <img
    src="/sea-logo.png"
    alt="Logo"
    className="h-24 w-auto max-w-[340px] object-contain sm:h-28 sm:max-w-[400px] lg:h-32 lg:max-w-[450px]"
  />
</a>

    
      <nav className="flex items-center gap-8 text-lg font-normal tracking-wide text-white max-lg:gap-5 max-md:gap-3 max-md:text-[10px]">
        <a
          href="#buscar"
          aria-label="Buscar"
          className="transition-opacity hover:opacity-70"
        >
          <Search size={23} className="max-md:h-4 max-md:w-4" />
        </a>

        {navigationItems.map((item, index) => (
          <div
            key={item.label}
            className="flex items-center gap-8 max-lg:gap-5 max-md:gap-3"
          >
            {index === 2 && (
              <span className="h-5 w-px bg-white/80 max-md:h-3" />
            )}

            <a
              href={item.href}
              className="whitespace-nowrap transition-opacity hover:opacity-70"
            >
              {item.label}
            </a>
          </div>
        ))}

        <a
          href="#cadastro"
          className="whitespace-nowrap rounded-full bg-gradient-to-r from-violet-500 to-cyan-400 px-5 py-3 transition-transform hover:scale-105 max-md:px-3 max-md:py-2"
        >
          Cadastre-se
        </a>
      </nav>
    </header>
  );
}

function ArtistCollage() {
  return (
    <div className="relative mx-auto aspect-[680/700] w-full max-w-[570px]">

      <div className="absolute left-0 top-0 z-0 aspect-square w-[75%] overflow-hidden rounded-[4px] bg-white">
        <img
          src={artistImages[0].src}
          alt={artistImages[0].alt}
          className="h-full w-full object-cover grayscale"
        />
      </div>

      <div className="absolute left-[7%] top-[9%] z-10 aspect-square w-[75%] overflow-hidden rounded-[4px] bg-neutral-900">
        <img
          src={artistImages[1].src}
          alt={artistImages[1].alt}
          className="h-full w-full object-cover grayscale brightness-75"
        />
      </div>

      <div className="absolute left-[17%] top-[19%] z-20 aspect-square w-[75%] overflow-hidden rounded-[4px] bg-neutral-900">
        <img
          src={artistImages[2].src}
          alt={artistImages[2].alt}
          className="h-full w-full object-cover brightness-75"
        />
      </div>

      <div className="absolute left-[25.5%] top-[27%] z-30 aspect-square w-[75%] overflow-hidden rounded-[4px] bg-neutral-800">
        <img
          src={artistImages[3].src}
          alt={artistImages[3].alt}
          className="h-full w-full object-cover"
        />
      </div>

    </div>
  );
}

function Hero() {
  return (
    <main className="flex min-h-[calc(100vh-110px)] items-center justify-between gap-6 px-[5.5%] pb-4 max-lg:min-h-[calc(100vh-90px)] max-md:min-h-0 max-md:flex-col max-md:justify-center max-md:gap-8 max-md:px-6 max-md:py-10">

      <section className="z-30 w-[47%] shrink-0 max-lg:w-[46%] max-md:w-full">

        <h1 className="text-[80px] font-extrabold leading-[1.12] tracking-tight text-white max-xl:text-6xl max-lg:text-5xl max-md:text-5xl">
          Navegue no
          <br />
          mar de
          <br />
          eventos
        </h1>

        <p className="mb-7 mt-7 text-[28px] font-normal tracking-[0.18em] text-white max-xl:text-xl max-lg:mt-5 max-md:text-base">
          A MÚSICA TE GUIA
        </p>

        <a
          href="#eventos"
          className="flex h-[58px] w-[370px] max-w-full items-center justify-center rounded-lg bg-gradient-to-r from-violet-500 to-cyan-400 text-base font-extrabold tracking-[0.3em] text-white transition-transform hover:-translate-y-1 max-lg:h-12 max-lg:w-[300px] max-md:h-11"
        >
          BUSCAR
        </a>
      </section>

      {/* Composição de imagens */}
      <section className="w-[51%] max-md:w-full">
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
