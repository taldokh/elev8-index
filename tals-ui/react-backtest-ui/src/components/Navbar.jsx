import { useState } from 'react';
import { NavLink } from 'react-router-dom';

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="nav-logo">Elev8</div>

      <div className="nav-wrapper">
        <div className="nav-container">
          <button
            className="nav-toggle"
            onClick={() => setIsOpen(!isOpen)}
            aria-label="Toggle menu"
          >
            <span className="hamburger"></span>
            <span className="hamburger"></span>
            <span className="hamburger"></span>
          </button>

          <ul className={`nav-links ${isOpen ? 'nav-active' : ''}`}>
            <li>
              <NavLink to="/" end className="nav-link" onClick={() => setIsOpen(false)}>
                Home
              </NavLink>
            </li>
            <li>
              <NavLink to="/about" className="nav-link" onClick={() => setIsOpen(false)}>
                About
              </NavLink>
            </li>
            <li>
              <NavLink to="/portfolio" className="nav-link" onClick={() => setIsOpen(false)}>
                Portfolio
              </NavLink>
            </li>
            <li>
              <NavLink to="/contact" className="nav-link" onClick={() => setIsOpen(false)}>
                Contact
              </NavLink>
            </li>
          </ul>
        </div>
      </div>

      <style>{`
        .navbar {
          width: 100vw;
          background-color: #0d1b2a;
          color: #e0e0e0;
          padding: 0 20px;
          box-shadow: 0 2px 6px rgba(0,0,0,0.3);
          position: sticky;
          top: 0;
          z-index: 1000;

          display: flex;
          align-items: center;
          height: 60px;
          justify-content: space-between;
        }

        .nav-logo {
          font-size: 1.8rem;
          font-weight: 700;
          letter-spacing: 2px;
          color: #00bfff;
          user-select: none;
          display: flex;
          align-items: center;
        }

        .nav-wrapper {
          flex-grow: 1;
          display: flex;
          justify-content: flex-end;
          max-width: 1200px;
          margin-left: 20px; /* spacing between logo and nav */
        }

        .nav-container {
          display: flex;
          align-items: center;
          justify-content: flex-end;
        }

        /* Links */
        .nav-links {
          display: flex;
          list-style: none;
          margin: 0;
          padding: 0;
        }

        .nav-links li {
          margin-left: 25px;
        }

        .nav-link {
          color: #cbd5e1;
          text-decoration: none;
          font-weight: 600;
          font-size: 1rem;
          padding: 8px 0;
          position: relative;
          transition: color 0.3s ease;
        }

        .nav-link:hover,
        .nav-link.active {
          color: #00bfff;
        }

        .nav-link.active::after,
        .nav-link:hover::after {
          content: '';
          position: absolute;
          left: 0;
          bottom: -6px;
          width: 100%;
          height: 2px;
          background-color: #00bfff;
          border-radius: 2px;
        }

        /* Hamburger Menu */
        .nav-toggle {
          display: none;
          flex-direction: column;
          justify-content: space-between;
          width: 25px;
          height: 18px;
          background: transparent;
          border: none;
          cursor: pointer;
          padding: 0;
          margin-left: 20px;
        }

        .hamburger {
          width: 100%;
          height: 3px;
          background-color: #00bfff;
          border-radius: 2px;
        }

        /* Responsive */
        @media (max-width: 768px) {
          .nav-toggle {
            display: flex;
          }

          .nav-links {
            position: fixed;
            right: 0;
            top: 60px;
            height: calc(100% - 60px);
            width: 200px;
            background-color: #112240;
            flex-direction: column;
            align-items: flex-start;
            padding: 20px;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            z-index: 999;
          }

          .nav-links.nav-active {
            transform: translateX(0);
            box-shadow: -2px 0 8px rgba(0,0,0,0.5);
          }

          .nav-links li {
            margin: 15px 0;
            width: 100%;
          }

          .nav-link {
            width: 100%;
            font-size: 1.2rem;
          }
        }
      `}</style>
    </nav>
  );
}

export default Navbar;
