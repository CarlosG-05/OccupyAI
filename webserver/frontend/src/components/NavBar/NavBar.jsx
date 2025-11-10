import React from 'react';
import logo from '../../assets/logo.png';
import './NavBar.css';

function NavBar({ buttons }) {
  return (
    <nav className="navbar navbar-vertical">
      <div className="navbar-logo-container">
        <img src={logo} alt="Logo" className="navbar-logo" />
      </div>
      <div className="navbar-buttons navbar-buttons-vertical">
        {buttons.map((btn, idx) => (
          <button
            key={idx}
            className="navbar-button"
            onClick={() => window.location.href = btn.href}
          >
            {btn.label}
          </button>
        ))}
      </div>
    </nav>
  );
}

export default NavBar;
