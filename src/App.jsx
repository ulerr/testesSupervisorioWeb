import { useState } from "react";
import supernovaLogo from "./assets/supernova.png";
import { invoke } from "@tauri-apps/api/core";
import "./App.css";

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");

  async function greet() {
    // Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
    setGreetMsg(await invoke("greet", { name }));
  }

  return (
    <main className="container">
      <h1>Teste pré-Alfa do supervisório web</h1>
      <div className="row">
        <a href="https://www.instagram.com/supernova.ufjf/" target="_blank">
          <img src={supernovaLogo} className="logo supernova" alt="Supernova logo" />
        </a>
      </div>
      <p>Clique no ícone da Supernova para acessar nosso Instagram.</p>

      <form
        className="row"
        onSubmit={(e) => {
          e.preventDefault();
          greet();
        }}
      >
        <input
          id="greet-input"
          onChange={(e) => setName(e.currentTarget.value)}
          placeholder="Enter a name..."
        />
        <button type="submit">Greet</button>
      </form>
      <p>{greetMsg}</p>
    </main>
  );
}

export default App;
