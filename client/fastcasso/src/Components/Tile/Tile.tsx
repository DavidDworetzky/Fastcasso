import { useLocation, Link } from 'react-router-dom'

/*tile component. Given base 64 image data, it will render the image. */
function Tile(props: TileProperties) {
    // format our new transform path
    const location = useLocation();
    const currentPath = location.pathname;
    const baseURL = currentPath.substring(0, currentPath.lastIndexOf('/'));

    // Construct the new path with the desired parameters
    const newPath = `${baseURL}/transform?image_id=${props.image_id}`;
    const imageSource = props.isBase64 ? `data:image/png;base64,${props.image}` : props.image;

    //create relative link to transform route if image_id exists using react-router

    if (props.image_id) {
        return (
                <Link to={newPath}>
                    <img style={{ width: props.width ?? '400px', height: props.height ?? '400px' }} src={imageSource} alt={props.alt}></img>
                </Link>
        );
    }
    else
    {
        return (
            <img style={{ width: props.width ?? '400px', height: props.height ?? '400px' }} src={imageSource} alt={props.alt}/>
        )
    }

}

/* props */
export interface TileProperties {
    image: string;
    alt?: string;
    width?: number;
    height?: number;
    isBase64: boolean;
    image_id?: number;
}

export class TileData implements TileProperties {
    constructor(image: string, alt?: string, width?: number, height?: number, isBase64?: boolean, image_id?: number) {
        this.image = image;
        this.alt = alt;
        this.width = width;
        this.height = height;
        this.isBase64 = isBase64 ?? true;
        this.image_id = image_id;
    }
    image: string;
    alt?: string;
    width?: number;
    height?: number;
    isBase64: boolean;
    image_id?: number;

}

export default Tile;