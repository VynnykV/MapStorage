// ** MUI Imports
import * as React from "react";
import {useEffect} from "react";
import GoogleMapComponent from "../../views/components/GoogleMapComponent";
import GoogleMapModeComponent from "../../views/components/GoogleMapModeComponent";
import Box from "@mui/material/Box";
import {IMPORT_MODES} from "../../constants/ImportModes";
import DialogImportMap from "../../views/dialogs/DialogImportMap";
import {
  Coordinates,
  FASTAction,
  ImportActions,
  ImportMapLayerCommand,
  ImportProfileType,
  PolylineProfileArgs,
  RectangleProfileArgs
} from "../../api/models/ImportMapLayer";
import MapLayerService from "../../api/services/MapLayerService";
import {useNotification} from "../../context/NotificationContext";
import OptimizeRouteService from "../../api/services/OptimizeRouteService";
import {AntColonyOptimization} from "../../api/models/AntColonyOptimization";
import {useSearchParams} from "next/navigation";
import GoogleMapCoordinateInputComponent from "../../views/components/GoogleMapCoordinateInputComponent";
import {useRouter} from "next/router";

const Map = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const mapLayerId = searchParams.get('mapLayerId');
  const [isReadonly, setIsReadonly] = React.useState(mapLayerId !== null);
  const [map, setMap] = React.useState<google.maps.Map>();
  const [clicks, setClicks] = React.useState<google.maps.LatLng[]>([]);
  const [zoom, setZoom] = React.useState(6); // initial zoom
  const [center, setCenter] = React.useState<google.maps.LatLngLiteral>({
    lat: 49.0275,
    lng: 31.4828
  });
  const [lastCoordinates, setLastCoordinates] = React.useState<google.maps.LatLngLiteral | null>(null);
  const [importMode, setImportMode] = React.useState(IMPORT_MODES.RECTANGLE);
  const [showImportMapDialog, setShowImportMapDialog] = React.useState<boolean>(false);
  const { showNotification } = useNotification();
  const [rectangle, setRectangle] = React.useState<google.maps.Rectangle | null>(null);
  const [polyline, setPolyline] = React.useState<google.maps.Polyline | null>(null);
  const [tiles, setTiles] = React.useState<google.maps.Rectangle[] | null>(null);

  const handleSearchCoordinatesAction = (coordinates: google.maps.LatLngLiteral | null) => {
    setCenter(coordinates!);
    setZoom(15)
  }

  const handleInsertCoordinatesAction = (coordinates: google.maps.LatLngLiteral | null) => {
    if (!coordinates) return;

    const latLng = new google.maps.LatLng(coordinates.lat, coordinates.lng);
    const isDuplicate = clicks.some(point => point.lat() === latLng.lat() && point.lng() === latLng.lng());

    if (!isDuplicate) {
      if (importMode === IMPORT_MODES.RECTANGLE && clicks.length < 2) {
        setClicks([...clicks, latLng]);
        setLastCoordinates(coordinates);
      } else if (importMode === IMPORT_MODES.POLYLINE) {
        setClicks([...clicks, latLng]);
        setLastCoordinates(coordinates);
      }
    }
  }



  const handleMapModeImportButton = () => {
    setShowImportMapDialog(true);
  }

  const handleMapModeClearCoordinatesButton = () => {
    setClicks([]);
    setLastCoordinates(null);

    if (rectangle) {
      rectangle.setMap(null);
      setRectangle(null);
    }

    if (polyline) {
      polyline.setMap(null);
      setPolyline(null);
    }
  }

  const handleMapModePreviewButton = () => {
    switch (importMode) {
      case IMPORT_MODES.RECTANGLE:
        showRectanglePreview();
        break;
      case IMPORT_MODES.POLYLINE:
        showPolylinePreview(clicks);
        break;
    }
  }

  const handleOptimizeButton = () => {
    showOptimizedPolyline(clicks);
  }

  const showOptimizedPolyline = (clicks: google.maps.LatLng[]) => {
    const requestBody = {
      polyline_points: clicks.map(click => ({
        latitude: click.lat(),
        longitude: click.lng()
      }))
    } as AntColonyOptimization

    console.log(requestBody.polyline_points)

    OptimizeRouteService.antColony(requestBody)
      .then((response) => {
        console.log(response.data)
        const updatedClicks = response.data.map(coord => new google.maps.LatLng(coord.latitude, coord.longitude));
        setClicks(updatedClicks);
        showPolylinePreview(updatedClicks);
      })
  }

  const handleImportMapButton = (data: any) => {
    let requestBody: ImportMapLayerCommand;
    switch (importMode) {
      case IMPORT_MODES.RECTANGLE:
        requestBody = getRectangleRequestBody(data);
        break;
      case IMPORT_MODES.POLYLINE:
        requestBody = getPolylineRequestBody(data);
        console.log(requestBody)
        break;
    }

    showNotification({
      message: 'Start importing map...',
      severity: 'info',
      position: { horizontal: "right", vertical: "top" }
    });
    MapLayerService.import(requestBody!)
      .then((response) => {
        router.push({
          pathname: '/map',
          query: { mapLayerId: response.data.id },
        }).then(() => {
          showNotification({
            message: 'Map imported successfully!',
            severity: 'success',
            position: { horizontal: "right", vertical: "top" }
          });
        });
      })
      .catch((error) => {
        showNotification({
          message: 'Error importing map!',
          severity: 'error',
          position: { horizontal: "right", vertical: "top" }
        });
        console.error("There was an error importing map", error);
      });
  }

  const getPolylineRequestBody = (formData: any) => {
    return {
      import_profile_type: ImportProfileType.POLYLINE,
      import_profile_args: {
        waypoints: clicks.map(click => ({
          latitude: click.lat(),
          longitude: click.lng()
        })),
        load_distance_m: formData.loadDistanceM
      } as PolylineProfileArgs,
      layer_name: formData.layerName,
      zoom_lvl: formData.zoomLevel,
      actions: {
        compute_fast: {
          threshold: formData.threshold,
          nonmaxSuppression: formData.nonmaxSuppression
        } as FASTAction
      } as ImportActions
    } as ImportMapLayerCommand
  }

  const getRectangleRequestBody = (formData: any) => {
    return {
      import_profile_type: ImportProfileType.RECTANGLE,
      import_profile_args: {
        start: {
          latitude: clicks[0].lat(),
          longitude: clicks[0].lng()
        } as Coordinates,
        end: {
          latitude: clicks[1].lat(),
          longitude: clicks[1].lng()
        } as Coordinates
      } as RectangleProfileArgs,
      layer_name: formData.layerName,
      zoom_lvl: formData.zoomLevel,
      actions: {
        compute_fast: {
          threshold: formData.threshold,
          nonmaxSuppression: formData.nonmaxSuppression
        } as FASTAction
      } as ImportActions
    } as ImportMapLayerCommand;
  }

  const showRectanglePreview = () => {
    // Видалення існуючого прямокутника, якщо він існує
    if (rectangle) {
      rectangle.setMap(null);
    }

    if (clicks.length >= 2) {
      const bounds = {
        north: Math.max(clicks[0].lat(), clicks[1].lat()),
        south: Math.min(clicks[0].lat(), clicks[1].lat()),
        east: Math.max(clicks[0].lng(), clicks[1].lng()),
        west: Math.min(clicks[0].lng(), clicks[1].lng()),
      };

      const newRectangle = new google.maps.Rectangle({
        bounds: bounds,
        strokeColor: "#FF0000",
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: "#FF0000",
        fillOpacity: 0.35,
      });

      newRectangle.setMap(map!);
      setRectangle(newRectangle);
    }
  };

  const showPolylinePreview = (clicks: google.maps.LatLng[]) => {
    // Видаляємо існуючу лінію, якщо вона існує
    if (polyline) {
      polyline.setMap(null);
    }

    // Створюємо лінію лише якщо є дві або більше точок
    if (clicks.length >= 2) {
      const polylinePath = clicks.map(click => ({
        lat: click.lat(),
        lng: click.lng(),
      }));

      const newPolyline = new google.maps.Polyline({
        path: polylinePath,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
      });

      // Вікно для відображення відстані
      const infoWindow = new google.maps.InfoWindow();

      // Додаємо слухача подій при наведенні миші на полілінію
      newPolyline.addListener('mouseover', (e) => {
        const path = newPolyline.getPath().getArray();
        const distanceInMeters = google.maps.geometry.spherical.computeLength(path);
        const distanceText = (distanceInMeters / 1000).toFixed(2) + ' km';
        const contentString = `<div style="color: black; font-weight: bold;">Відстань: ${distanceText}</div>`;
        infoWindow.setContent(contentString);
        infoWindow.setPosition(e.latLng);
        infoWindow.open(map);
      });

      // Закриваємо InfoWindow при відведенні миші
      newPolyline.addListener('mouseout', () => {
        infoWindow.close();
      });

      newPolyline.setMap(map!); // Впевніться, що map вже ініціалізована
      setPolyline(newPolyline);
    }
  };



  const displayMapLayerTiles = (data) => {
    // Очистка старих плиток
    tiles?.forEach(tile => tile.setMap(null));

    const newTiles = data.map(tile => {
      const rectangle = new google.maps.Rectangle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: map,
        bounds: {
          north: tile.nw_lat,
          south: tile.se_lat,
          east: tile.ne_long,
          west: tile.sw_long,
        }
      });

      // Створення InfoWindow
      const infoWindowContent = `
      <div style="color: black; font-weight: bold;">
        center_lat: ${tile.center_lat.toFixed(5)}<br>
        center_long: ${tile.center_long.toFixed(5)}
      </div>`;

      const infoWindow = new google.maps.InfoWindow({
        content: infoWindowContent,
        position: new google.maps.LatLng(tile.center_lat, tile.center_long)
      });

      // Додавання події mouseover для відкриття InfoWindow
      rectangle.addListener('mouseover', () => {
        infoWindow.open(map);
      });

      // Додавання події mouseout для закриття InfoWindow
      rectangle.addListener('mouseout', () => {
        infoWindow.close();
      });

      return rectangle;
    });

    setTiles(newTiles);
  }

  useEffect(() => {
    if (mapLayerId) {
      MapLayerService.mapLayerDetails(parseInt(mapLayerId))
        .then(response => {
          if (map) {
            resetToDefault();
            displayMapLayerTiles(response.data.tiles);
            setCenter(calculateTilesCenter(response.data.tiles));
            const importMode = response.data.import_type === 'rectangle' ? IMPORT_MODES.RECTANGLE : IMPORT_MODES.POLYLINE;
            setImportMode(importMode);
            setZoom(14);
          }
        })
        .catch(error => {
          console.error("Error fetching map layer tiles", error);
          showNotification({
            message: 'Error fetching map layer tiles!',
            severity: 'error',
            position: { horizontal: "right", vertical: "top" }
          });
        });
    }
  }, [map, mapLayerId]);

  useEffect(() => {
    resetToDefault();
  }, [mapLayerId]);

  const resetToDefault = () => {
    setIsReadonly(mapLayerId !== null);
    setClicks([]);
    setZoom(6);
    setCenter({
      lat: 49.0275,
      lng: 31.4828
    });
    setLastCoordinates(null);
    setImportMode(IMPORT_MODES.RECTANGLE);
    rectangle?.setMap(null);
    polyline?.setMap(null);
    tiles?.forEach(tile => tile.setMap(null));
  }

  const calculateTilesCenter = (tiles) => {
    let totalLat = 0;
    let totalLong = 0;
    const count = tiles.length;

    tiles.forEach(tile => {
      totalLat += tile.center_lat;
      totalLong += tile.center_long;
    });

    return {
      lat: totalLat / count,
      lng: totalLong / count
    };
  }


  return (
    <Box sx={{ display: 'flex', height: '100%' }}>
      <Box sx={{ width: '70%', height: '100%', mr: 5, position: 'relative' }}>
        <GoogleMapComponent
          clicks={clicks}
          setClicks={setClicks}
          zoom={zoom}
          setZoom={setZoom}
          center={center}
          setCenter={setCenter}
          setLastCoordinates={setLastCoordinates}
          importMode={importMode}
          onMapLoad={setMap}
          isReadonly={isReadonly}
        />
        {!isReadonly && (
          <GoogleMapCoordinateInputComponent
            handleInsertAction={handleInsertCoordinatesAction}
            handleSearchAction={handleSearchCoordinatesAction}
          />
        )}
      </Box>
      <Box sx={{ width: '30%', height: '100%' }}>
        <GoogleMapModeComponent
          zoom={zoom}
          setZoom={setZoom}
          clicks={clicks}
          setClicks={setClicks}
          lastCoordinates={lastCoordinates}
          importMode={importMode}
          setImportMode={setImportMode}
          handleImportButton={handleMapModeImportButton}
          handlePreviewButton={handleMapModePreviewButton}
          handleOptimizeButton={handleOptimizeButton}
          handleClearCoordinatesButton={handleMapModeClearCoordinatesButton}
          isReadonly={isReadonly}
        />
      </Box>
      {showImportMapDialog && <DialogImportMap handleImportButton={handleImportMapButton} importMode={importMode} show={showImportMapDialog} setShow={setShowImportMapDialog} />}
    </Box>
  )
}

export default Map
