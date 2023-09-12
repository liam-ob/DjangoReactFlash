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
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        const controller = new AbortController();
        setIsLoading(true);
        axios
            .get<FlashcardStack[]>(
                apiURL + "api/flashcards/flashcardstacks/listcreate/",
                { signal: controller.signal }
            )
            .then((response) => {
                setFlashcardStacks(response.data);
                setIsLoading(false);
            })
            .catch((err) => {
                if (err instanceof CanceledError) {
                    return;
                }
                setIsLoading(false);
                setError(err.message);
            })
            // Doesnt work in strict mode?
            .finally(() => {
                setIsLoading(false);
            });

        return () => {
            controller.abort();
        };
    }, []);

    return (
        <>
            {error != "" && <p className="text-danger">{error}</p>}
            {isLoading && <div className="spinner-border"></div>}
            <div className="container-fluid text-center row">
                <h5 className="col">Flashcard Stacks</h5>
                <div className="col">
                    <Collapsible text="Create Flashcard Stack">
                        <FlashcardStackForm apiURL={apiURL} />
                    </Collapsible>
                </div>
            </div>
        </>
    );
};

export default FlashcardStackList;
