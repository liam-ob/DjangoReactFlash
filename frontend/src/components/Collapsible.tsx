import React, { useState, useRef, useEffect } from "react";
import { BsCaretDownSquareFill, BsFillCaretUpSquareFill } from "react-icons/bs";
interface CollapsibleProps {
    open?: boolean;
    text: string;
    children: React.ReactNode;
}

const Collapsible: React.FC<CollapsibleProps> = ({
    open = false,
    children,
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
            <div className="">
                <div>
                    <button
                        type="button"
                        className="btn btn-primary"
                        onClick={handleFilterOpening}
                    >
                        <span>{text} </span>
                        {!isOpen ? (
                            <BsCaretDownSquareFill />
                        ) : (
                            <BsFillCaretUpSquareFill />
                        )}
                    </button>
                </div>
                <div className="my-collapsible" style={{ height }}>
                    <div ref={heightRef}>
                        {isOpen && (
                            <div className="card card-body">{children}</div>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
};

export default Collapsible;
