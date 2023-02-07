import {TileProperties} from '../Components/Tile/Tile';
import Tile from '../Components/Tile/Tile';
import TileGrid from '../Components/Tile/TileGrid';
import {TileGridProperties} from '../Components/Tile/TileGrid';
import {TileData} from '../Components/Tile/Tile';
import BlackSquare from '../black_square.jpg'
import {GetHomeImages, GetImageById} from '../Client/resources';
import React from 'react';
import { useEffect } from 'react';
import { Buffer } from 'buffer';
import { GetPresets, Preset } from '../Client/resources';
import Select from '../Components/Form/Select';
import {Option} from '../Components/Form/Select';

function Generate(){
    const tileDimension = 400;
    const mockTile = new TileData(BlackSquare, 'test', tileDimension, tileDimension, false)

    const [tileData, setTileData] = React.useState<TileData>(mockTile);
    const [presets, setPresetData] = React.useState<Preset[]>([] as Preset[]);

    const onPresetChange = (event: any) => {
        console.log(event.target.value);
    }

    useEffect(() => {
        //retrieve presets
        GetPresets().then((result) => {
            setPresetData(result);
        });
    }, []);
    const options = presets.map((preset) => {return {name: `${preset.preset_id}${preset.model_id}`, value: `${preset.preset_id}`}}) as Option[];
    const selectProperties = { id:"preset", name:"preset", options: options, onChange: onPresetChange};


    return <React.Fragment>
        <div className="w-full max-w-xs">
            <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Prompt
                    </label>
                    <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="prompt" type="text" placeholder="magic!" />
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Name
                    </label>
                    <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="name" type="text" placeholder="name" />
                </div>
                <div className="mb-6">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Negative Prompt
                    </label>
                    <input className="shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" id="negative prompt" type="text" placeholder="ugly, distorted, bad anatomy, extra hands, extra feet, extra limbs" />
                </div>
                <Select {...selectProperties}/>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Height
                    </label>
                    <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="height" type="text" placeholder="height" />
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Width
                    </label>
                    <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="width" type="text" placeholder="width" />
                </div>
                <div className="flex items-center justify-between">
                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button">
                        Generate
                    </button>
                </div>
            </form>
            <p className="text-center text-gray-500 text-xs">
                &copy;2023 Fastcasso. All rights reserved.
            </p>
        </div>


    </React.Fragment>
    
}

export default Generate;