import { AxiosInstance } from "axios";
import { useState, useEffect } from "react";

interface StackModalProps {
    axiosInstance: AxiosInstance;
    stackID: number;
    closeStack: () => void;
}
interface FlashcardStack {
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
interface Flashcard {
    id: number;
    stack: FlashcardStack;
    question: string;
    answer_type: string;
    answer_img: string;
    answer_char: string;
    date_created: string;
    date_modified: string;
}

const StackModal = ({
    axiosInstance,
    stackID,
    closeStack,
}: StackModalProps) => {
    const [stack, setStack] = useState<FlashcardStack>();
    const [flashcard, setFlashcard] = useState<Flashcard>();
    const [error, setError] = useState("");
    const [showAnswer, setShowAnswer] = useState(false);

    useEffect(() => {
        getNewFlashcard();
    }, []);

    const getNewFlashcard = () => {
        axiosInstance
            .get(`api/flashcard/flashcard/weightedflashcard/`)
            .then((res) => {
                setFlashcard(res.data);
            })
            .catch((err) => {
                setError(err.message);
            });
    };

    const getNextFlashCard = () => {};

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
