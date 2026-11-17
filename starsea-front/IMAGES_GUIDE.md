# 📸 Guia Completo - Todas as Imagens do Projeto

## 🎯 Estrutura Completa de Pastas

```
starsea-front/
└── public/
    └── images/
        ├── hero-card-1.jpg              (Hero Stack)
        ├── hero-card-2.jpg              (Hero Stack)
        ├── hero-card-3.jpg              (Hero Stack)
        ├── featured-doja-cat.jpg        (Featured Section)
        ├── featured-mcr.jpg             (Featured Section)
        ├── featured-kali.jpg            (Featured Section)
        ├── artists/
        │   ├── doja-cat.jpg             (Profile + PopGenre)
        │   ├── mcr.jpg                  (Profile)
        │   ├── kali-uchis.jpg           (Profile)
        │   ├── bad-bunny.jpg            (Profile)
        │   ├── rufus.jpg                (Profile)
        │   ├── ed-sheeran.jpg           (PopGenre)
        │   ├── oasis.jpg                (PopGenre)
        │   └── bbno.jpg                 (PopGenre)
        └── venues/
            ├── allianz-parque.jpg       (Venues)
            ├── espaco-unimed.jpg        (Venues)
            ├── audio.jpg                (Venues)
            ├── anhembi.jpg              (Venues)
            ├── interlagos.jpg           (Venues)
            └── morumbi.jpg              (Venues)
```

**Total: 21 imagens necessárias**

---

## 📋 Lista Completa de Imagens Por Componente

---

## 🚀 Setup Rápido

### 1. Crie a pasta de imagens:

```
starsea-front/
└── public/
    └── images/
```

### 2. Adicione 6 imagens:

**Hero Card Stack (3 imagens):**
- `hero-card-1.jpg` - Card de trás
- `hero-card-2.jpg` - Card do meio
- `hero-card-3.jpg` - Card da frente

**Featured Section (3 imagens):**
- `featured-doja-cat.jpg` - Evento 1
- `featured-mcr.jpg` - Evento 2
- `featured-kali.jpg` - Evento 3

### 3. Pronto! 🎉

Os componentes já estão configurados para usar essas imagens.

---

## 📐 Hero Section - Card Stack

### Estrutura Atual

```typescript
// src/components/home/HeroSection.tsx

const cardImages: CardStackImage[] = [
  {
    src: '/images/hero-card-1.jpg',      // Imagem do card
    alt: 'Evento 1',
    color: 'from-blue-600 to-blue-800',  // Gradiente fallback
    rotation: 'rotate-[-8deg]',          // Rotação
    zIndex: 10
  },
  {
    src: '/images/hero-card-2.jpg',
    alt: 'Evento 2',
    color: 'from-pink-500 to-purple-600',
    rotation: 'rotate-[-4deg]',
    zIndex: 20
  },
  {
    src: '/images/hero-card-3.jpg',
    alt: 'Evento 3',
    color: 'from-green-400 to-teal-500',
    rotation: 'rotate-[0deg]',
    zIndex: 30
  }
];
```

### Como personalizar:

**Usar URLs externas:**
```typescript
src: 'https://exemplo.com/imagem.jpg'
```

**Mudar cores do gradiente fallback:**
```typescript
color: 'from-red-500 to-orange-600'
color: 'from-purple-700 to-pink-500'
```

**Adicionar mais cards:**
```typescript
{
  src: '/images/hero-card-4.jpg',
  alt: 'Evento 4',
  color: 'from-teal-400 to-blue-600',
  rotation: 'rotate-[4deg]',
  zIndex: 40
}
```

### Recomendações de imagem:
- **Dimensões:** 540x780px (proporção 2:3)
- **Formato:** JPG ou WebP
- **Tamanho:** < 200KB
- **Conteúdo:** Fotos verticais de eventos, artistas ou público

---

## 🎯 Featured Section - Eventos em Destaque

### Estrutura Atual

