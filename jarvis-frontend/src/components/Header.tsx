import React from 'react';
import { FaRobot } from 'react-icons/fa';
import './Header.css';

const Header = () => (
  <header className="jarvis-header">
    <FaRobot size={32} />
    <h1>JARVIS Dashboard</h1>
  </header>
);

export default Header;