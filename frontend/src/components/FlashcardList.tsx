import axios, { AxiosInstance } from "axios";
import React, { useState, useEffect } from "react";
import { toast } from "./toasts/ToastManager";
import Collapsible from "./Collapsible";
import FlashcardForm from "./FlashcardForm";
import { FaTrashAlt } from "react-icons/fa";
import { FieldValues, set } from "react-hook-form";

interface FlashcardListProps {
    axiosInstance: AxiosInstance;
    stackID: number;
}
export interface Flashcard {
    id: number;
    stack_id: number;
    question: string;
    answer_img: string;
    answer_char: string;
    date_created: string;
    date_modified: string;
    priority_id: number;
    user_priority: number;
}

const FlashcardList = ({ axiosInstance, stackID }: FlashcardListProps) => {
    const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const controller = new AbortController();
        getFlashcards();
        return () => {
            controller.abort();
        };
    }, []);

    const getFlashcards = () => {
        setIsLoading(true);
        axiosInstance
            .get(`api/flashcards/flashcards/listcreate/${stackID}/`)
            .then((res) => {
                setFlashcards(res.data);
                setIsLoading(false);
                if (res.status === 401 || res.status === 403) {
                    toast.show({
                        title: "Error",
                        content:
                            "You Need to be the Author (or do you need to be logged in idk) of the Stack!",
                        duration: 10000,
                    });
                }
            })
            .catch((err) => {
                setIsLoading(false);
                toast.show({
                    title: "Error",
                    content: "Failed to get flashcard list: " + err.message,
                    duration: 10000,
                });
            })
            .finally(() => setIsLoading(false));
    };

    const createFlashcard = (data: FieldValues) => {
        data = { ...data, stack_id: stackID };
        const originalFlashcards = [...flashcards];
        setFlashcards([
            ...flashcards,
            {
                id: 0,
                stack_id: stackID,
                question: data.question,
                answer_img: data.answer_img,
                answer_char: data.answer_char,
                date_created: "",
                date_modified: "",
                priority_id: 0,
                user_priority: 1,
            },
        ]);

        if (data.answer_img[0]) {
            const formData = new FormData();
            formData.append("answer_char", data.answer_char);
            data = { ...data, answer_img: data.answer_img[0].name };
            formData.append("question", data.question);
        } else {
            delete data.answer_img;
        }
        console.log(data);
        axiosInstance
            .post(`api/flashcards/flashcards/listcreate/${stackID}/`, data)
            .then((res) => {
                if (res.status === 201) {
                    setFlashcards([res.data, ...flashcards]);
                } else if (res.status === 403 || res.status === 401) {
                    toast.show({
                        title: "Error",
                        content: "You Need to be the Author of the Stack!",
                        duration: 5000,
                    });
                    setFlashcards(originalFlashcards);
                }
                console.log(res);
            })
            .catch((err) => {
                toast.show({
                    title: "Error",
                    content: "Failed to create flashcard: " + err.message,
                    duration: 5000,
                });
                setFlashcards(originalFlashcards);
            });
    };

    const deleteFlashcard = (flashcard: Flashcard) => {
        const originalFlashcards = [...flashcards];
        setFlashcards(
            flashcards.filter((flashcard) => flashcard.id != flashcard.id)
        );
        axiosInstance
            .delete(`api/flashcards/flashcards/detail/${flashcard.id}/`)
            .catch((err) => {
                toast.show({
                    title: "Error",
                    content: "Failed to delete flashcard: " + err.message,
                    duration: 5000,
                });
                setFlashcards(originalFlashcards);
            });
    };

    return (
        <>
            <div className="row text-center">
                <Collapsible text="Create Flashcard">
                    <FlashcardForm onFormSubmit={createFlashcard} />
                </Collapsible>
            </div>
            {isLoading && <div className="spinner-border"></div>}
            {flashcards.map((flashcard) => (
                <div className="card" key={flashcard.id}>
                    <div className="card-body">
                        <h5 className="card-title">{flashcard.question}</h5>
                        <p className="card-text">{flashcard.answer_char}</p>
                        {flashcard?.answer_img && (
                            <p className="card-text">{flashcard.answer_img}</p>
                        )}
                        <p className="card-text">
                            Priority : {flashcard.priority_id}
                        </p>
                    </div>
                    <div className="card-footer">
                        <p>{flashcard.date_modified}</p>
                        <button
                            className="btn btn-outline-danger"
                            onClick={() => deleteFlashcard(flashcard)}
                        >
                            <FaTrashAlt />
                        </button>
                        <button className="btn btn-primary">Edit</button>
                    </div>
                </div>
            ))}
        </>
    );
};

export default FlashcardList;
