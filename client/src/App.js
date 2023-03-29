import logo from "./logo.svg";
import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import DisplayAll from "./components/DisplayAll";
import AuthorForm from "./components/AuthorForm";
import EditAuthor from "./components/EditAuthor";

function App() {
  return (
    <div className="App">
      <h1>Welcome to the Book Club</h1>
      <h3>Share some of your favorite authors with friends, family and the world!</h3>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<DisplayAll />} />
          <Route path="/new" element={<AuthorForm />} />
          <Route path="/edit/:id" element={<EditAuthor />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;