import { Link } from 'react-router-dom';

export function QuestionsSection() {
  return (
    <section className="bg-gradient-to-r from-purple-500 via-blue-400 to-cyan-400 py-16 px-12">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start gap-12">
        <div className="text-black max-w-md">
          <h2 className="text-4xl font-bold mb-6">Dúvidas ou comentários?</h2>
          <div className="space-y-2 text-sm">
            <p className="font-medium">starsea@gmail.com</p>
            <p>Avenida Vida Nova, 166, Bairro Maria Rosa</p>
            <p>(12) 3456-7890</p>
          </div>
        </div>
        
        <div className="flex gap-16">
          <div className="space-y-3 text-black">
            <Link to="#" className="block hover:underline font-medium">Sobre</Link>
            <Link to="#" className="block hover:underline font-medium">Shows</Link>
            <Link to="#" className="block hover:underline font-medium">Locais</Link>
          </div>
          <div className="space-y-3 text-black">
            <Link to="#" className="block hover:underline font-medium">Ajuda</Link>
          </div>
        </div>
      </div>
    </section>
  );
}
