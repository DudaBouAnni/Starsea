import { Link } from 'react-router-dom';

interface FeaturedEventData {
  name: string;
  venue: string;
  img: string;
}

export function FeaturedEventsSection() {
  const featured: FeaturedEventData[] = [
    {
      name: "#LollaBR 2026",
      venue: "Sabrina Carpenter, Chappell Roan, Tyler, The Creator e mais",
      img: "https://p2.trrsf.com/image/fget/cf/940/0/images.terra.com/2026/03/25/636880049-mceclip3-1774460703.jpg",
    },
    {
      name: "Rock In Rio",
      venue: "Veja line-up, datas e como chegar",
      img: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQMN92Bs32sD5SYZLJ7nSFhYvWUFundeDfowfDyclmtXI-k1JhLAyr6ZQ3p&s=10",
    },
  ];

  return (
    <section className="bg-gray-50 py-16 px-12">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold mb-8">Festivais de 2026</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {featured.map((event, index) => (
            <Link
              key={index}
              to="/events"
              className="group relative aspect-[5/3] rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition"
            >
              {/* Imagem de fundo */}
              <div
                className="absolute inset-0 bg-cover bg-center transition-transform duration-500 group-hover:scale-105"
                style={{ backgroundImage: `url(${event.img})` }}
              />

              {/* Overlay para melhorar a leitura do texto */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />

              <div className="absolute inset-0 p-8 flex flex-col justify-end">
                <h3 className="text-3xl font-extrabold text-white mb-2">
                  {event.name}
                </h3>
                <p className="text-sm text-white/90">{event.venue}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}