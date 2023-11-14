import { useState } from "react";
import { useForm, FieldValues } from "react-hook-form";
import Button from "./Button";
import axios, { AxiosError, AxiosInstance } from "axios";

interface FlashcardStackFormProps {
    onFormSubmit: (data: FieldValues) => void;
}

const FlashcardStackForm = ({ onFormSubmit }: FlashcardStackFormProps) => {
    const { register, handleSubmit, formState } = useForm();

    return (
        <>
            <form onSubmit={handleSubmit(onFormSubmit)} className="container">
                <div className="border rounded border-priamry border-2 m-auto">
                    <div className="m-auto p-2">
                        <input {...register("public")} className="form-check-input" type="checkbox" value="" id="public"></input>
                        <label className="form-check-label px-3" htmlFor="public">
                            Make this stack public
                        </label>
                    </div>
                    <div className="m-auto p-2">
                        <label htmlFor="name" className="form-label">
                            Flashcard Stack Name
                        </label>
                        <input
                            {...register("name", {
                                required: true,
                            })}
                            id="name"
                            type="text"
                            className="form-control"
                            placeholder="Flashcard Stack Name"
                        />
                        {formState.errors.name?.type === "required" && <p>This field is required</p>}
                    </div>
                    <div className="p-2">
                        <label htmlFor="difficulty" className="form-label">
                            Stack Difficulty
                        </label>
                        <select
                            {...register("difficulty", {
                                required: true,
                            })}
                            className="form-select"
                            id="difficulty"
                        >
                            <option value="easy">Easy</option>
                            <option value="medium">Medium</option>
                            <option value="hard">Hard</option>
                        </select>
                    </div>
                    <div className="p-3">
                        <Button text="Create Flashcard Stack" type="submit" />
                    </div>
                </div>
            </form>
        </>
    );
};

export default FlashcardStackForm;
