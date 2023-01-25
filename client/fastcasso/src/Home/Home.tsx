import {TileProperties} from '../Components/Tile/Tile';
import Tile from '../Components/Tile/Tile';
import TileGrid from '../Components/Tile/TileGrid';
import {TileGridProperties} from '../Components/Tile/TileGrid';
import {TileData} from '../Components/Tile/Tile';
import BlackSquare from '../black_square.jpg'

function Home(){
    //request basic search to construct grid

    //limit stubs to top 10 

    //create tile grid properties from stubs
    //mock tile grid
  const tiles = [
    new TileData(BlackSquare, 'test', 400, 400),
    new TileData(BlackSquare, 'test', 400, 400),
    new TileData(BlackSquare, 'test', 400, 400),
    new TileData(BlackSquare, 'test', 400, 400),
    new TileData(BlackSquare, 'test', 400, 400),
    new TileData(BlackSquare, 'test', 400, 400)] as TileProperties[];
  const tileGridProperties = {tiles: tiles};

    return <TileGrid {...tileGridProperties} />
    
}

export default Home;