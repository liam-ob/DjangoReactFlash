import React, { useState, useEffect, MouseEventHandler } from "react";
import axios, { AxiosInstance, CanceledError } from "axios";
import Button from "./Button";
import FlashcardStackForm from "./FlashcardStackForm";
import Collapsible from "./Collapsible";
import FlashcardList from "./FlashcardList";
import { FaTrashAlt } from "react-icons/fa";
import { FieldValues } from "react-hook-form";
import { toast } from "./toasts/ToastManager";
import MyModal from "./MyModal";

interface FlashcardStackListProps {
    axiosInstance: AxiosInstance;
    launchStack: (id: number) => MouseEventHandler<HTMLButtonElement>;
}
export interface FlashcardStack {
    id: number;
    author: {
        id: number;
        username: string;
    };
    public: boolean;
    name: string;
    difficulty: string;
    date_created: string;
    date_modified: string;
}

const FlashcardStackList = ({
    axiosInstance,
    launchStack,
}: FlashcardStackListProps) => {
    const [flashcardStacks, setFlashcardStacks] = useState<FlashcardStack[]>(
        []
    );
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        const controller = new AbortController();
        setIsLoading(true);
        axiosInstance
            .get<FlashcardStack[]>(
                "api/flashcards/flashcardstacks/listcreate/",
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
                toast.show({
                    title: "Error",
                    content: "Failed to get flashcard stacks: " + err.message,
                    duration: 5000,
                });
            })
            // Doesnt work in strict mode?
            .finally(() => {
                setIsLoading(false);
            });

        return () => {
            controller.abort();
        };
    }, []);

    const deleteStack = (flashcardStack: FlashcardStack) => {
        // save current state in case of error
        const origianalFlashcardStacks = [...flashcardStacks];
        // provide instant feedback to user by removing flashcardStack from list
        setFlashcardStacks(
            flashcardStacks.filter((stack) => stack.id != flashcardStack.id)
        );
        axiosInstance
            .delete("api/flashcards/flashcardstacks/" + flashcardStack.id + "/")
            .catch((err) => {
                setError(err.message);
                setFlashcardStacks(origianalFlashcardStacks);
            });
    };

    const createStack = (data: FieldValues) => {
        const originalFlashcardStacks = [...flashcardStacks];
        setFlashcardStacks([
            ...flashcardStacks,
            {
                id: 0,
                author: {
                    id: 0,
                    username: "",
                },
                public: data.public,
                name: data.name,
                difficulty: data.difficulty,
                date_created: "",
                date_modified: "",
            },
        ]);
        axiosInstance
            .post("api/flashcards/flashcardstacks/listcreate/", data)
            .then((response) => {
                if (response.status === 201) {
                    console.log("Flashcard stack created!");
                    setFlashcardStacks([response.data, ...flashcardStacks]);
                } else if (response.status === 403 || response.status === 401) {
                    setError(
                        "You are not authorized to create a flashcard stack!"
                    );
                }
            })
            .catch((err) => {
                setError(err.message);
                setFlashcardStacks(originalFlashcardStacks);
            });
    };

    return (
        <>
            {error != "" && <p className="text-danger">{error}</p>}
            {isLoading && <div className="spinner-border"></div>}
            <div className="container-fluid text-center row p-5">
                <h1 className="col">Flashcard Stacks</h1>
                <div className="col">
                    <Collapsible text="Create Flashcard Stack">
                        <FlashcardStackForm onFormSubmit={createStack} />
                    </Collapsible>
                </div>
            </div>
            <div className="row row-cols-1 row-cols-4 g-4">
                {flashcardStacks.map((flashcardStack) => (
                    <div key={flashcardStack.id} className="col">
                        <div className="card p-3">
                            <div className="card-body d-flex justify-content-between">
                                <h5 className="card-title">
                                    {flashcardStack.name}
                                </h5>
                                <button
                                    className="btn btn-primary"
                                    onClick={launchStack(flashcardStack.id)}
                                >
                                    Launch Stack
                                </button>
                            </div>

                            <p className="card-text">
                                Difficulty : {flashcardStack.difficulty}
                            </p>
                            <p className="card-text">
                                <small className="text-muted">
                                    Last Updated :{" "}
                                    {flashcardStack.date_modified}
                                </small>
                            </p>

                            <div className="text-muted d-flex justify-content-between pb-1">
                                Author : {flashcardStack.author.username}
                                <button
                                    className="btn btn-outline-danger"
                                    onClick={() => deleteStack(flashcardStack)}
                                >
                                    <FaTrashAlt />
                                </button>
                            </div>
                            <div className="card-footer">
                                <div className="text-center">
                                    <MyModal
                                        button_text="edit"
                                        title="Flashcards"
                                        size="xl"
                                    >
                                        <div className="card card-body">
                                            <FlashcardList
                                                axiosInstance={axiosInstance}
                                                stackID={flashcardStack.id}
                                            />
                                        </div>
                                    </MyModal>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </>
    );
};

export default FlashcardStackList;
