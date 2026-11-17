import { useState } from "react";
import { Link } from "react-router-dom";

type TicketType = 'pista' | 'premium';

interface Ticket {
  name: string;
  price: number;
}

export default function EventDetailPage() {
  const [quantity, setQuantity] = useState<number>(2);
  const [selectedTicket, setSelectedTicket] = useState<TicketType>("pista");

  const tickets: Record<TicketType, Ticket> = {
    pista: { name: "Pista", price: 180 },
    premium: { name: "Pista Premium", price: 320 }
  };

  const total: number = tickets[selectedTicket].price * quantity;

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-[#1a1a1a] text-white py-4 px-8 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3">
          <img
            src="/sea-logo.png"
            alt="Logo"
            className="h-24 w-auto max-w-[340px] object-contain sm:h-28 sm:max-w-[400px] lg:h-32 lg:max-w-[450px]"
          />
        </Link>

        <nav className="flex items-center gap-8">
          <Link to="/events" className="text-gray-300 hover:text-white">Eventos</Link>
          <Link to="/genres" className="text-gray-300 hover:text-white">Gêneros</Link>
          <Link to="/locais" className="text-gray-300 hover:text-white">Locais</Link>
          <Link to="/tickets" className="text-cyan-400 hover:text-cyan-300">Ingressos</Link>
          <Link to="/profile" className="text-gray-300 hover:text-white">Perfil</Link>
          <Link to="/login" className="text-gray-300 hover:text-white">Entrar</Link>
          <Link to="/signup" className="px-4 py-2 bg-gradient-to-r from-purple-500 to-cyan-400 rounded-lg font-bold hover:opacity-90">
            CADASTRE-SE
          </Link>
        </nav>
      </header>

      <div className="bg-gradient-to-r from-pink-500 via-purple-500 to-purple-700 py-16 px-8">
        <div className="max-w-7xl mx-auto">
          <p className="text-white/80 mb-2">Eventos / São Paulo / Doja Cat</p>
          
          <div className="flex items-center gap-4 mb-4">
            <span className="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-white font-bold">
              Pop
            </span>
          </div>

          <h1 className="text-6xl font-bold text-white mb-8">Doja Cat</h1>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-8 py-8 grid grid-cols-3 gap-8">
        <div className="col-span-2 space-y-6">
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-white rounded-lg p-4 flex items-start gap-3">
              <span className="text-2xl">📅</span>
              <div>
                <p className="text-gray-500 text-xs">DATA</p>
                <p className="font-bold">05 de fevereiro</p>
              </div>
            </div>

            <div className="bg-white rounded-lg p-4 flex items-start gap-3">
              <span className="text-2xl">⏰</span>
              <div>
                <p className="text-gray-500 text-xs">HORÁRIO</p>
                <p className="font-bold">Abertura 19h - Show 23h</p>
              </div>
            </div>

            <div className="bg-white rounded-lg p-4 flex items-start gap-3">
              <span className="text-2xl">📍</span>
              <div>
                <p className="text-gray-500 text-xs">LOCAL</p>
                <p className="font-bold">Sahal Music Hall</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4">Sobre o show</h2>
            <p className="text-gray-600">
              Doja Cat no Sahal Music Hall, em São Paulo. Abertura às 19h e início do show às 23h.
            </p>
          </div>

          {/* Como chegar */}
          <div className="bg-white rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4">Como chegar</h2>
            
            {/* Mapa visual */}
            <div className="bg-gray-200 rounded-lg h-48 mb-4 relative overflow-hidden">
              <svg className="absolute inset-0 w-full h-full" viewBox="0 0 400 200">
                <path
                  d="M 50 180 Q 150 100, 350 80"
                  fill="none"
                  stroke="#8b5cf6"
                  strokeWidth="3"
                  strokeDasharray="8 8"
                />
                <circle cx="50" cy="180" r="8" fill="#1a1a1a" />
                <circle cx="350" cy="80" r="12" fill="#8b5cf6" />
              </svg>
              <div className="absolute bottom-4 right-4 bg-white px-3 py-1 rounded-lg font-bold">
                Sahal Music Hall
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div className="border border-gray-300 rounded-lg p-4">
                <span className="text-2xl mb-2 block">🚗</span>
                <p className="font-bold mb-1">De carro</p>
                <p className="text-sm text-gray-600">12 min - 4.2 km</p>
                <p className="text-xs text-gray-500">Estacionamento próximo</p>
              </div>

              <div className="border border-gray-300 rounded-lg p-4">
                <span className="text-2xl mb-2 block">🚌</span>
                <p className="font-bold mb-1">Transporte público</p>
                <p className="text-sm text-gray-600">32 min - ver rotas</p>
              </div>

              <div className="border border-gray-300 rounded-lg p-4">
                <span className="text-2xl mb-2 block">🚶</span>
                <p className="font-bold mb-1">A pé</p>
                <p className="text-sm text-gray-600">0 usando para quem mora</p>
                <p className="text-xs text-gray-500">perto</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg p-6 h-fit sticky top-8">
          <h2 className="text-2xl font-bold mb-6">Ingressos</h2>

          <div className="space-y-3 mb-6">
            <button
              onClick={() => setSelectedTicket("pista")}
              className={`w-full text-left p-4 rounded-lg border-2 transition ${
                selectedTicket === "pista"
                  ? "border-purple-500 bg-purple-50"
                  : "border-gray-300 hover:border-purple-300"
              }`}
            >
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-bold">Pista</p>
                  <p className="text-sm text-gray-500">Inteira geral</p>
                </div>
                <p className="text-xl font-bold">R$ 180</p>
              </div>
            </button>

            <button
              onClick={() => setSelectedTicket("premium")}
              className={`w-full text-left p-4 rounded-lg border-2 transition ${
                selectedTicket === "premium"
                  ? "border-purple-500 bg-purple-50"
                  : "border-gray-300 hover:border-purple-300"
              }`}
            >
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-bold">Pista Premium</p>
                  <p className="text-sm text-gray-500">Pista elevada</p>
                </div>
                <p className="text-xl font-bold">R$ 320</p>
              </div>
            </button>
          </div>

          <div className="p-4 bg-gray-100 rounded-lg mb-6">
            <div className="flex justify-between items-center">
              <div>
                <p className="font-bold text-gray-400">Camarote</p>
                <p className="text-sm text-gray-400">Entre em contato</p>
              </div>
              <p className="text-gray-400">A consultar</p>
            </div>
          </div>

          <div className="mb-6">
            <p className="font-bold mb-3">Quantidade</p>
            <div className="flex items-center justify-center gap-4">
              <button
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                className="w-10 h-10 rounded-full border-2 border-gray-300 flex items-center justify-center hover:border-purple-500"
              >
                −
              </button>
              <span className="text-2xl font-bold w-8 text-center">{quantity}</span>
              <button
                onClick={() => setQuantity(quantity + 1)}
                className="w-10 h-10 rounded-full border-2 border-gray-300 flex items-center justify-center hover:border-purple-500"
              >
                +
              </button>
            </div>
          </div>

          <div className="border-t border-gray-300 pt-4 mb-6">
            <div className="flex justify-between items-center mb-2">
              <p className="text-gray-600">Total</p>
              <p className="text-3xl font-bold">R$ {total}</p>
            </div>
          </div>

          <button className="w-full py-4 bg-gradient-to-r from-purple-500 to-cyan-400 text-white font-bold rounded-lg hover:opacity-90 transition mb-3">
            COMPRAR INGRESSO
          </button>

          <div className="text-center space-x-4 text-sm text-gray-500">
            <a href="#" className="hover:text-gray-700">Compra segura</a>
            <span>•</span>
            <a href="#" className="hover:text-gray-700">Meia e isenções</a>
          </div>
        </div>
      </div>
    </div>
  );
}
