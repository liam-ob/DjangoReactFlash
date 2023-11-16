import { useState } from "react";
import Modal from "react-bootstrap/Modal";
import ModalBody from "react-bootstrap/ModalBody";
import ModalHeader from "react-bootstrap/ModalHeader";
import ModalFooter from "react-bootstrap/ModalFooter";
import ModalTitle from "react-bootstrap/ModalTitle";

interface MyModalProps {
    title: string;
    button_text: string;
    button_size?: "sm" | "md" | "lg";
    children?: React.ReactNode;
    size?: "sm" | "lg" | "xl" | undefined;
}

const MyModal = ({ title, button_text, button_size = "sm", children, size = "sm" }: MyModalProps) => {
    const [show, setShow] = useState(false);

    return (
        <>
            <button
                className={"btn  h-100 btn-primary btn-" + button_size}
                onClick={() => {
                    setShow(!show);
                }}
            >
                {button_text}
            </button>
            {show && (
                <Modal
                    show={show}
                    size={size}
                    onHide={() => {
                        setShow(false);
                    }}
                    backdrop="static"
                    keyboard={false}
                >
                    <ModalHeader>
                        <ModalTitle>{title}</ModalTitle>
                        <button
                            type="button"
                            className="btn-close float-end"
                            onClick={() => {
                                setShow(false);
                            }}
                        ></button>
                    </ModalHeader>

                    <ModalBody>{children}</ModalBody>
                </Modal>
            )}
        </>
    );
};

export default MyModal;
