/*tile component. Given base 64 image data, it will render the image. */
function tile (props: TileProperties) {
    return (
        <div style={{width: props.width ?? '400px', height: props.height ?? '400px'}}>
            <img src={props.image} alt={props.alt}/>
        </div>
    );
}

/* props */
export interface TileProperties {
    image: string;
    alt?: string;
    width?: number;
    height?: number;
}

export default tile;