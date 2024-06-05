import axios from 'axios';
import { AntColonyOptimization } from "../models/AntColonyOptimization";

const OPTIMIZE_ROUTE_API_BASE_URL = process.env.NEXT_PUBLIC_HUB_API_URL + '/optimizeRoute';

class OptimizeRouteService {
  antColony(data: AntColonyOptimization){
    return axios.post(OPTIMIZE_ROUTE_API_BASE_URL + '/antColony', data);
  }
}

export default new OptimizeRouteService()
