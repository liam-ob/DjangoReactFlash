interface ButtonProps {
    text: string;
    colour?: "primary" | "secondary" | "success" | "danger" | "warning" | "info" | "light" | "dark";
    type?: "button" | "submit" | "reset";
    onClick?: () => void;
    disabled?: boolean;
}

const Button = ({ text, colour = "primary", onClick = () => {}, type = "button", disabled = false }: ButtonProps) => {
    return (
        <button type={type} className={"btn nowrap btn-" + colour} onClick={onClick} disabled={disabled}>
            {text}
        </button>
    );
};

export default Button;
