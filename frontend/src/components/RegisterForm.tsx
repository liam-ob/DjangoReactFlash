import Button from "./Button";
import { useForm, FieldValues } from "react-hook-form";

interface RegisterFormProps {}

const RegisterForm = () => {
    const {
        register,
        handleSubmit,
        formState: { errors, isValid },
    } = useForm();
    let emailRegexExp = new RegExp(/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i);

    const emailValidation = (email: string) => {
        console.log("validate email called: " + email);
        return emailRegexExp.test(email);
    };

    const onFormSubmit = (data: FieldValues) => {
        console.log(data);
    };

    return (
        <form onSubmit={onFormSubmit} className="container-sm">
            <div className="mb-3">
                <label htmlFor="username" className="form-label">
                    Username
                </label>
                <input
                    {...register("username", {
                        required: true,
                        minLength: 4,
                    })}
                    id="username"
                    type="text"
                    className="form-control"
                    placeholder="Username"
                />
                {errors.username?.type === "required" && (
                    <p>This field is required</p>
                )}
                {errors.username?.type === "minLength" && (
                    <p>Username must be at least 4 characters long</p>
                )}
            </div>
            <div className="mb-3">
                <label htmlFor="email" className="form-label">
                    Email
                </label>
                <input
                    {...register("email", {
                        required: true,
                        validate: emailValidation,
                    })}
                    id="email"
                    type="email"
                    className="form-control"
                    placeholder="Email"
                />
                {errors.email?.type === "required" && (
                    <p>This field is required</p>
                )}
                {errors.email?.type === "validate" && (
                    <p>Please enter a valid email</p>
                )}
            </div>
            <div className="mb-3">
                <label htmlFor="password" className="form-label">
                    Password
                </label>
                <input
                    {...register("password", { required: true, minLength: 8 })}
                    id="password"
                    type="password"
                    className="form-control"
                    placeholder="password"
                />
                {errors.password?.type === "minLength" && (
                    <p>Username must be at least 8 characters long</p>
                )}
            </div>
            <div className="mb-3">
                <label htmlFor="password2" className="form-label">
                    Confirm Password
                </label>
                <input
                    {...register("password2", {
                        required: true,
                        validate: (value) => value === "password",
                    })}
                    id="password2"
                    type="password"
                    className="form-control"
                    placeholder="confirm password"
                />
                {errors.password2?.type === "required" && (
                    <p>This field is required</p>
                )}
                {errors.password2?.type === "validate" && (
                    <p>Passwords must match</p>
                )}
            </div>
            <Button text="Register" type="submit" colour="success" />
        </form>
    );
};

export default RegisterForm;
