import { Navbar } from "../components/home/Navbar";
import { HeroSection } from "../components/home/HeroSection";
import { FeaturedSection } from "../components/home/FeaturedSection";
import { PopGenreSection } from "../components/home/PopGenreSection";
import { ConnectSection } from "../components/home/ConnectSection";
import { FeaturedEventsSection } from "../components/home/FeaturedEventsSection";
import { NearbyVenuesSection } from "../components/home/NearbyVenuesSection";
import { QuestionsSection } from "../components/home/QuestionsSection";

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      <HeroSection />
      <FeaturedSection />
      <PopGenreSection />
      <ConnectSection />
      <FeaturedEventsSection />
      <NearbyVenuesSection />
      <QuestionsSection />
    </div>
  );
}
