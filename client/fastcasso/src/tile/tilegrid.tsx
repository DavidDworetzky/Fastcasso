import {TileProperties} from './tile';
import Tile from './tile';
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