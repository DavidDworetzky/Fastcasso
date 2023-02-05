// import axios
import axios from 'axios';
// import 
const { API_ENDPOINT } = process.env;
const base = API_ENDPOINT
const homeImageCount = 10;

//base search without advanced parameters
//returns promise of image results
export function SearchImages(query: string) {
    const encodedQuery = encodeURIComponent(query);
    return axios.get(`${base}/search/${encodedQuery}`);
}

export function GetHomeImages() : Promise<Array<ImageStub>> {
    const query = ' ';
    const wrappedHome = new Promise<Array<ImageStub>>((resolve, reject) => {
        const homeImages = SearchImages(query);
        SearchImages(query).then(
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
   return axios.get(`${base}/image/${id}`);
}

export interface ImageStub {
    id: string;
}