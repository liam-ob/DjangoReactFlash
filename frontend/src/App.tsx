import { useState, useRef } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import FlashcardStackList from "./components/FlashcardStackList";
import StackModal from "./components/StackModal";
import axios from "axios";

function App() {
    var baseURL = "";
    if (window.location.origin === "http://localhost:3000") {
        baseURL = "http://127.0.0.1:8000";
    } else {
        baseURL = window.location.origin;
    }

    const axiosInstance = axios.create({
        baseURL: baseURL,
        headers: {
            Authorization: `Token ${localStorage.getItem("token")}`,
        },
    });
    const [stackID, setStackID] = useState<number>(0);

    return (
        <div>
            <Navbar axiosInstance={axiosInstance} />
            <FlashcardStackList axiosInstance={axiosInstance} />
        </div>
    );
}

export default App;
