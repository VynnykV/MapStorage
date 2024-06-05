import {Status, Wrapper} from "@googlemaps/react-wrapper";
import * as React from "react";
import {isLatLngLiteral} from "@googlemaps/typescript-guards";
import {createCustomEqual} from "fast-equals";
import {IMPORT_MODES} from "../../constants/ImportModes";

const render = (status: Status) => {
  return <h1>{status}</h1>;
};

interface GoogleMapComponentProps {
  clicks: google.maps.LatLng[];
  setClicks: React.Dispatch<React.SetStateAction<google.maps.LatLng[]>>;
  zoom: number;
  setZoom: React.Dispatch<React.SetStateAction<number>>;
  center: google.maps.LatLngLiteral;
  setCenter: React.Dispatch<React.SetStateAction<google.maps.LatLngLiteral>>;
  setLastCoordinates: React.Dispatch<React.SetStateAction<google.maps.LatLngLiteral | null>>;
  importMode: string;
  onMapLoad?: (map: google.maps.Map) => void;
  isReadonly: boolean;
}

const GoogleMapComponent: React.FC<GoogleMapComponentProps> =
  ({ clicks, setClicks,
     zoom, setZoom,
     center, setCenter,
     setLastCoordinates,
     importMode, onMapLoad,
    isReadonly}) => {

  const apiKey = process.env.NEXT_PUBLIC_MAPS_JAVASCRIPT_API_KEY;

  const onClick = (e: google.maps.MapMouseEvent) => {
    if (!isReadonly) {
      if (importMode === IMPORT_MODES.RECTANGLE && clicks.length < 2) {
        setClicks([...clicks, e.latLng!]);
        setLastCoordinates(e.latLng.toJSON())
      }
      if (importMode === IMPORT_MODES.POLYLINE) {
        setClicks([...clicks, e.latLng!]);
        setLastCoordinates(e.latLng.toJSON())
      }
    }
  };

  const onIdle = (m: google.maps.Map) => {
    console.log("onIdle");
    setZoom(m.getZoom()!);
    setCenter(m.getCenter()!.toJSON());
  };

  return (
    <div style={{ display: "flex", height: "100%" }}>
      <Wrapper apiKey={apiKey!} language={'en'} render={render}>
        <Map
          center={center}
          onClick={onClick}
          onIdle={onIdle}
          zoom={zoom}
          style={{ flexGrow: "1", height: "100%" }}
          onMapLoad={onMapLoad}
        >
          {clicks.map((latLng, i) => (
            <Marker key={i} position={latLng} setLastCoordinates={setLastCoordinates} />
          ))}
        </Map>
      </Wrapper>
    </div>
  );
}

interface MapProps extends google.maps.MapOptions {
  style: { [key: string]: string };
  onClick?: (e: google.maps.MapMouseEvent) => void;
  onIdle?: (map: google.maps.Map) => void;
  children?: React.ReactNode;
  onMapLoad?: (map: google.maps.Map) => void;
}

const Map: React.FC<MapProps> = ({
                                   onClick,
                                   onIdle,
                                   children,
                                   style,
                                   onMapLoad,
                                   ...options
                                 }) => {
  const ref = React.useRef<HTMLDivElement>(null);
  const [map, setMap] = React.useState<google.maps.Map>();

  React.useEffect(() => {
    if (ref.current && !map) {
      const initializedMap = new window.google.maps.Map(ref.current, {
        mapTypeId: google.maps.MapTypeId.HYBRID,
        streetViewControl: false
      });

      setMap(initializedMap);
      if (onMapLoad) {
        onMapLoad(initializedMap);
      }
    }
  }, [ref, map, options, onMapLoad]);

  // because React does not do deep comparisons, a custom hook is used
  // see discussion in https://github.com/googlemaps/js-samples/issues/946
  useDeepCompareEffectForMaps(() => {
    if (map) {
      map.setOptions(options);
    }
  }, [map, options]);

  React.useEffect(() => {
    if (map) {
      ["click", "idle"].forEach((eventName) =>
        google.maps.event.clearListeners(map, eventName)
      );

      if (onClick) {
        map.addListener("click", onClick);
      }

      if (onIdle) {
        map.addListener("idle", () => onIdle(map));
      }
    }
  }, [map, onClick, onIdle]);

  return (
    <>
      <div ref={ref} style={style} />
      {React.Children.map(children, (child) => {
        if (React.isValidElement(child)) {
          // set the map prop on the child component
          // @ts-ignore
          return React.cloneElement(child, { map });
        }
      })}
    </>
  );
};

interface MarkerProps extends google.maps.MarkerOptions {
  setLastCoordinates: React.Dispatch<React.SetStateAction<google.maps.LatLngLiteral | null>>;
}

const Marker: React.FC<MarkerProps> = ({ setLastCoordinates, ...options }) => {
  const [marker, setMarker] = React.useState<google.maps.Marker>();

  React.useEffect(() => {
    if (!marker) {
      const newMarker = new google.maps.Marker();
      setMarker(newMarker);

      // Додаємо слухач події click для маркера
      newMarker.addListener('click', () => {
        const position = newMarker.getPosition();
        if (position) {
          setLastCoordinates({ lat: position.lat(), lng: position.lng() });
        }
      });
    }

    return () => {
      if (marker) {
        marker.setMap(null);
      }
    };
  }, [marker, setLastCoordinates]);

  React.useEffect(() => {
    if (marker) {
      marker.setOptions(options);
    }
  }, [marker, options]);

  return null;
};


const deepCompareEqualsForMaps = createCustomEqual(
  (deepEqual) => (a: any, b: any) => {
    if (
      isLatLngLiteral(a) ||
      a instanceof google.maps.LatLng ||
      isLatLngLiteral(b) ||
      b instanceof google.maps.LatLng
    ) {
      return new google.maps.LatLng(a).equals(new google.maps.LatLng(b));
    }

    return deepEqual(a, b);
  }
);

function useDeepCompareMemoize(value: any) {
  const ref = React.useRef();

  if (!deepCompareEqualsForMaps(value, ref.current)) {
    ref.current = value;
  }

  return ref.current;
}

function useDeepCompareEffectForMaps(
  callback: React.EffectCallback,
  dependencies: any[]
) {
  React.useEffect(callback, dependencies.map(useDeepCompareMemoize));
}

export default GoogleMapComponent
