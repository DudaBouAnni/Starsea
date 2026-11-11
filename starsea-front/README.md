# Meu Projeto

Projeto React + Vite com Twind (Tailwind-in-JS) e TypeScript

## Estrutura de Pastas

```
src/
├── pages/          # Páginas da aplicação
├── components/     # Componentes reutilizáveis
├── utils/          # Funções utilitárias e configuração Twind
├── styles/         # Estilos globais/temas customizados
└── assets/         # Imagens e arquivos estáticos
```

## Comandos

```bash
npm run dev      # Iniciar servidor de desenvolvimento
npm run build    # Build de produção
npm run preview  # Preview do build
```

## Tecnologias

- ⚛️ React 19
- ⚡ Vite 8
- 🎨 Twind (Tailwind-in-JS)
- 📘 TypeScript

## Twind

Este projeto usa Twind para estilização - escreva classes Tailwind diretamente no JSX/TSX usando a função `tw`.

Exemplo:
```tsx
import { tw } from '@twind/core'

<div className={tw`bg-blue-500 text-white p-4`}>
  Conteúdo
</div>
```

## Começando

Execute `npm run dev` para iniciar o servidor de desenvolvimento e comece a editar `src/pages/Home.tsx`.

## Começando

Execute `npm run dev` para iniciar o servidor de desenvolvimento e comece a editar `src/pages/Home.jsx`.
