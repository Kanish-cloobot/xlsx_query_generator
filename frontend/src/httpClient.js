// httpClient.js
import axios from 'axios';


const PROD_BACK = 'http://20.198.93.27:5000'   //kanish ids

const httpClient = axios.create({
  baseURL: PROD_BACK 
});


export default httpClient;