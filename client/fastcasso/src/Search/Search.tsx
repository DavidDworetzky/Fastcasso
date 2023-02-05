import { TileProperties } from '../Components/Tile/Tile';
import Tile from '../Components/Tile/Tile';
import TileGrid from '../Components/Tile/TileGrid';
import { TileGridProperties } from '../Components/Tile/TileGrid';
import { TileData } from '../Components/Tile/Tile';
import BlackSquare from '../black_square.jpg'
import { SearchImages, GetImageById } from '../Client/resources';
import React from 'react';
import { useEffect } from 'react';
import { Buffer } from 'buffer';
import SearchBar from '../Components/Search/Search';

function Home() {
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
    const [searchTerm, setSearchTerm] = React.useState<string>(' ');

    const onTermChange = (term: any) => {
        //if term is a string, do not unpack
        const unpackedTerm = typeof term === 'string' ? term : term.target.value;
        setSearchTerm(unpackedTerm);

        //get home images
        const homeImages = SearchImages(unpackedTerm);
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
                    const base64 = Buffer.from(ele.data, 'binary').toString('base64')
                    return new TileData(base64, selectedStub.id, tileDimension, tileDimension);
                });
                setTileData(tileData);
            })
        });
    }
    //load of search images
    useEffect(() => {
        onTermChange(searchTerm);
    }, []);
    const searchBarProperties = { onChange: onTermChange};
    const tileGridProperties = { tiles: tileData };

    return (
        <React.Fragment>
            <SearchBar {...searchBarProperties} />
            <TileGrid {...tileGridProperties} />
        </React.Fragment>
    )

}

export default Home;