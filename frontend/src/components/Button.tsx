interface ButtonProps {
    text: string;
    colour?: "primary" | "secondary" | "success" | "danger" | "warning" | "info" | "light" | "dark";
    type?: "button" | "submit" | "reset";
    onClick?: () => void;
    disabled?: boolean;
    size?: "sm" | "md" | "lg";
}

const Button = ({ text, colour = "primary", onClick = () => {}, type = "button", disabled = false, size = "md" }: ButtonProps) => {
    return (
        <button type={type} className={"btn nowrap btn-" + colour + " btn-" + size} onClick={onClick} disabled={disabled}>
            {text}
        </button>
    );
};

export default Button;
