import React, { useState, useEffect } from "react";
import { Button } from "@mui/material";
import { DatePicker } from "antd";
import Header from "./components/Header";
import Footer from "./components/Footer";
import ImageGallery from "./components/ImageGallery";

const heavyData = Array.from({ length: 100000 }, (_, i) => ({
  id: i,
  name: `Item ${i}`,
  value: Math.random() * 1000,
  description: `This is a long description for item ${i}`,
}));

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState<any[]>([]);

  // Simulate heavy computation on every render
  const result = heavyData
    .filter((item) => item.value > 500)
    .map((item) => ({
      ...item,
      calculated: item.value * Math.random() * 10,
    }));

  useEffect(() => {
    // Simulate data fetching
    const timeout = setTimeout(() => {
      setData(result);
      setIsLoading(false);
    }, 1000);
    return () => clearTimeout(timeout);
  }, []);

  return (
    <div className="app">
      <Header />
      <main>
        <h1>FLin Part 2</h1>
        <div className="controls">
          <Button variant="contained" color="primary">
            Click Me
          </Button>
          <DatePicker />
        </div>

        <ImageGallery />

        <div className="heavy-content">
          {data.length > 0 && (
            <div>
              <h2>A Lot of Data</h2>
              <div className="data-grid">
                {data.map((item) => (
                  <div key={item.id} className="data-item">
                    <h3>{item.name}</h3>
                    <p>{item.description}</p>
                    <span>{item.calculated.toFixed(2)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;
