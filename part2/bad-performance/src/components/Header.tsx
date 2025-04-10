import React from "react";

const Header = () => {
  return (
    <header className="main-header">
      <div className="logo">
        <h1>FLin</h1>
      </div>

      <nav className={`main-nav open`}>
        <ul>
          {Array.from({ length: 10 }, (_, i) => (
            <li key={i}>
              <a href={`#section-${i}`}>Nav {i}</a>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
};

export default Header;
