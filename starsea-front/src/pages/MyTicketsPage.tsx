import { useState } from "react";
import { Link } from "react-router-dom";
import { Header } from "../components/Header";

type FilterType = 'proximos' | 'passados';

interface Ticket {
  id: number;
  event: string;
  venue: string;
  date: string;
  time: string;
  section: string;
  quantity: number;
  color: string;
  isPast: boolean;
}

export default function MyTicketsPage() {
  const [filter, setFilter] = useState<FilterType>("proximos");

  const tickets: Ticket[] = [
    {
      id: 1,
      event: "Doja Cat",
      venue: "Sahal Music Hall",
      date: "05 fev",
      time: "21h",
      section: "Pista",
      quantity: 2,
      color: "from-pink-500 to-purple-600",
      isPast: false
    },
    {
      id: 2,
      event: "Oasis",
      venue: "Estádio Alvalade",
      date: "22 nov",
      time: "19h",
      section: "Pistas Premium",
      quantity: 2,
      color: "from-blue-600 to-blue-800",
      isPast: false
    }
  ];

  const filteredTickets = tickets.filter(t =>
    filter === "proximos" ? !t.isPast : t.isPast
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <Header currentPage="tickets" />

      <div className="max-w-6xl mx-auto px-8 py-12">
        <h1 className="text-4xl font-bold mb-8">Meus ingressos</h1>

        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setFilter("proximos")}
            className={`px-6 py-2 rounded-full font-medium transition ${
              filter === "proximos"
                ? "bg-gradient-to-r from-purple-500 to-cyan-400 text-white"
                : "bg-white text-gray-700 hover:bg-gray-100"
            }`}
          >
            Próximos (2)
          </button>
          <button
            onClick={() => setFilter("passados")}
            className={`px-6 py-2 rounded-full font-medium transition ${
              filter === "passados"
                ? "bg-gradient-to-r from-purple-500 to-cyan-400 text-white"
                : "bg-white text-gray-700 hover:bg-gray-100"
            }`}
          >
            Passados (0)
          </button>
        </div>

        <div className="space-y-6">
          {filteredTickets.map((ticket) => (
            <div key={ticket.id} className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md transition">
              <div className="flex">
                <div className={`w-48 bg-gradient-to-br ${ticket.color} p-6 flex flex-col justify-between text-white`}>
                  <div>
                    <h3 className="text-2xl font-bold mb-1">{ticket.event}</h3>
                    <p className="text-white/80 text-sm">{ticket.venue}</p>
                  </div>
                </div>

                <div className="flex-1 p-6 flex items-center justify-between">
                  <div className="grid grid-cols-3 gap-12">
                    <div>
                      <p className="text-xs text-gray-500 mb-1">DATA</p>
                      <p className="font-bold text-lg">{ticket.date}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">SETOR</p>
                      <p className="font-bold text-lg">{ticket.section}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">QTD</p>
                      <p className="font-bold text-lg">{ticket.quantity}</p>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    {[...Array(ticket.quantity)].map((_, i) => (
                      <div key={i} className="w-20 h-20 bg-gray-200 rounded-lg flex items-center justify-center">
                        <div className="w-16 h-16 bg-black/10 rounded"></div>
                      </div>
                    ))}
                    <p className="text-xs text-gray-400 ml-2 flex items-center">
                      Aproxime da entrada
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}

          {filteredTickets.length === 0 && (
            <div className="text-center py-16">
              <p className="text-gray-400 text-lg">Nenhum ingresso {filter === "proximos" ? "próximo" : "passado"}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
