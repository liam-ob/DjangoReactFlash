import { useEffect, useState } from "react";
import Button from "./Button";
import Collapsible from "./Collapsible";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";
import { FieldValues } from "react-hook-form";
import axios, { AxiosInstance } from "axios";

interface NavbarProps {
    axiosInstance: AxiosInstance;
}

const Navbar = ({ axiosInstance }: NavbarProps) => {
    const [user, setUser] = useState({
        id: "",
        username: "",
    });

    const [login, setLogin] = useState(true);
    const [register, setRegister] = useState(false);

    // Set the logged in user. probably make this a jwt token
    useEffect(() => {
        const controller = new AbortController();
        axiosInstance
            .post("api/core/users/checklogin/")
            .then((response) => {
                console.log(response?.data);
                setUser(response.data);
            })
            .catch((err) => {
                console.log(err);
            });
        return () => {
            controller.abort();
        };
    }, []);

    const loginUser = (data: FieldValues) => {
        console.log(data);
        const originalUser = user;
        setUser({ id: data.id, username: data.username });
        axiosInstance
            .post("api/core/users/login/", data)
            .then((response) => {
                console.log(response);
                // Make this a jwt token
                localStorage.setItem("token", response.data.token);
            })
            .catch((err) => {
                console.log(err);
                setUser(originalUser);
            });
    };

    const registerUser = (data: FieldValues) => {
        console.log(data);
        const originalUser = user;
        setUser({ id: data.id, username: data.username });
        axiosInstance
            .post("api/core/users/register/", data)
            .then((response) => {
                console.log(response);
                // Make this a jwt token
                localStorage.setItem("token", response.data.token);
            })
            .catch((err) => {
                console.log(err);
                setUser(originalUser);
            });
    };

    const logoutUser = () => {
        const originalUser = user;
        setUser({ id: "", username: "" });
        axiosInstance
            .get("api/core/users/logout/")
            .then((response) => {
                console.log(response);
                localStorage.removeItem("token");
            })
            .catch((err) => {
                console.log(err);
                setUser(originalUser);
            });
    };

    const handleLoginRegisterSwitch = () => {
        setLogin(!login);
        setRegister(!register);
    };

    return (
        <header className="border-bottom">
            <nav className="container-md">
                <div className="row justify-content-md-center">
                    <a className="col-sm-8 d-none d-sm-block nav-link px-2 link-primary">
                        <strong>DRF</strong>lashcards
                    </a>
                    {user.username === "" ? (
                        <>
                            <div className="col-sm-4 col- row">
                                <div className="p-1 col">
                                    <Collapsible text={register ? "Login" : "Register"}>
                                        {register && (
                                            <>
                                                <LoginForm onFormSubmit={loginUser} handleRegister={handleLoginRegisterSwitch} />
                                            </>
                                        )}
                                        {login && (
                                            <>
                                                <RegisterForm onFormSubmit={registerUser} handleLogin={handleLoginRegisterSwitch} />
                                            </>
                                        )}
                                    </Collapsible>
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className="col-sm-4">
                            <div className="container py-2">
                                <div className="row text-center">
                                    <div className="col-6">
                                        <span className="badge rounded-pill text-bg-dark">{user.username}</span>
                                    </div>
                                    <div className="col-6">
                                        <Button text="Logout" onClick={logoutUser} />
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </nav>
        </header>
    );
};

export default Navbar;
