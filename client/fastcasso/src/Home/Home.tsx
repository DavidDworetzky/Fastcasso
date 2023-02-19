import {TileProperties} from '../Components/Tile/Tile';
import Tile from '../Components/Tile/Tile';
import TileGrid from '../Components/Tile/TileGrid';
import {TileGridProperties} from '../Components/Tile/TileGrid';
import {TileData} from '../Components/Tile/Tile';
import BlackSquare from '../black_square.jpg'
import {GetHomeImages, GetImageById, GetImagesByIds} from '../Client/resources';
import React from 'react';
import { useEffect } from 'react';
import { Buffer } from 'buffer';
import * as JSZip from 'jszip';

function Home(){
    const mockTiles = [
      new TileData(BlackSquare, 'test', 400, 400, false),
      new TileData(BlackSquare, 'test', 400, 400, false),
      new TileData(BlackSquare, 'test', 400, 400, false),
      new TileData(BlackSquare, 'test', 400, 400, false),
      new TileData(BlackSquare, 'test', 400, 400, false),
      new TileData(BlackSquare, 'test', 400, 400, false)] as TileProperties[];
    const tileDimension = 400;
    //set state hook of tile data
    const [tileData, setTileData] = React.useState<TileProperties[]>(mockTiles);

    //initial load of home images
    useEffect(() => {
    //get home images
    const homeImages = GetHomeImages();
    //get image contents from image stubs
    homeImages.then((result) => {
      let imageStubs = [] as Array<any>;
      //push image stubs from homeImages
      for(let i = 0; i < result.length; i++){
        imageStubs.push(result[i]);
      }
      //get image contents for all stubs
      const imageZip = GetImagesByIds(imageStubs.map((ele) => ele.id));

      imageZip.then((result) => {
        const imageFiles = new Array<Promise<any>>();
        JSZip.loadAsync(result.data)
        .then(function(zip) {
            for(let j = 0; j < imageStubs.length; j++){
              console.log(zip);
              imageFiles.push(zip.file(`${imageStubs[j].id}.png`)?.async("base64") ?? Promise.resolve(null));
            }
            Promise.all(imageFiles).then((resultFiles) => {
              let counter = 0;
              const tileData = resultFiles.map((ele) => {
                const selectedStub = imageStubs[counter];
                counter++;
                const base64 = ele;
                return new TileData(base64, selectedStub.id, tileDimension, tileDimension);
              });
              setTileData(tileData);
            });
          });
      });
    });
  }, []);
    const tileGridProperties = {tiles: tileData};

    return <TileGrid {...tileGridProperties} />
    
}

export default Home;