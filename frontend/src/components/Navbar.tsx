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

    return (
        <nav className="navbar bg-body-tertiary">
            <div className="container-fluid">
                <a className="navbar-brand" href="#">
                    DRFlashcards
                </a>
                {user.username === "" ? (
                    <div className="d-flex">
                        <Button text="Login" onClick={() => {}} />
                    </div>
                ) : (
                    <div className="d-flex">
                        <div className="me-2">{user.username}</div>
                        <Button text="Logout" onClick={() => {}} />
                    </div>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
