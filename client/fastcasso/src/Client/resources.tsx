// import axios
import axios from 'axios';
// import 
const { API_ENDPOINT } = process.env;
const base = API_ENDPOINT

export function search_images(query: string) {
    return axios.get(`${base}/search/${query}`);
}