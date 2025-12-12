import React from "react";

export default function Logotype() {
    return (
        <div className="logo">
            <div className="logo-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
                    <path d="M3 13H11V3H3V13ZM3 21H11V15H3V21ZM13 21H21V11H13V21ZM13 3V9H21V3H13Z" fill="white"/>
                </svg>
            </div>
            <div className="logo-text">
                <h1>БанкротствоAI</h1>
                <p>Прогнозирование рисков</p>
            </div>
        </div>
    );
}
