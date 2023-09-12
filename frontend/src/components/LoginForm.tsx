import Button from "./Button";
import React, { FormEvent, useRef } from "react";
import { useForm, FieldValues } from "react-hook-form";

interface LoginFormProps {}

const LoginForm = () => {
    const { register, handleSubmit, formState } = useForm();
    let emailRegexExp = new RegExp(/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i);

    const onFormSubmit = (data: FieldValues) => {
        console.log(data);
    };

    const emailValidation = (email: string) => {
        console.log("validate email called: " + email);
        return emailRegexExp.test(email);
    };

    return (
        <div className="container-sm">
            <form onSubmit={handleSubmit(onFormSubmit)}>
                <div className="mb-3">
                    <label htmlFor="email" className="form-label">
                        Email
                    </label>
                    <input
                        {...register("name", {
                            required: true,
                            validate: emailValidation,
                            minLength: 5,
                        })}
                        id="email"
                        type="email"
                        className="form-control"
                        placeholder="Email"
                    />
                    {formState.errors.username?.type === "required" && (
                        <p>This field is required!</p>
                    )}
                    {formState.errors.username?.type === "validate" && (
                        <p>Invalid email!</p>
                    )}
                    {formState.errors.username?.type === "minLength" && (
                        <p>Please make the email longer!</p>
                    )}
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                        Password
                    </label>
                    <input
                        {...register("password", { required: true })}
                        id="password"
                        type="password"
                        className="form-control"
                        placeholder="password"
                    />
                    {formState.errors.password?.type === "required" && (
                        <p>This field is required!</p>
                    )}
                </div>
                <Button text="Login" colour="success" type="submit" />
            </form>
        </div>
    );
};

export default LoginForm;
