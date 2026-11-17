# Guia de Configuração - Imagens do Home

## Hero Card Stack Images

### Como adicionar suas imagens ao Hero Section

### Opção 1: Pasta Public (Recomendado)

1. Crie a pasta de imagens:
```
starsea-front/
└── public/
    └── images/
        ├── hero-card-1.jpg
        ├── hero-card-2.jpg
        └── hero-card-3.jpg
```

2. No arquivo `HeroSection.tsx`, as imagens já estão configuradas como:
```typescript
src: '/images/hero-card-1.jpg'
```

✅ Pronto! Basta adicionar as imagens na pasta `public/images/`

---

### Opção 2: Assets (Import)

1. Crie a pasta:
```
starsea-front/
└── src/
    └── assets/
        └── images/
            ├── hero-card-1.jpg
            ├── hero-card-2.jpg
            └── hero-card-3.jpg
```

2. No arquivo `HeroSection.tsx`, adicione os imports no topo:
```typescript
import card1 from '../../assets/images/hero-card-1.jpg';
import card2 from '../../assets/images/hero-card-2.jpg';
import card3 from '../../assets/images/hero-card-3.jpg';
```

3. Atualize o array `cardImages`:
```typescript
const cardImages: CardStackImage[] = [
  {
    src: card1,
    alt: 'Evento 1',
    color: 'from-blue-600 to-blue-800',
    rotation: 'rotate-[-8deg]',
    zIndex: 10
  },
  // ... resto
];
```

---

### Opção 3: URLs Externas

Basta substituir o `src` por uma URL completa:
```typescript
src: 'https://exemplo.com/imagem.jpg'
```

---

## Configuração Atual

O componente está configurado com 3 cards empilhados:

```typescript
const cardImages: CardStackImage[] = [
  {
    src: '/images/hero-card-1.jpg',      // Card 1 (atrás)
    alt: 'Evento 1',
    color: 'from-blue-600 to-blue-800',  // Gradiente fallback
    rotation: 'rotate-[-8deg]',          // Rotação -8°
    zIndex: 10
  },
  {
    src: '/images/hero-card-2.jpg',      // Card 2 (meio)
    alt: 'Evento 2',
    color: 'from-pink-500 to-purple-600',
    rotation: 'rotate-[-4deg]',          // Rotação -4°
    zIndex: 20
  },
  {
    src: '/images/hero-card-3.jpg',      // Card 3 (frente)
    alt: 'Evento 3',
    color: 'from-green-400 to-teal-500',
    rotation: 'rotate-[0deg]',           // Sem rotação
    zIndex: 30
  }
];
```

---

## Personalização

### Mudar quantidade de cards

Adicione ou remova itens do array `cardImages`:

```typescript
const cardImages: CardStackImage[] = [
  // Card 1
  { src: '/images/card1.jpg', alt: '...', color: '...', rotation: 'rotate-[-12deg]', zIndex: 10 },
  // Card 2
  { src: '/images/card2.jpg', alt: '...', color: '...', rotation: 'rotate-[-8deg]', zIndex: 20 },
  // Card 3
  { src: '/images/card3.jpg', alt: '...', color: '...', rotation: 'rotate-[-4deg]', zIndex: 30 },
  // Card 4 (novo)
  { src: '/images/card4.jpg', alt: '...', color: '...', rotation: 'rotate-[0deg]', zIndex: 40 },
];
```

### Mudar cores do gradiente fallback

Edite a propriedade `color` usando classes Tailwind:

```typescript
color: 'from-red-500 to-orange-600'
color: 'from-purple-700 to-pink-500'
color: 'from-teal-400 to-blue-600'
```

### Ajustar posicionamento

No JSX do componente, ajuste as classes de posição:

```typescript
className={`absolute ${
  index === 0 ? 'right-20 top-8' :     // Card 1
  index === 1 ? 'right-10 top-16' :    // Card 2
  'right-0 top-24'                     // Card 3
} ...`}
```

---

## Fallback Automático

✅ Se a imagem não carregar, o componente automaticamente mostra um gradiente colorido no lugar!

---

## Recomendações

📐 **Dimensões ideais:** 540x780px (proporção 2:3)
📦 **Formato:** JPG ou WebP (otimizado)
💾 **Tamanho:** < 200KB por imagem
🎨 **Conteúdo:** Fotos de eventos, artistas ou público

---

## Remover o texto sobreposto (opcional)

Se quiser apenas as imagens sem o texto "Descubra eventos", delete este bloco no final do Card Stack:

```typescript
{/* Texto no último card (opcional - pode remover se quiser só imagens) */}
<div className="absolute right-0 top-24 w-[180px] h-[260px] flex items-end p-5 pointer-events-none" style={{ zIndex: 40 }}>
  <div className="text-white bg-black/30 backdrop-blur-sm rounded-lg p-3">
    <p className="font-bold text-sm">Descubra eventos</p>
    <p className="text-xs opacity-90">na sua cidade</p>
  </div>
</div>
```
