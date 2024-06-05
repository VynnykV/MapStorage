import React from 'react';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import {Icon} from "@iconify/react";
import IconButton from '@mui/material/IconButton';

interface GoogleMapCoordinateInputComponentProps {
  handleSearchAction: (coordinates: google.maps.LatLngLiteral | null) => void;
  handleInsertAction: (coordinates: google.maps.LatLngLiteral | null) => void;
}

const GoogleMapCoordinateInputComponent: React.FC<GoogleMapCoordinateInputComponentProps> =
  ({handleSearchAction, handleInsertAction}) => {
    const [isActionsEnabled, setIsActionsEnabled] = React.useState(false);
    const [inputCoordinates, setInputCoordinates] = React.useState<google.maps.LatLngLiteral | null>(null);

    const handleCoordinateInput = (event) => {
      const input = event.target.value;
      const coordsPattern = /^-?\d+(\.\d+)?,\s*-?\d+(\.\d+)?$/;
      const isInputValid = coordsPattern.test(input);
      setIsActionsEnabled(isInputValid);
      if (isInputValid) {
        const [lat, lng] = input.split(',').map(Number);
        setInputCoordinates({lat , lng});
      }
    };

    return (
      <TextField
        type="text"
        variant="outlined"
        placeholder="Enter coordinates..."
        onChange={handleCoordinateInput}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton disabled={!isActionsEnabled} onClick={() => handleSearchAction(inputCoordinates)}>
                <Icon icon='mdi:magnify' color={'red'} />
              </IconButton>
              <IconButton disabled={!isActionsEnabled} onClick={() => handleInsertAction(inputCoordinates)}>
                <Icon icon='mdi:plus' color={'red'} />
              </IconButton>
            </InputAdornment>
          ),
          style: {
            color: 'red'
          },
          sx: {
            '& .MuiInputBase-input::placeholder': {
              color: '#ff5555',
              opacity: 1
            },
          }
        }}
        style={{
          position: 'absolute',
          top: '10px',
          left: '50%',
          transform: 'translateX(-50%)',
          zIndex: 5,
          width: 300
        }}
      />
    );
}

export default GoogleMapCoordinateInputComponent;
