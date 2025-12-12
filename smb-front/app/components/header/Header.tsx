import React, { useState } from 'react';
import './Header.css';
import Logotype from '../logo/Logotype';

interface HeaderProps {
    onMenuToggle?: () => void;
}

const Header: React.FC<HeaderProps> = ({  }) => {
    const [isGuideMenuOpen, setIsGuideMenuOpen] = useState(false);
    const handleMenuToggle = () => {
        setIsGuideMenuOpen(!isGuideMenuOpen);
    };

    return (
        <header className="header">
            <div className="header-container">
                <Logotype />

                <button
                    className="menu-toggle"
                    onClick={handleMenuToggle}
                    aria-label="Меню"
                >
                    {isGuideMenuOpen ? '✕' : '☰'}
                </button>

                <nav className={`nav ${isGuideMenuOpen ? 'nav-open' : ''}`}>
                    <a href="#" className="nav-link active">Главная</a>
                    <a href="#analytics" className="nav-link">Аналитика</a>
                    <a href="#companies" className="nav-link">Компании</a>
                </nav>

            </div>

            <div className="status-bar">
                <div className="status-container">
                    <div className="status-item">
                        <span className="status-dot online"></span>
                        Система активна
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;