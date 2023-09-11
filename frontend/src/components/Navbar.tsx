import { useState } from "react";
import Button from "./Button";

interface NavbarProps {
    apiURL: string;
}

const Navbar = ({ apiURL }: NavbarProps) => {
    const [user, setUser] = useState({
        username: "",
        email: "",
        id: "",
    });

    const onClickLogin = () => {
        fetch(apiURL + "/api/core/users/login/", {
            method: "post",
            credentials: "same-origin",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: "admin",
                password: "admin",
            }),
        })
            .then((response) => {
                if (response.status !== 200) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                console.log(data);
                setUser(data);
            })
            .catch((error) => {
                console.error(
                    "There has been a problem with your fetch operation:",
                    error
                );
            });
    };
    const onClickLogout = () => {
        fetch(apiURL + "/api/core/users/logout/")
            .then((response) => {
                if (response.status !== 200) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                setUser({ ...user, username: "" });
                console.log(data);
            })
            .catch((error) => {
                console.error(
                    "There has been a problem with your fetch operation:",
                    error
                );
            });
    };

    return (
        <nav className="navbar bg-body-tertiary">
            <div className="container-fluid">
                <a className="navbar-brand" href="#">
                    DRFlashcards
                </a>
                {user.username === "" ? (
                    <div className="d-flex">
                        <Button text="Login" onClick={onClickLogin} />
                    </div>
                ) : (
                    <div className="d-flex">
                        <div className="me-2">{user.username}</div>
                        <Button text="Logout" onClick={onClickLogout} />
                    </div>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
