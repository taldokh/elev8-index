import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import OverviewPage from './components/OverviewPage';
import HomePage from './components/HomePage';  // import the new HomePage
import ContactPage from './components/ContactPage';

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/overview" element={<OverviewPage />} />
        <Route path="/contact" element={<ContactPage />} />
      </Routes>
    </>
  );
}

export default App;
