import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./styles/global.css";

import * as _ from "lodash";
import * as moment from "moment";
import "bootstrap/dist/css/bootstrap.min.css";
import "antd/dist/reset.css";
import { Chart } from "chart.js/auto";

(window as any)._ = _;
(window as any).moment = moment;
(window as any).Chart = Chart;

setTimeout(() => {
  ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}, 1000);
