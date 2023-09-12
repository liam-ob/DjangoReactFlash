import { useState } from "react";
import { useForm, FieldValues } from "react-hook-form";
import Button from "./Button";
import axios, { AxiosError } from "axios";

interface FlashcardStackFormProps {
    apiURL: string;
}

const FlashcardStackForm = ({ apiURL }: FlashcardStackFormProps) => {
    const { register, handleSubmit, formState } = useForm();
    const [error, setError] = useState("");

    const onFormSubmit = async (data: FieldValues) => {
        try {
            const response = await axios.post(
                apiURL + "api/flashcards/flashcardstacks/listcreate/",
                data,
                { headers: { "Content-Type": "application/json" } }
            );
            if (response.status === 201) {
                console.log("Flashcard stack created!");
            } else if (response.status === 403 || response.status === 401) {
                setError("You are not authorized to create a flashcard stack!");
            }
            console.log(response);
        } catch (err) {
            setError((err as AxiosError).message);
        }
    };

    return (
        <>
            {error != "" && <p className="text-danger">{error}</p>}
            <form onSubmit={handleSubmit(onFormSubmit)}>
                <div className="mb-3">
                    <input
                        {...register("publicFlashcardStack")}
                        className="form-check-input"
                        type="checkbox"
                        value=""
                        id="publicFlashcardStack"
                    ></input>
                    <label
                        className="form-check-label"
                        htmlFor="publicFlashcardStack"
                    >
                        Make this stack public
                    </label>
                </div>
                <div className="mb-3">
                    <label htmlFor="flashcardStackName" className="form-label">
                        Flashcard Stack Name
                    </label>
                    <input
                        {...register("flashcardStackName", { required: true })}
                        id="flashcardStackName"
                        type="text"
                        className="form-control"
                        placeholder="Flashcard Stack Name"
                    />
                    {formState.errors.flashcardStackName?.type ===
                        "required" && <p>This field is required</p>}
                </div>
                <div className="mb-3">
                    <label htmlFor="flashcardDifficulty" className="form-label">
                        Stack Difficulty
                    </label>
                    <select
                        {...register("flashcardDifficulty", { required: true })}
                        className="form-select"
                        id="flashcardDifficulty"
                    >
                        <option value="easy">Easy</option>
                        <option value="medium">Medium</option>
                        <option value="hard">Hard</option>
                    </select>
                </div>
                <Button text="Create Flashcard Stack" type="submit" />
            </form>
        </>
    );
};

export default FlashcardStackForm;
