import React from "react";

export default function Select(props: SelectProperties) {
    const options = props.options.map((option) => {return (
            <option value={option.value}>{option.name}</option>
    )});
    return (
        <select name={props.name} id={props.id} onChange={props.onChange}>
            {options}
        </select>
    );
}

export interface Option {
    name: string;
    value: string;
}

export interface SelectProperties {
    options: Option[];
    name: string;
    id: string;
    onChange: any;
}