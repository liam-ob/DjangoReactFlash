import { useState } from "react";
import Button from "./Button";

interface NavbarProps {
    apiURL: string;
}

// Does this even work??
const fetchAPI = (url: string, my_function: () => void) => {
    fetch(url)
        .then((response) => {
            if (response.status !== 200) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => {
            my_function();
        })
        .catch((error) => {
            console.error(
                "There has been a problem with your fetch operation:",
                error
            );
        });
};

const Navbar = ({ apiURL }: NavbarProps) => {
    const [user, setUser] = useState({
        username: "",
        email: "",
        id: "",
    });

    const onClickLogin = () => {
        fetch(apiURL + "/api/core/login")
            .then((response) => {
                if (response.status !== 200) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
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
        fetch(apiURL + "/api/core/logout")
            .then((response) => {
                if (response.status !== 200) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                setUser({ ...user, username: "" });
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
