// import axios
import axios from 'axios';
// import 
const base = process.env.REACT_APP_API_ENDPOINT;
const homeImageCount = 10;
const root = '';

console.log(process.env);
console.log(base);

//base search without advanced parameters
//returns promise of image results
export function SearchImages(query: string, limit: number = 10) : Promise<Array<ImageStub>> {
    const encodedQuery = encodeURIComponent(query);
    const wrappedImages = new Promise<Array<ImageStub>>((resolve, reject) => {
        const images = axios.get(`${root}/image/search/${encodedQuery}`);
        images.then(
            (response: any) => {
                resolve(response.data.slice(0, limit));
            }
        ).catch(
            (error:any) => {
                reject(error);
            }
        )
    });
    return wrappedImages;
}

export function GetHomeImages() : Promise<Array<ImageStub>> {
    const query = ' ';
    return SearchImages(query, homeImageCount);
}

export function GetImageById(id: string) {
   return axios.get(`${root}/image/${id}`, {
    responseType: 'arraybuffer'
   });
}

export function GetImagesByIds(ids: string[]) {
    return axios.post(`${root}/image/multiple`, {ids: ids}, {});
}

export function GenerateImage(request: GenerateRequest){
    const encodedPrompt = encodeURIComponent(request.prompt);
    const encodedName = encodeURIComponent(request.name);
    const encodedNegative = encodeURIComponent(request.negative_prompt);
    return axios.get(`${root}/image/generate/${encodedPrompt}/${encodedName}?preset_id=${request.preset_id}&height=${request.height}&width=${request.width}&negative_prompt=${encodedNegative}`, {
        responseType: 'arraybuffer'
    });
}

export function GetPresets() : Promise<Array<Preset>> {
    const presets = new Promise<Array<Preset>>((resolve, reject) => {
        const presetPromise = axios.get(`${root}/presets`);
        presetPromise.then(
            (response: any) => {
                resolve(response.data);
            }
        ).catch(
            (error:any) => {
                reject(error);
            }
        )
    });
    return presets;
}

export interface GenerateRequest {
    prompt: string;
    name: string;
    preset_id: number;
    negative_prompt: string;
    height: number;
    width: number;
}

export interface ImageStub {
    id: string;
    prompt: string;
    name: string;
    model_id: string;
}

export interface Preset {
    preset_id: number,
    model_id: string,
    inference_steps: number,
    default_width: number,
    default_height: number,
    keywords: string,
    negative_keywords : string
}