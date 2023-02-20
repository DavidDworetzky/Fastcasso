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
import PaginationBar from '../Components/Search/Pagination';

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
    const [elements, setElements] = React.useState<number>(10);
    const [page, setPage] = React.useState<number>(0);

    const onSearchClick = (event: any, passedPage: number | null) => {
        const term = searchTerm;

        //get home images
        const homeImages = SearchImages(term, passedPage ?? page);
        //get image contents from image stubs
        homeImages.then((result) => {
            setElements(result.count);
            let imageStubs = [] as Array<any>;
            let promises = result.images.map((ele) => {
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
    const onTermChange = (term: any) => {
        //if term is a string, do not unpack
        const unpackedTerm = typeof term === 'string' ? term : term.target.value;
        setSearchTerm(unpackedTerm);
    }
    //load of search images
    useEffect(() => {
        onTermChange(searchTerm);
    }, []);

    const onPageChange = (page: number) => {
        setPage(page);
        onSearchClick(null, page);
    }
    const searchBarProperties = { onChange: onTermChange, onClick: onSearchClick};
    const tileGridProperties = { tiles: tileData };
    const paginationProperties = {elementCount: elements, pageSize: 10, onPageChange : onPageChange};

    return (
        <React.Fragment>
            <SearchBar {...searchBarProperties} />
            <TileGrid {...tileGridProperties} />
            <PaginationBar {...paginationProperties} />
        </React.Fragment>
    )

}

export default Home;