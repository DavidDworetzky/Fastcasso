// import axios
import axios from 'axios';
// import 
const { API_ENDPOINT } = process.env;
const base = API_ENDPOINT

//base search without advanced parameters
export function search_images(query: string) {
    const encodedQuery = encodeURIComponent(query);
    return axios.get(`${base}/search/${encodedQuery}`);
}