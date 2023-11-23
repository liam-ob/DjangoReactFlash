import { AxiosInstance } from "axios";
import { useState, useEffect } from "react";
import { toast } from "./toasts/ToastManager";
import { Flashcard } from "./FlashcardList";
import MyModal from "./MyModal";
import { set } from "react-hook-form";

interface StackModalProps {
    axiosInstance: AxiosInstance;
    stackID: number;
}

const StackModal = ({ axiosInstance, stackID }: StackModalProps) => {
    const [flashcard, setFlashcard] = useState<Flashcard>();
    const [showAnswer, setShowAnswer] = useState(false);
    const [start, setStart] = useState(false);

    useEffect(() => {
        start && getNewFlashcard();
    }, [start]);

    const getNewFlashcard = () => {
        axiosInstance
            .get(`api/flashcards/flashcards/weightedflashcard/${stackID}/`)
            .then((res) => {
                setFlashcard(res.data);
            })
            .catch((err) => {
                toast.show({
                    title: "Error",
                    content: "Failed to get flashcard: " + err.message,
                    duration: 5000,
                });
            });
    };

    const postPriority = (priorityChange: number) => {
        if (flashcard) {
            axiosInstance
                .post(`api/flashcards/flashcards/weightedflashcard/${flashcard.id}/`, {
                    id: flashcard.priority_id,
                    priority: priorityChange + flashcard.user_priority,
                    flashcard_id: flashcard.id,
                })
                .catch((err) => {
                    toast.show({
                        title: "Error",
                        content: "Failed to update priority! Error: " + err.message,
                        duration: 5000,
                    });
                });
            getNewFlashcard();
        }
    };

    return (
        <>
            <MyModal button_text="Launch" title="Stack" size="lg">
                {start ? (
                    <>
                        <div className="p-5 pt-0">
                            {flashcard?.question ? (
                                <>
                                    <h5>Question</h5>
                                    <p>{flashcard.question}</p>
                                </>
                            ) : (
                                <p>No Question</p>
                            )}
                        </div>
                        <div className="p-4 pt-0">
                            {showAnswer ? (
                                <>
                                    {flashcard?.answer_char ? (
                                        <>
                                            <h5>Answer</h5>
                                            <p>{flashcard?.answer_char}</p>
                                            <img
                                                style={{ maxWidth: "300px" }}
                                                src={flashcard?.answer_img && "http://127.0.0.1:8000" + flashcard.answer_img}
                                                alt="image"
                                            />
                                        </>
                                    ) : (
                                        <p>No Answer</p>
                                    )}
                                </>
                            ) : (
                                <button
                                    className="btn btn-primary"
                                    onClick={() => {
                                        setShowAnswer(true);
                                    }}
                                >
                                    <h4>Answer</h4>
                                </button>
                            )}
                        </div>
                        <div className="modal-footer">
                            <div className="">Change Priority</div>
                            <div className="text-center p-1">
                                <button
                                    className="btn btn-primary"
                                    onClick={() => {
                                        postPriority(-1);
                                        setShowAnswer(false);
                                    }}
                                >
                                    -1
                                </button>
                                <button
                                    className="btn btn-primary"
                                    onClick={() => {
                                        postPriority(0);
                                        setShowAnswer(false);
                                    }}
                                >
                                    +0
                                </button>
                                <button
                                    className="btn btn-primary"
                                    onClick={() => {
                                        postPriority(1);
                                        setShowAnswer(false);
                                    }}
                                >
                                    +1
                                </button>
                                <button
                                    className="btn btn-primary"
                                    onClick={() => {
                                        postPriority(2);
                                        setShowAnswer(false);
                                    }}
                                >
                                    +2
                                </button>
                            </div>
                        </div>
                    </>
                ) : (
                    <button
                        className="btn btn-primary p-2"
                        onClick={() => {
                            setStart(true);
                        }}
                    >
                        Start
                    </button>
                )}
            </MyModal>
        </>
    );
};

export default StackModal;
