import React from "react";
import { useEffect } from "react";
import { useState } from "react";

const maxPages = 10;

export default function PaginationBar(props: PaginationProperties) {
    const pageCount = Math.ceil(props.elementCount / props.pageSize);
    const [currentPage, setCurrentPage] = useState(0);

    const previousClick = () => {
        if (currentPage > 0) {
            setCurrentPage(currentPage - 1);
            props.onPageChange(currentPage - 1);
        }
    }

    const nextClick = () => {
        if (currentPage < pageCount - 1) {
            setCurrentPage(currentPage + 1);
            props.onPageChange(currentPage + 1);
        }
    }

    let pages = [];
    for (let i = 0; i < pageCount; i++) {
        const onClick = () => {
            setCurrentPage(i);
            props.onPageChange(i);
        }
        pages.push((                
        <li>
            <a href="#" onClick={onClick} className="px-3 py-2 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">{i + 1}</a>
        </li>));
    }
    const filteredPages = pages.slice(0, maxPages);

    return (
        <nav aria-label="PaginationBar">
            <ul className="inline-flex -space-x-px">
                <li>
                    <a href="#" onClick={previousClick} className="px-3 py-2 ml-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-l-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">Previous</a>
                </li>
                {filteredPages}
                <li>
                    <a href="#" onClick={nextClick} className="px-3 py-2 leading-tight text-gray-500 bg-white border border-gray-300 rounded-r-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">Next</a>
                </li>
            </ul>
        </nav>
    )
}

export interface PaginationProperties {
    elementCount: number;
    pageSize: number;
    onPageChange: any;
}