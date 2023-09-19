import { AxiosInstance } from "axios";
import { useState, useEffect } from "react";
import { toast } from "./toasts/ToastManager";
import { Flashcard } from "./FlashcardList";

interface StackModalProps {
    axiosInstance: AxiosInstance;
    stackID: number;
    closeStack: () => void;
}

const StackModal = ({
    axiosInstance,
    stackID,
    closeStack,
}: StackModalProps) => {
    const [flashcard, setFlashcard] = useState<Flashcard>();
    const [showAnswer, setShowAnswer] = useState(false);

    useEffect(() => {
        getNewFlashcard();
    }, []);

    const getNewFlashcard = () => {
        axiosInstance
            .get(`api/flashcard/flashcard/weightedflashcard/${stackID}/`)
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

    const postPriority = () => {};

    return (
        <div className="modal-dialog modal-xl" role="document">
            <div className="modal-content rounded-4 shadow">
                <div className="modal-header p-5 pb-4 border-bottom-0">
                    <h1 className="fw-bold mb-0 fs-2">Flashcard Stack</h1>
                    <button
                        type="button"
                        className="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                        onClick={closeStack}
                    ></button>
                </div>

                <div className="modal-body p-5 pt-0">
                    {flashcard?.question ? (
                        <h3>{flashcard.question}</h3>
                    ) : (
                        <p>No Question</p>
                    )}
                </div>
                <div className="modal-footer">
                    <div className="text-start">Change Priority</div>
                    <div className="text-center">
                        <button className="btn btn-primary">-1</button>
                        <button className="btn btn-primary">+1</button>
                        <button className="btn btn-primary">+2</button>
                    </div>
                    <div className="text-end">
                        <button className="btn btn-primary">
                            <h4>Answer</h4>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default StackModal;
