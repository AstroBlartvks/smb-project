import type { Route } from "./+types/home";
import Header from '~/components/header/Header';

import './home.css'
import React from "react";
import MainContent from "~/components/homeComponent/mainContent/mainContent";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Анализатор МСБ" },
    { name: "description", content: "Анализатор МСБ!" },
  ];
}

export default function Home() {

    return (
        <div className="home-page">
            <Header />

            <main className="main-content">
                <MainContent/>
            </main>

            <footer className="footer">
                <div className="footer-content">
                    <p>Система прогнозирования банкротств МСБ © 2025</p>
                    <p>Для коммерческого использования обратитесь к Astro</p>
                </div>
            </footer>
        </div>
    );
}
