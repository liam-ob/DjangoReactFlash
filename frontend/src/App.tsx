import { useState } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import FlashcardStackList from "./components/FlashcardStackList";
import axios from "axios";

function App() {
    const axiosInstance = axios.create({
        baseURL: "http://localhost:8000/",
        headers: {
            Authorization: `Token ${localStorage.getItem("token")}`,
        },
    });
    return (
        <div>
            <Navbar axiosInstance={axiosInstance} />
            <FlashcardStackList axiosInstance={axiosInstance} />
        </div>
    );
}

export default App;
