import { useState } from "react";
import Modal from "react-bootstrap/Modal";
import ModalBody from "react-bootstrap/ModalBody";
import ModalHeader from "react-bootstrap/ModalHeader";
import ModalFooter from "react-bootstrap/ModalFooter";
import ModalTitle from "react-bootstrap/ModalTitle";

interface MyModalProps {
    title: string;
    button_text: string;
    children?: React.ReactNode;
    size?: "sm" | "lg" | "xl" | undefined;
}

const MyModal = ({
    title,
    button_text,
    children,
    size = "sm",
}: MyModalProps) => {
    const [show, setShow] = useState(false);

    return (
        <>
            <button
                className="btn btn-primary p-2"
                onClick={() => {
                    setShow(!show);
                }}
            >
                {button_text}
            </button>
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
                </ModalHeader>

                <ModalBody>{children}</ModalBody>

                <ModalFooter>
                    <button
                        className="btn btn-primary"
                        onClick={() => {
                            setShow(false);
                        }}
                    >
                        Close
                    </button>
                </ModalFooter>
            </Modal>
        </>
    );
};

export default MyModal;
