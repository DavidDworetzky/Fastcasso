import { TileProperties } from '../Components/Tile/Tile';
import Tile from '../Components/Tile/Tile';
import TileGrid from '../Components/Tile/TileGrid';
import { TileGridProperties } from '../Components/Tile/TileGrid';
import { TileData } from '../Components/Tile/Tile';
import BlackSquare from '../black_square.jpg'
import { GetHomeImages, GetImageById } from '../Client/resources';
import React from 'react';
import { useEffect } from 'react';
import { Buffer } from 'buffer';
import { GetPresets, Preset } from '../Client/resources';
import Select from '../Components/Form/Select';
import { Option } from '../Components/Form/Select';
import { GenerateRequest } from '../Client/resources';
import { GenerateImage } from '../Client/resources';

function Generate() {
    const tileDimension = 512;
    const mockTile = new TileData(BlackSquare, 'test', tileDimension, tileDimension, false)

    const [tileData, setTileData] = React.useState<TileData>(mockTile);
    const [presets, setPresetData] = React.useState<Preset[]>([] as Preset[]);
    const [generateData, setGenerateData] = React.useState<GenerateRequest>(
    { 
        prompt: "", 
        preset_id: 0, 
        name: "", 
        height: 512, 
        width: 512, 
        negative_prompt: "" 
    });

    const onElementChange = (event: any) => {
        const numbers = ['width', 'height']
        const id = event.target.id;
        const value = !numbers.includes(id) ? event.target.value : parseInt(event.target.value);
        setGenerateData({ ...generateData, [id]: value });
    }

    const onPresetChange = (event: any) => {
        setGenerateData({ ...generateData, preset_id: parseInt(event.target.value) });
    }

    const onGenerate = () => {
        GenerateImage(generateData).then((result) => {
            const base64 = Buffer.from(result.data, 'binary').toString('base64')
            setTileData(new TileData(base64, 'result', tileDimension, tileDimension));
        });
    }

    useEffect(() => {
        //retrieve presets
        GetPresets().then((result) => {
            setPresetData(result);
        });
    }, []);
    const options = presets.map((preset) => { return { name: `${preset.preset_id}${preset.model_id}`, value: `${preset.preset_id}` } }) as Option[];
    const selectProperties = { id: "preset", name: "preset", options: options, onChange: onPresetChange };


    return <React.Fragment>
        <div className="w-full max-w-xs">
            <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Prompt
                    </label>
                    <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="prompt" type="text" placeholder="magic!" onChange={onElementChange} />
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Name
                    </label>
                    <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="name" type="text" placeholder="name" onChange={onElementChange} />
                </div>
                <div className="mb-6">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Negative Prompt
                    </label>
                    <input className="shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" id="negative_prompt" type="text" onChange={onElementChange} placeholder="ugly, distorted, bad anatomy, extra hands, extra feet, extra limbs" />
                </div>
                <Select {...selectProperties} />
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Height
                    </label>
                    <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="height" type="text" onChange={onElementChange} placeholder="height" />
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">
                        Width
                    </label>
                    <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="width" onChange={onElementChange} type="text" placeholder="width" />
                </div>
                <div className="flex items-center justify-between">
                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" onClick={onGenerate}>
                        Generate
                    </button>
                </div>
            </form>
        </div>

        <div className="w-full">
            <Tile {...tileData} />
            <p className="text-center text-gray-500 text-xs">
                &copy;2023 Fastcasso. All rights reserved.
            </p>
        </div>


    </React.Fragment>

}

export default Generate;