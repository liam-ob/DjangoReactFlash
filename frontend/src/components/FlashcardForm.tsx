import { useForm, FieldValues } from "react-hook-form";
import Button from "./Button";

interface FlashcardFormProps {
    onFormSubmit: (data: FieldValues) => void;
}

const FlashcardForm = ({ onFormSubmit }: FlashcardFormProps) => {
    const { register, handleSubmit, formState } = useForm();

    return (
        <>
            <form onSubmit={handleSubmit(onFormSubmit)} className="row g-3">
                <div className="col-md-12">
                    <label htmlFor="question" className="form-label">
                        Question
                    </label>
                    <input
                        {...register("question", {
                            required: true,
                        })}
                        id="question"
                        type="text"
                        className="form-control"
                        placeholder="Question"
                    ></input>
                    {formState.errors.question?.type === "required" && (
                        <p>This field is required</p>
                    )}
                </div>
                <div className="col-md-9">
                    <label htmlFor="answer_char" className="form-label">
                        Answer
                    </label>
                    <input
                        {...register("answer_char", { maxLength: 1000 })}
                        id="answer_char"
                        type="text"
                        className="form-control"
                        placeholder="Answer"
                    ></input>
                    {formState.errors.answer_char?.type === "maxLength" && (
                        <p>Answer must be less than 1000 characters</p>
                    )}
                </div>
                <div className="col-md-3">
                    <label htmlFor="answer_img" className="form-label">
                        Image (optional)
                    </label>
                    <input
                        {...register("answer_img")}
                        id="answer_img"
                        type="file"
                        className="form-control"
                        placeholder="Answer Image"
                    ></input>
                </div>
                <div className="col-12">
                    <Button
                        type="submit"
                        text="Create Flashcard"
                        disabled={formState.isSubmitting}
                    />
                </div>
            </form>
        </>
    );
};

export default FlashcardForm;
