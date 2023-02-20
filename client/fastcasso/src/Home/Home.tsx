import {TileProperties} from '../Components/Tile/Tile';
import TileGrid from '../Components/Tile/TileGrid';
import {TileData} from '../Components/Tile/Tile';
import BlackSquare from '../black_square.jpg'
import {GetHomeImages, GetImageById, GetImagesByIds} from '../Client/resources';
import React from 'react';
import { useEffect } from 'react';
import * as JSZip from 'jszip';
import PaginationBar from '../Components/Search/Pagination';

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
    const [elements, setElements] = React.useState<number>(10);

    const loadImages = (page: number) => {
    //get home images
    const homeImages = GetHomeImages(page);
    //get image contents from image stubs
    homeImages.then((result) => {
      let imageStubs = [] as Array<any>;
      setElements(result.count);
      //push image stubs from homeImages
      for(let i = 0; i < result.images.length; i++){
        imageStubs.push(result.images[i]);
      }
      //get image contents for all stubs
      const imageZip = GetImagesByIds(imageStubs.map((ele) => ele.id));

      imageZip.then((result) => {
        const imageFiles = new Array<Promise<any>>();
        JSZip.loadAsync(result.data)
        .then(function(zip) {
            for(let j = 0; j < imageStubs.length; j++){
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
    }
    //initial load of home images
    useEffect(() => {
      loadImages(0);
  }, []);
  const onPageChange = (page: number) => {
    loadImages(page);
  }
    const tileGridProperties = {tiles: tileData};
    const paginationProperties = {elementCount: elements, pageSize: 10, onPageChange : onPageChange};

    return <React.Fragment>
            <TileGrid {...tileGridProperties} />
            <PaginationBar {...paginationProperties}/>
           </React.Fragment>
    
}

export default Home;