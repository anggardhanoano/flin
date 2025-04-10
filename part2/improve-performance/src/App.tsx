import React from "react";

import { DatePicker, Button } from "antd";
import Header from "./components/Header";
import Footer from "./components/Footer";
import ImageGallery from "./components/ImageGallery";
import HeavyData from "./components/HeavyData";

function App() {
  return (
    <div className="app">
      <Header />
      <main>
        <h1>FLin Part 2</h1>
        <div className="controls">
          <Button color="primary">Click Me</Button>
          <DatePicker />
        </div>

        <ImageGallery />
        <HeavyData />
      </main>
      <Footer />
    </div>
  );
}

export default App;
