import React, { useState, useEffect } from "react";
import axios, { CanceledError } from "axios";
import Button from "./Button";
import FlashcardStackForm from "./FlashcardStackForm";
import Collapsible from "./Collapsible";

interface FlashcardStackListProps {
    apiURL: string;
}
interface FlashcardStack {
    id: number;
    author: string;
    public: boolean;
    name: string;
    difficulty: string;
    date_created: string;
    date_modified: string;
}

const FlashcardStackList = ({ apiURL }: FlashcardStackListProps) => {
    const [flashcardStacks, setFlashcardStacks] = useState<FlashcardStack[]>(
        []
    );
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");
    const controller = new AbortController();

    useEffect(() => {
        axios
            .get<FlashcardStack[]>(
                apiURL + "api/flashcards/flashcardstacks/listcreate/",
                { signal: controller.signal }
            )
            .then((response) => setFlashcardStacks(response.data))
            .catch((err) => {
                if (err instanceof CanceledError) {
                    return;
                }
                setError(err.message);
            });

        return () => {
            controller.abort();
        };
    }, []);

    return (
        <>
            {error != "" && <p className="text-danger">{error}</p>}
            <div className="container mb-3">
                <h5>Flashcard Stacks</h5>
                <Collapsible text="Create Flashcard Stack">
                    <FlashcardStackForm apiURL={apiURL} />
                </Collapsible>
            </div>
        </>
    );
};

export default FlashcardStackList;
