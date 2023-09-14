import { useState } from "react";
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
    const launchStack = (id: number) => () => {
        setStackID(id);
    };
    const closeStack = () => {
        setStackID(0);
    };

    return (
        <div>
            <Navbar axiosInstance={axiosInstance} />
            <FlashcardStackList
                axiosInstance={axiosInstance}
                launchStack={launchStack}
            />
            {stackID !== 0 && (
                <StackModal
                    axiosInstance={axiosInstance}
                    stackID={stackID}
                    closeStack={closeStack}
                />
            )}
        </div>
    );
}

export default App;
