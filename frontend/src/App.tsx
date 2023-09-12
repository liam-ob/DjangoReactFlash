import { useState } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import LoginForm from "./components/LoginForm";

function App() {
    const [showAlert, setShowAlert] = useState(false);

    return (
        <div>
            <Navbar apiURL="http://localhost:8000" />
            <LoginForm />
        </div>
    );
}

export default App;