```typescript
// src/components/home/FeaturedSection.tsx

const events: EventCard[] = [
  { 
    id: 1, 
    artist: "Doja Cat", 
    venue: "Sahal Music Hall - 05 fev", 
    matchPercentage: "Match 93%", 
    imageSrc: "/images/featured-doja-cat.jpg",     // IMAGEM
    gradientFallback: "from-pink-500 to-purple-600" // Fallback
  },
  { 
    id: 2, 
    artist: "My Chemical Romance", 
    venue: "Allianz Parque - 06 e 08 fev", 
    matchPercentage: "Match 87%", 
    imageSrc: "/images/featured-mcr.jpg",
    gradientFallback: "from-gray-700 to-gray-900"
  },
  { 
    id: 3, 
    artist: "Kali Uchis", 
    venue: "Vibra São Paulo - 08 fev", 
    matchPercentage: "Match 81%", 
    imageSrc: "/images/featured-kali.jpg",
    gradientFallback: "from-orange-400 to-purple-600"
  }
];
```

### Como personalizar:

**Adicionar mais eventos:**
```typescript
{ 
  id: 4, 
  artist: "Taylor Swift", 
  venue: "Morumbi - 15 mar", 
  matchPercentage: "Match 95%", 
  imageSrc: "/images/featured-taylor.jpg",
  gradientFallback: "from-blue-500 to-cyan-400"
}
```

**Mudar informações:**
```typescript
artist: "Nome do Artista"       // Título principal
venue: "Local - Data"            // Subtítulo
matchPercentage: "Match 88%"    // Badge no topo
```

**Usar URLs externas:**
```typescript
imageSrc: "https://exemplo.com/artista.jpg"
```

### Recomendações de imagem:
- **Dimensões:** 600x800px (proporção 3:4)
- **Formato:** JPG ou WebP
- **Tamanho:** < 300KB
- **Conteúdo:** Fotos dos artistas, pôsteres ou shows
- **Dica:** Use imagens com boa iluminação (tem overlay escuro no bottom)

---

## 📁 Estrutura de Pastas Completa

```
starsea-front/
└── public/
    └── images/
        ├── hero-card-1.jpg         ← Hero Stack
        ├── hero-card-2.jpg         ← Hero Stack
        ├── hero-card-3.jpg         ← Hero Stack
        ├── featured-doja-cat.jpg   ← Featured
        ├── featured-mcr.jpg        ← Featured
        └── featured-kali.jpg       ← Featured
```

---

## 🎨 Opções de Origem das Imagens

### ✅ Opção 1: Public (Recomendado)
- Coloque em `public/images/`
- Use caminho: `/images/nome.jpg`
- **Vantagem:** Mais simples, sem imports

### ✅ Opção 2: Assets com Import
1. Crie `src/assets/images/`
2. Adicione no topo do componente:
```typescript
import img1 from '../../assets/images/hero-card-1.jpg';
```
3. Use: `src: img1`

### ✅ Opção 3: URLs Externas
- Use URLs completas: `https://exemplo.com/img.jpg`
- **Vantagem:** Não aumenta o bundle

---

## 🛡️ Sistema de Fallback Automático

✅ Ambos os componentes têm fallback inteligente:

1. Tenta carregar a imagem
2. Se falhar → mostra gradiente colorido
3. Nenhum erro para o usuário!

**Você pode testar:** use um path inválido e verá o gradiente aparecer.

---

## 🎯 Resumo - 3 Passos

1. ✅ Crie `public/images/`
2. ✅ Adicione 6 imagens (3 hero + 3 featured)
3. ✅ **Pronto!** Sem código adicional

**Os componentes já estão 100% configurados!**

---

## 🔧 Personalização Avançada

### Remover texto sobreposto do Hero

No `HeroSection.tsx`, delete este bloco:

```typescript
{/* Texto no último card */}
<div className="absolute right-0 top-24 ...">
  <div className="text-white ...">
    <p>Descubra eventos</p>
    <p>na sua cidade</p>
  </div>
</div>
```

### Mudar quantidade de cards no grid

Em `FeaturedSection.tsx`, mude:
```typescript
className="grid grid-cols-1 md:grid-cols-3 gap-6"
```

Para:
```typescript
className="grid grid-cols-1 md:grid-cols-4 gap-6"  // 4 colunas
className="grid grid-cols-1 md:grid-cols-2 gap-6"  // 2 colunas
```

---

## 📞 Precisa de Ajuda?

- **Hero Section:** `src/components/home/HeroSection.tsx`
- **Featured Section:** `src/components/home/FeaturedSection.tsx`
- **Este guia:** `starsea-front/IMAGES_GUIDE.md`

🎉 **Boas imagens para o seu projeto!**
