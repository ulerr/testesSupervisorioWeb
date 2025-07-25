import { useState } from "react";
import reactLogo from "./assets/react.svg";
import supernovaLogo from "./assets/supernova.png";
import { invoke } from "@tauri-apps/api/core";
import { pyInvoke } from "tauri-plugin-pytauri-api";
import "./App.css";

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");

  async function greet() {
    try {
      // Call the Rust greet function
      const rsGreeting = await invoke("greet", { name });
      
      // Call the Python greet function
      const pyGreeting = await pyInvoke("greet", { name });
      
      // Combine both greetings
      setGreetMsg(rsGreeting + "\n" + pyGreeting.message);
    } catch (error) {
      console.error("Error calling greet:", error);
      setGreetMsg("Error: " + error.message);
    }
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
