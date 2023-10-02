import React, { useState, useRef, useEffect } from "react";
import { BsCaretDownSquareFill, BsFillCaretUpSquareFill } from "react-icons/bs";
interface CollapsibleProps {
    open?: boolean;
    text: string;
    color?:
        | "primary"
        | "secondary"
        | "success"
        | "danger"
        | "warning"
        | "info"
        | "light"
        | "dark";
    children: React.ReactNode;
}

const Collapsible: React.FC<CollapsibleProps> = ({
    open = false,
    children,
    color = "primary",
    text,
}) => {
    const [isOpen, setIsOpen] = useState(open);

    const handleFilterOpening = () => {
        setIsOpen((prev) => !prev);
    };

    const [height, setHeight] = useState<number | undefined>(
        open ? undefined : 0
    );
    const heightRef = useRef<HTMLDivElement>(null);
    useEffect(() => {
        if (!height || !isOpen || !heightRef.current) return undefined;
        const resizeObserver = new ResizeObserver((el) => {
            setHeight(el[0].contentRect.height);
        });
        resizeObserver.observe(heightRef.current);
        return () => {
            resizeObserver.disconnect();
        };
    }, [height, isOpen]);

    useEffect(() => {
        if (isOpen)
            setHeight(heightRef.current?.getBoundingClientRect().height);
        else setHeight(0);
    }, [isOpen]);

    return (
        <>
            <div>
                <button
                    type="button"
                    className={"btn btn-" + color}
                    onClick={handleFilterOpening}
                >
                    <span className="pe-3">{text}</span>
                    <span>
                        {!isOpen ? (
                            <BsCaretDownSquareFill />
                        ) : (
                            <BsFillCaretUpSquareFill />
                        )}
                    </span>
                </button>
            </div>
            <div className="my-collapsible" style={{ height }}>
                <div ref={heightRef}>
                    {isOpen && <div className="">{children}</div>}
                </div>
            </div>
        </>
    );
};

export default Collapsible;
