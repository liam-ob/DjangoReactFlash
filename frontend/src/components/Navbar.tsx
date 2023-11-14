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

    return (
        <header className="p-3 mb-3 border-bottom">
            <nav className="container">
                <div className="d-flex flex-wrap aling-items-center justify-content-center">
                    <ul className="nav col-12 col-lg-auto me-lg-auto link-body-emphasis text-decoration-none">
                        <li>
                            <a className="nav-link px-2 link-primary">
                                <strong>DRF</strong>lashcards
                            </a>
                        </li>
                    </ul>
                    {user.username === "" ? (
                        <>
                            <div className="justify-content row w-50">
                                <div className="col-6">
                                    <Collapsible text="Login">
                                        <LoginForm onFormSubmit={loginUser} />
                                    </Collapsible>
                                </div>
                                <div className="col-6">
                                    <Collapsible text="Register">
                                        <RegisterForm onFormSubmit={registerUser} />
                                    </Collapsible>
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className="d-flex">
                            <div className="me-2">{user.username}</div>
                            <Button text="Logout" onClick={logoutUser} />
                        </div>
                    )}
                </div>
            </nav>
        </header>
    );
};

export default Navbar;
