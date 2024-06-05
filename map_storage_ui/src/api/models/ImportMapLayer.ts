import { Coordinates } from "./shared/Coordinates";

enum ImportProfileType {
  POLYLINE = 'polyline',
  RECTANGLE = 'rectangle',
}

interface RectangleProfileArgs {
  start: Coordinates;
  end: Coordinates;
}

interface PolylineProfileArgs {
  waypoints: Coordinates[];
  load_distance_m: number;
}

interface SURFAction {
  hessianThreshold: number;
}

interface FASTAction {
  threshold: number;
  nonmaxSuppression: boolean;
  type?: number;
}

interface ImportActions {
  save_img: boolean;
  compute_surf?: SURFAction;
  compute_fast?: FASTAction;
}

interface ImportMapLayerCommand {
  import_profile_type: ImportProfileType;
  import_profile_args: PolylineProfileArgs | RectangleProfileArgs;
  layer_name: string;
  zoom_lvl: number;
  actions: ImportActions;
  description?: string;
}

export {ImportProfileType}
export type {Coordinates, ImportMapLayerCommand, PolylineProfileArgs, RectangleProfileArgs, ImportActions, FASTAction}
