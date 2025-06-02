import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import AboutPage from './components/AboutPage';
import HomePage from './components/HomePage';  // import the new HomePage
import ContactPage from './components/ContactPage';

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/contact" element={<ContactPage />} />
      </Routes>
    </>
  );
}

export default App;
