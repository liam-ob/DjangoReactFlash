import { useState, useRef } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import FlashcardStackList from "./components/FlashcardStackList";
import StackModal from "./components/StackModal";
import axios from "axios";

function App() {
    const axiosInstance = axios.create({
        baseURL: "http://localhost:8000/",
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
