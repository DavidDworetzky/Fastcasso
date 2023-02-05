/*tile component. Given base 64 image data, it will render the image. */
function Tile (props: TileProperties) {
    const imageSource = props.isBase64 ? `data:image/png;base64,${props.image}` : props.image;
    return (
        <img style={{width: props.width ?? '400px', height: props.height ?? '400px'}} src={imageSource} alt={props.alt}/>
    );
}

/* props */
export interface TileProperties {
    image: string;
    alt?: string;
    width?: number;
    height?: number;
    isBase64: boolean;
}

export class TileData implements TileProperties {
    constructor(image: string, alt?: string, width?: number, height?: number, isBase64?: boolean) {
        this.image = image;
        this.alt = alt;
        this.width = width;
        this.height = height;
        this.isBase64 = isBase64 ?? true;
    }
    image: string;
    alt?: string;
    width?: number;
    height?: number;
    isBase64: boolean;

}

export default Tile;