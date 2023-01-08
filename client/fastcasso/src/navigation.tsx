function Navigation(props: NavigationProps): JSX.Element {
    const innerElements = props.navigationElements.map(ele => {
        return (
            <li className="relative">
            <a href={ele.link} className="flex items-center text-sm py-4 px-6 h-12 overflow-hidden text-gray-700 text-ellipsis whitespace-nowrap rounded hover:text-gray-900 hover:bg-gray-100 transition duration-300 ease-in-out" data-mdb-ripple="true" data-mdb-ripple-color="dark">
                <svg aria-hidden="true" focusable="false" data-prefix="fas" className="w-3 h-3 mr-3" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                <path fill="currentColor" d={ele.svg}></path>
                </svg>
                <span>{ele.name}</span>
            </a>
            </li>
        )
    })
    return (
        <div className="w-60 h-full shadow-md bg-white px-1 absolute">
    <ul className="relative">
        {innerElements}
    </ul>
    </div>)
}

interface NavigationProps {
    navigationElements: NavigationElement[];
}

interface NavigationElement {
    name: string;
    link: string;
    svg: string;
}

export default Navigation