import { AxiosInstance } from "axios";
import { useState } from "react";

interface StackModalProps {
    axiosInstance: AxiosInstance;
    stackID: number;
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

const StackModal = ({ axiosInstance, stackID }: StackModalProps) => {
    const [stack, setStack] = useState<FlashcardStack>();
    const [flashcard, setFlashcard] = useState<Flashcard>();

    axiosInstance
        .get(`api/flashcard/flashcard/weightedflashcard/`)
        .then((res) => {})
        .catch((err) => {});
};

export default StackModal;
