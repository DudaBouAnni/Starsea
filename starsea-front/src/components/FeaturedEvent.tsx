interface FeaturedEventProps {
  logo: string;
  badge: string;
  posterImage: string;
  socialImage: string;
  description: string;
  artists: string[];
  backgroundClassName?: string;
  decorationClassName?: string;
  secondaryDecorationClassName?: string;
}

export function FeaturedEvent({
  logo,
  badge,
  posterImage,
  socialImage,
  description,
  artists,
  backgroundClassName = "bg-gradient-to-r from-violet-500 via-indigo-400 to-cyan-400",
  decorationClassName = "bg-lime-400",
  secondaryDecorationClassName = "bg-black",
}: FeaturedEventProps) {
  return (
    <section
      className={`relative isolate overflow-hidden py-16 sm:py-20 ${backgroundClassName}`}
    >
      <div
        className={`pointer-events-none absolute left-[-8%] top-[42%] z-0 h-[40%] w-[116%] rounded-[50%] ${decorationClassName}`}
      />
      <div
        className={`pointer-events-none absolute left-[-8%] top-[54%] z-0 h-[55%] w-[116%] rounded-[50%] ${secondaryDecorationClassName}`}
      />

      <div className="relative z-10 mx-auto max-w-6xl px-5 sm:px-8">

        <div className="relative mx-auto mb-16 min-h-[180px] w-full max-w-[820px]">

          <div className="absolute inset-0 z-10 flex items-center justify-center rounded-[20px] bg-purple-600 pl-[30%] pr-6">
            <span className="text-center text-sm font-extrabold tracking-[0.2em] text-white sm:text-xl">
              {badge}
            </span>
          </div>

          <div className="absolute left-0 top-1/2 z-20 flex w-[43%] -translate-y-1/2 items-center justify-center">
            <img
              src={logo}
              alt="Logo do festival"
              className={`block h-auto w-[100%] max-w-none object-contain ${logo}`}
            />
          </div>
        </div>

        <div className="grid grid-cols-1 items-stretch gap-8 md:grid-cols-2 md:gap-12">
          <div className="overflow-hidden rounded-xl shadow-2xl">
            <img
              src={posterImage}
              alt="Cartaz do festival"
              className="block h-full w-full object-cover"
            />
          </div>

          <div className="flex flex-col overflow-hidden rounded-xl bg-white shadow-2xl">
            <img
              src={socialImage}
              alt="Conteúdo social do festival"
              className="block w-full flex-1 object-cover"
            />

            <div className="space-y-4 bg-white p-5 sm:p-6">
              <div className="rounded-lg bg-cyan-400 p-4">
                <p className="font-medium leading-relaxed text-neutral-950">
                  {description}
                </p>
              </div>

              <p className="text-sm leading-relaxed text-neutral-800">
                Você quis dizer:{" "}
                {artists.map((artist, index) => (
                  <span key={`${artist}-${index}`}>
                    <span className="font-semibold underline">{artist}</span>
                    {index < artists.length - 1 && " • "}
                  </span>
                ))}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
