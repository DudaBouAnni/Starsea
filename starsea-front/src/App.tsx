import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Landing } from './pages/Landing';
import LoginPage from './pages/LoginPage.tsx';
import SignupPage from './pages/SignupPage.tsx';
import OnboardingMusicPage from './pages/OnboardingMusicPage.tsx';
import EventDetailPage from './pages/EventDetailPage.tsx';
import ProfilePage from './pages/ProfilePage.tsx';
import MyTicketsPage from './pages/MyTicketsPage.tsx';
import EventsPage from './pages/EventsPage.tsx';
import GenresPage from './pages/GenresPage.tsx';
import LocationsPage from './pages/LocationsPage.tsx';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/onboarding/connect-music" element={<OnboardingMusicPage />} />
          <Route path="/events" element={<EventsPage />} />
          <Route path="/genres" element={<GenresPage />} />
          <Route path="/locais" element={<LocationsPage />} />
          <Route path="/event/:id" element={<EventDetailPage />} />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/tickets"
            element={
              <ProtectedRoute>
                <MyTicketsPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
