import Button from "./Button";
import { useForm, FieldValues, set } from "react-hook-form";

interface LoginFormProps {
    onFormSubmit: (data: FieldValues) => void;
    handleRegister: () => void;
}

const LoginForm = ({ onFormSubmit, handleRegister }: LoginFormProps) => {
    const { register, handleSubmit, formState } = useForm();

    return (
        <div className="container-sm">
            <form onSubmit={handleSubmit(onFormSubmit)}>
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">
                        Username
                    </label>
                    <input
                        {...register("username", {
                            required: true,
                        })}
                        id="username"
                        type="username"
                        className="form-control"
                        placeholder="username"
                    />
                    {formState.errors.username?.type === "required" && <p>This field is required!</p>}
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                        Password
                    </label>
                    <input {...register("password", { required: true })} id="password" type="password" className="form-control" placeholder="password" />
                    {formState.errors.password?.type === "required" && <p>This field is required!</p>}
                </div>
                <div className="row text-center">
                    <div className="col">
                        <Button text="Login" colour="success" type="submit" />
                    </div>
                    <div className="col">
                        <Button text="Register Instead" colour="primary" onClick={handleRegister} />
                    </div>
                </div>
            </form>
        </div>
    );
};

export default LoginForm;
