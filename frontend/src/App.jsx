import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import SearchPage from './pages/SearchPage';
import BuyerDetailPage from './pages/BuyerDetailPage';
import DemoArchetypesPage from './pages/DemoArchetypesPage';
import { getDemoArchetypes, resetDemoData } from './services/api';
import { Check } from 'lucide-react';

export default function App() {
  const [currentView, setCurrentView] = useState('landing');
  const [selectedBuyerId, setSelectedBuyerId] = useState(null);
  const [demoBuyers, setDemoBuyers] = useState([]);
  const [toastMessage, setToastMessage] = useState(null);

  useEffect(() => {
    loadArchetypes();
  }, []);

  async function loadArchetypes() {
    try {
      const data = await getDemoArchetypes();
      setDemoBuyers(data);
    } catch (err) {
      console.error("Failed to load demo archetypes:", err);
    }
  }

  const handleSelectBuyer = (buyerId) => {
    setSelectedBuyerId(buyerId);
    setCurrentView('buyer-detail');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleResetDemo = async () => {
    try {
      await resetDemoData();
      await loadArchetypes();
      setToastMessage('Benchmark dataset successfully reseeded.');
      setTimeout(() => setToastMessage(null), 3000);
      if (currentView === 'buyer-detail') {
        setCurrentView('landing');
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-[#07090D] text-[#F4F3EF] flex flex-col font-sans selection:bg-[#6757D9]/25 selection:text-[#F4F3EF]">
      
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-[#0D1118] border border-[#202734] text-[#55C89A] px-4 py-2.5 rounded-lg shadow-2xl text-xs font-mono flex items-center gap-2 animate-fadeIn">
          <Check className="w-3.5 h-3.5 text-[#55C89A]" />
          {toastMessage}
        </div>
      )}

      {/* Top Navbar */}
      <Navbar
        currentView={currentView}
        setCurrentView={setCurrentView}
        demoBuyers={demoBuyers}
        onSelectBuyer={handleSelectBuyer}
        onResetDemo={handleResetDemo}
      />

      {/* Main Content Area */}
      <main className="flex-1">
        {currentView === 'landing' && (
          <LandingPage
            onSelectBuyer={handleSelectBuyer}
            onNavigateSearch={() => setCurrentView('search')}
            onNavigateDemo={() => setCurrentView('demo-archetypes')}
            demoBuyers={demoBuyers}
          />
        )}

        {currentView === 'search' && (
          <SearchPage onSelectBuyer={handleSelectBuyer} />
        )}

        {currentView === 'buyer-detail' && (
          <BuyerDetailPage
            buyerId={selectedBuyerId}
            onBack={() => setCurrentView('landing')}
            onSelectBuyer={handleSelectBuyer}
          />
        )}

        {currentView === 'demo-archetypes' && (
          <DemoArchetypesPage
            demoBuyers={demoBuyers}
            onSelectBuyer={handleSelectBuyer}
          />
        )}
      </main>

      {/* Editorial Footer */}
      <footer className="border-t border-[#202734] bg-[#07090D] py-12 px-6 text-center text-xs text-[#5F6877] space-y-3">
        <div className="flex items-center justify-center gap-2 text-xs font-mono text-[#8F98A8]">
          <span className="w-1.5 h-1.5 rounded-sm bg-signature-gradient"></span>
          <span>CrediShield Intelligence — PS-09-S2</span>
        </div>
        <p className="max-w-md mx-auto text-[11px] text-[#5F6877] font-light leading-relaxed">
          Evidence-grounded buyer identity resolution, MSME payment dispute tracking, 
          MCA21 statutory extraction, and commercial terms calibration.
        </p>
        <p className="text-[10px] text-[#5F6877]/80 font-mono">
          Curated benchmark evaluation mode • All rights reserved
        </p>
      </footer>

    </div>
  );
}
