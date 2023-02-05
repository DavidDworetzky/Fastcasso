import {TileProperties} from '../Components/Tile/Tile';
import Tile from '../Components/Tile/Tile';
import TileGrid from '../Components/Tile/TileGrid';
import {TileGridProperties} from '../Components/Tile/TileGrid';
import {TileData} from '../Components/Tile/Tile';
import BlackSquare from '../black_square.jpg'
import {GetHomeImages, GetImageById} from '../Client/resources';
import React from 'react';

function Home(){
    const mockTiles = [
      new TileData(BlackSquare, 'test', 400, 400),
      new TileData(BlackSquare, 'test', 400, 400),
      new TileData(BlackSquare, 'test', 400, 400),
      new TileData(BlackSquare, 'test', 400, 400),
      new TileData(BlackSquare, 'test', 400, 400),
      new TileData(BlackSquare, 'test', 400, 400)] as TileProperties[];
    const tileDimension = 400;
    //set state hook of tile data
    const [tileData, setTileData] = React.useState<TileProperties[]>(mockTiles);
    //get home images
    const homeImages = GetHomeImages();
    //get image contents from image stubs
    homeImages.then((result) => {
      let imageStubs = [] as Array<any>;
      let promises = result.map((ele) => {
        imageStubs.push(ele);
        return GetImageById(ele.id);
      });

      const imageResults = Promise.all(promises);
      imageResults.then((result) => {
        let counter = 0;
        const tileData = result.map((ele) => {
          const selectedStub = imageStubs[counter];
          counter++;
          return new TileData(ele.data, selectedStub.id, tileDimension, tileDimension);
        });
        setTileData(tileData);
      })
    });
    const tileGridProperties = {tiles: tileData};

    return <TileGrid {...tileGridProperties} />
    
}

export default Home;