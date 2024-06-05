import axios from 'axios';
import {ImportMapLayerCommand} from "../models/ImportMapLayer";

const MAP_LAYERS_API_BASE_URL = process.env.NEXT_PUBLIC_HUB_API_URL + '/mapLayers';

class MapLayerService {
  mapLayerDetails(id: number) {
    return axios.get(MAP_LAYERS_API_BASE_URL + `/${id}`)
  }

  listMapLayers() {
    return axios.get(MAP_LAYERS_API_BASE_URL);
  }

  import(data: ImportMapLayerCommand){
    return axios.post(MAP_LAYERS_API_BASE_URL + '/import', data);
  }

  deleteMapLayer(id: number) {
    return axios.delete(MAP_LAYERS_API_BASE_URL + `/${id}`)
  }
}

export default new MapLayerService()
