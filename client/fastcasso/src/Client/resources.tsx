// import axios
import axios from 'axios';
// import 
const base = process.env.REACT_APP_API_ENDPOINT;
const homeImageMaxCount = 1000;
const homeImagePageSize = 10;
const root = '';

//base search without advanced parameters
//returns promise of image results
export function SearchImages(query: string, page:number = 0, limit: number = 1000) : Promise<ImageStubCollection> {
    const encodedQuery = encodeURIComponent(query);
    const lowerIndex = page * homeImagePageSize;
    const upperIndex = lowerIndex + homeImagePageSize - 1;
    const wrappedImages = new Promise<ImageStubCollection>((resolve, reject) => {
        const images = axios.get(`${root}/image/search/${encodedQuery}`);
        images.then(
            (response: any) => {
                resolve({images: response.data.slice(lowerIndex, upperIndex), count: response.data.length});
            }
        ).catch(
            (error:any) => {
                reject(error);
            }
        )
    });
    return wrappedImages;
}

export function GetHomeImages(page: number) : Promise<ImageStubCollection> {
    const query = ' ';
    return SearchImages(query, page, homeImageMaxCount);
}

export function GetImageById(id: string) {
   return axios.get(`${root}/image/${id}`, {
    responseType: 'arraybuffer'
   });
}

export function GetImagesByIds(ids: number[]) {
    return axios.post(`${root}/image/multiple`, {ids: ids}, {responseType: 'arraybuffer'});
}

export function GenerateImage(request: GenerateRequest){
    const encodedPrompt = encodeURIComponent(request.prompt);
    const encodedName = encodeURIComponent(request.name);
    const encodedNegative = encodeURIComponent(request.negative_prompt);
    return axios.get(`${root}/image/generate/${encodedPrompt}/${encodedName}?preset_id=${request.preset_id}&height=${request.height}&width=${request.width}&negative_prompt=${encodedNegative}`, {
        responseType: 'arraybuffer'
    });
}

export function GenerateTransform(request: GenerateTransformRequest)
{
    const encodedPrompt = encodeURIComponent(request.prompt);
    const encodedName = encodeURIComponent(request.name);
    const url = `${root}/image/generate/transform/${encodedPrompt}/${encodedName}/${request.image_id.toString()}`;
    return axios.get(url, {
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

export interface ImageStubCollection {
    images: Array<ImageStub>;
    count: number;
}

export interface GenerateRequest {
    prompt: string;
    name: string;
    preset_id: number;
    negative_prompt: string;
    height: number;
    width: number;
}

export interface GenerateTransformRequest {
    prompt: string;
    name: string;
    transform_type: string;
    image_id: number;
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