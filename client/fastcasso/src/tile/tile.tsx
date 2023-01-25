/*tile component. Given base 64 image data, it will render the image. */
function Tile (props: TileProperties) {
    return (
        <img style={{width: props.width ?? '400px', height: props.height ?? '400px'}} src={props.image} alt={props.alt}/>
    );
}

/* props */
export interface TileProperties {
    image: string;
    alt?: string;
    width?: number;
    height?: number;
}

export class TileData implements TileProperties {
    constructor(image: string, alt?: string, width?: number, height?: number) {
        this.image = image;
        this.alt = alt;
        this.width = width;
        this.height = height;
    }
    image: string;
    alt?: string;
    width?: number;
    height?: number;

}

export default Tile;