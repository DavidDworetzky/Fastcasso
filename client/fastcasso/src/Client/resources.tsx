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

export interface ImageStub {
    id: string;
    prompt: string;
    name: string;
    model_id: string;
}