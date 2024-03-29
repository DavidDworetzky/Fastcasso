import React from "react";

export default function SearchBar(props: SearchBarProperties) {
    return (
        <div className="flex items-center">
            <div className="flex space-x-1">
                <input
                    onKeyDown={props.onKeyDown}
                    onChange={props.onChange}
                    type="text"
                    className="block w-full px-4 py-2 text-purple-700 bg-white border rounded-full focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40"
                    placeholder="Search..."
                />
                <button className="px-4 text-white white rounded-full w-8 " onClick={props.onClick}>
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="w-5 h-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="purple"
                        strokeWidth={2}
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                        />
                    </svg>
                </button>
            </div>
        </div>
    );
}

export interface SearchBarProperties {
    onChange: any;
    onClick: any;
    onKeyDown?: any;
}