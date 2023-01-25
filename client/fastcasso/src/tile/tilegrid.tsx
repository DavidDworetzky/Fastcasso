import {TileProperties} from './Tile';
import Tile from './Tile';
function TileGrid(props: TileGridProperties){
    return (
        /*flex container around tiles*/
        <div className="Container">
            {props.tiles.map((ele, i) => {
                return <Tile key={i} {...ele}/>
            })}
        </div>
    );
}

export interface TileGridProperties {
    tiles: TileProperties[];
}

export default TileGrid;