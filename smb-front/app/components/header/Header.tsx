import React, { useState } from 'react';
import './Header.css';
import Logotype from '../logo/Logotype';
import {Link} from "react-router";

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
                    <Link className="nav-link" to={"/"}>Главная </Link>
                    <Link className="nav-link" to={"/analytics"}>Аналитика </Link>
                    <Link className="nav-link" to={"/companies"}>Компании </Link>
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