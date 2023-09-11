import { useState } from "react";
import reactLogo from "./assets/react.svg";
import "./App.css";
import ListGroup from "./components/ListGroup";
import Alert from "./components/Alert";
import Button from "./components/Button";
import Navbar from "./components/Navbar";

function App() {
    const [showAlert, setShowAlert] = useState(false);

    return (
        <div>
            <Navbar apiURL="http://localhost:8000" />
        </div>
    );
}

export default App;
