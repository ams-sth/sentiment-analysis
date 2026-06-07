import { BrowserRouter, Route, Routes } from "react-router-dom";
import CsvResult from "./pages/CsvResult";
import Home from "./pages/Home";
import TextResult from "./pages/TextResult";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/result" element={<TextResult />} />
        <Route path="/result/csv" element={<CsvResult />} />
      </Routes>
    </BrowserRouter>
  );
}
