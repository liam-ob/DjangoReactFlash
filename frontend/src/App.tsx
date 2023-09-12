import { useState } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import LoginForm from "./components/LoginForm";
import FlashcardStackList from "./components/FlashcardStackList";

function App() {
    const [showAlert, setShowAlert] = useState(false);

    return (
        <div>
            <Navbar apiURL="http://localhost:8000/" />
            <FlashcardStackList apiURL="http://localhost:8000/" />
        </div>
    );
}

export default App;
