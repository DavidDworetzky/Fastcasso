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
export function SearchImages(query: string) {
    const encodedQuery = encodeURIComponent(query);
    return axios.get(`${root}/image/search/${encodedQuery}`);
}

export function GetHomeImages() : Promise<Array<ImageStub>> {
    const query = ' ';
    const wrappedHome = new Promise<Array<ImageStub>>((resolve, reject) => {
        const homeImages = SearchImages(query);
        homeImages.then(
            (response: any) => {
                resolve(response.slice(0, homeImageCount));
            }
        ).catch(
            (error:any) => {
                reject(error);
            }
        )
    });
    return wrappedHome
}

export function GetImageById(id: string) {
   return axios.get(`${root}/image/${id}`);
}

export interface ImageStub {
    id: string;
}