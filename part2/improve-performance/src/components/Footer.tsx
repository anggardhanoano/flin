import React, { useMemo } from "react";

const Footer = () => {
  const calculateFooterStuff = () => {
    let result = 0;
    for (let i = 0; i < 1000000; i++) {
      result += (Math.sqrt(i) * Math.tan(i)) / Math.log(i + 1);
    }
    return result;
  };

  const calculatedValue = useMemo(() => {
    return calculateFooterStuff();
  }, []);

  return (
    <footer className="main-footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>About Us</h3>
          <p>Part of the Flin Assignment (Part 2)</p>
          <p>Calculated value: {calculatedValue?.toFixed(2)}</p>
        </div>

        <div className="footer-section">
          <h3>Links</h3>
          <ul>
            {Array.from({ length: 20 }, (_, i) => (
              <li key={i}>
                <a href={`#footer-link-${i}`}>Footer Link {i}</a>
              </li>
            ))}
          </ul>
        </div>

        <div className="footer-section">
          <h3>Contact</h3>
          <p>Email: example@flin.co</p>
          <p>Phone: 123-456-7890</p>
        </div>
      </div>

      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} Flin Part 2</p>
      </div>
    </footer>
  );
};

export default Footer;
