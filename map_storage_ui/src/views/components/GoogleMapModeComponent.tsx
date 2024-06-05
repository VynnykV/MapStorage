import {Card, FormControl, Grid, InputAdornment, InputLabel, Select, TextField} from '@mui/material';
import React from 'react';
import {Icon} from "@iconify/react";
import CardHeader from "@mui/material/CardHeader";
import CardContent from "@mui/material/CardContent";
import MenuItem from "@mui/material/MenuItem";
import {IMPORT_MODES} from "../../constants/ImportModes";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";

interface GoogleMapModeComponentProps {
  clicks: google.maps.LatLng[];
  setClicks: React.Dispatch<React.SetStateAction<google.maps.LatLng[]>>;
  zoom: number;
  setZoom: React.Dispatch<React.SetStateAction<number>>;
  lastCoordinates: google.maps.LatLngLiteral | null;
  importMode: string;
  setImportMode: React.Dispatch<React.SetStateAction<string>>;
  handleImportButton: () => void;
  handleOptimizeButton: () => void;
  handlePreviewButton: () => void;
  handleClearCoordinatesButton: () => void;
  isReadonly: boolean;
}

const GoogleMapModeComponent: React.FC<GoogleMapModeComponentProps> =
  ({ zoom, setZoom,
     clicks,
     lastCoordinates,
     importMode, setImportMode,
     handleImportButton, handleOptimizeButton, handlePreviewButton, handleClearCoordinatesButton,
     isReadonly}) => {

  const handleChangeImportMode = (event: { target: { value: React.SetStateAction<string>; }; }) => {
    setImportMode(event.target.value);
    handleClearCoordinatesButton();
  }

  const clearCoordinates = () => {
    handleClearCoordinatesButton();
  }

  return (
    <Card sx={{height: '100%'}}>
      <CardHeader
        title="Import Settings"
        sx={{
          minHeight: '100px', // Встановіть мінімальну висоту хедера
          alignItems: 'center', // Вирівняйте елементи вертикально
          '& .MuiCardHeader-action': {
            alignSelf: 'center', // Вирівняйте дію (кнопку) вертикально по центру
          },
        }}
        action={
          clicks.length >= 2 && (
            <Button
              variant="contained"
              color="success"
              sx={{
                visibility: clicks.length >= 2 && !isReadonly ? 'visible' : 'hidden'
              }}
              onClick={handleImportButton}
            >
              Import
            </Button>
          )
        }
      />
      <CardContent>
        <form onSubmit={e => e.preventDefault()}>
          <Grid container spacing={5}>
            <Grid item xs={12}>
              <FormControl fullWidth={true}>
                <InputLabel id='import-mode-label'>Import Mode</InputLabel>
                <Select
                  label='Import Mode'
                  defaultValue={IMPORT_MODES.RECTANGLE}
                  value={importMode}
                  id='import-mode-select'
                  labelId='import-mode-label'
                  onChange={handleChangeImportMode}
                  readOnly={isReadonly}
                >
                  <MenuItem value={IMPORT_MODES.RECTANGLE}>Rectangle</MenuItem>
                  <MenuItem value={IMPORT_MODES.POLYLINE}>Polyline</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label='Zoom'
                value={zoom}
                onChange={(event) => setZoom(Number(event.target.value))}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position='start'>
                      <Icon icon='mdi:magnify' />
                    </InputAdornment>
                  ),
                  readOnly: true
                }}
              />
            </Grid>
            {!isReadonly && (
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label='Latitude'
                  value={lastCoordinates ? lastCoordinates.lat.toFixed(6) : ""}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position='start'>
                        <Icon icon='mdi:latitude' />
                      </InputAdornment>
                    ),
                    readOnly: true
                  }}
                />
              </Grid>
            )}
            {!isReadonly && (
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label='Longitude'
                  value={lastCoordinates ? lastCoordinates.lng.toFixed(6) : ""}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position='start'>
                        <Icon icon='mdi:longitude' />
                      </InputAdornment>
                    ),
                    readOnly: true
                  }}
                />
              </Grid>
            )}
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', width: '100%', flexWrap: 'wrap' }}>
                {clicks.length > 1 && !isReadonly && (
                  <Button
                    variant="outlined"
                    color="primary"
                    onClick={handlePreviewButton}
                    sx={{ marginRight: '8px', flexGrow: 1, marginBottom: 2 }}
                  >
                    Preview
                  </Button>
                )}
                {clicks.length > 0 && !isReadonly && (
                  <Button
                    variant="outlined"
                    color="error"
                    onClick={clearCoordinates}
                    sx={{ flexGrow: 1, marginBottom: 2 }}
                  >
                    Clear coordinates
                  </Button>
                )}
                {clicks.length > 1 && !isReadonly && importMode !== IMPORT_MODES.RECTANGLE &&  (
                  <Button
                    variant="outlined"
                    color="success"
                    onClick={handleOptimizeButton}
                    sx={{ flexGrow: 1, width: '100%' }}
                  >
                    Optimize
                  </Button>
                )}
              </Box>
            </Grid>
          </Grid>
        </form>
      </CardContent>
    </Card>
  );
};

export default GoogleMapModeComponent;
