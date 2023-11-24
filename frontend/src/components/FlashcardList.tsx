import axios, { AxiosInstance } from "axios";
import React, { useState, useEffect } from "react";
import { toast } from "./toasts/ToastManager";
import Collapsible from "./Collapsible";
import FlashcardForm from "./FlashcardForm";
import { FaTrashAlt } from "react-icons/fa";
import { FieldValues, set } from "react-hook-form";
import MyModal from "./MyModal";

interface FlashcardListProps {
    axiosInstance: AxiosInstance;
    stackID: number;
    userIsAuthor?: boolean;
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

const FlashcardList = ({ axiosInstance, stackID, userIsAuthor = false }: FlashcardListProps) => {
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
                        content: "You Need to be the Author (or do you need to be logged in idk) of the Stack!",
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

        var image = "";
        if (data.answer_img[0]) {
            image = data.answer_img[0];
        } else {
            delete data.answer_img;
        }

        setFlashcards([
            ...flashcards,
            {
                id: 0,
                stack_id: stackID,
                question: data.question,
                answer_img: image,
                answer_char: data.answer_char,
                date_created: "",
                date_modified: "",
                priority_id: 0,
                user_priority: 1,
            },
        ]);

        const formData = new FormData();
        for (const key in data) {
            formData.append(key, data[key]);
        }
        if (image != "") {
            formData.append("answer_img", image);
        }

        axiosInstance
            .post(`api/flashcards/flashcards/listcreate/${stackID}/`, formData)
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
        setFlashcards(flashcards.filter((flashcard) => flashcard.id != flashcard.id));
        axiosInstance.delete(`api/flashcards/flashcards/detail/${flashcard.id}/`).catch((err) => {
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
            <div className="text-center">
                {userIsAuthor && (
                    <>
                        <MyModal button_text="Create Flashcard" title="Create Flashcard" size="lg">
                            <FlashcardForm onFormSubmit={createFlashcard} />
                        </MyModal>
                    </>
                )}
            </div>
            {isLoading && <div className="spinner-border"></div>}
            <div className="container">
                <div className="row">
                    {flashcards.map((flashcard) => (
                        <div className="col-sm-4 p-1" key={flashcard.id}>
                            <div className="card">
                                <div className="card-body">
                                    <h5 className="card-title">{flashcard.question}</h5>
                                    <p className="card-text">{flashcard.answer_char}</p>
                                    <p className="card-text">Priority : {flashcard.user_priority}</p>
                                </div>
                                <div className="card-footer text-center">
                                    <p>{flashcard.date_modified}</p>
                                    <div className="row">
                                        <div className="col-md-auto">
                                            <button className="btn btn-outline-danger" onClick={() => deleteFlashcard(flashcard)}>
                                                <FaTrashAlt />
                                            </button>
                                        </div>
                                        {userIsAuthor && (
                                            <div className="col-md-auto">
                                                <button className="btn btn-primary">Edit (not working)</button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
};

export default FlashcardList;
