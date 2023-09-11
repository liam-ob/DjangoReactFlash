interface ButtonProps {
    text: string;
    colour?:
        | "primary"
        | "secondary"
        | "success"
        | "danger"
        | "warning"
        | "info"
        | "light"
        | "dark";
    onClick: () => void;
}

const Button = ({ text, colour = "primary", onClick }: ButtonProps) => {
    return (
        <button type="button" className={"btn btn-" + colour} onClick={onClick}>
            {text}
        </button>
    );
};

export default Button;
