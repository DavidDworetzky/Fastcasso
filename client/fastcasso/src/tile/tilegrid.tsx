import {TileProperties} from './Tile';
import Tile from './Tile';
function TileGrid(props: TileProperties[]){
    return (
        /*flex container around tiles*/
        <div className="Container">
            {props.map((ele) => {
                return <Tile {...ele}/>
            })}
        </div>
    );
}

export default TileGrid;