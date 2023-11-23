import { useState, useRef } from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import FlashcardStackList from "./components/FlashcardStackList";
import StackModal from "./components/StackModal";
import axios from "axios";

function App() {
    var baseURL = "";
    if (window.location.origin === "http://localhost:5173") {
        baseURL = "http://localhost:8000";
    } else {
        baseURL = window.location.origin;
    }

    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.withCredentials = true;

    const axiosInstance = axios.create({
        baseURL: baseURL,
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
