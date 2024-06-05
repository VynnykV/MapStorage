// ** MUI Imports
import Card from '@mui/material/Card'
import Grid from '@mui/material/Grid'
import CardHeader from '@mui/material/CardHeader'
import {useEffect, useState} from "react";
import MapLayerService from "../../api/services/MapLayerService";
import {ListMapLayer} from "../../api/models/ListMapLayer";
import {DataGrid, GridColDef, GridRenderCellParams} from "@mui/x-data-grid";
import Typography from "@mui/material/Typography";
import { Button } from '@mui/material';
import {useNotification} from "../../context/NotificationContext";
import {useRouter} from "next/router";

const MapLayers = () => {
  const [rows, setRows] = useState<ListMapLayer[]>([]);
  const { showNotification } = useNotification();
  const router = useRouter();

  const fetchMapLayers = () => {
    return MapLayerService.listMapLayers()
      .then(response => {
        setRows(response.data);

        return response;
      })
      .catch(() => {
        console.log('Error fetching map layers');
      });
  }

  const handleDeleteMapLayer = (id: number) => {
    MapLayerService.deleteMapLayer(id)
      .then(() => fetchMapLayers())
      .then(() => {
        showNotification({
          message: 'Map Layer was deleted successfully!',
          severity: 'success',
          position: { horizontal: "right", vertical: "top" }
        });
      })
      .catch((error) => {
        showNotification({
          message: 'Error deleting Map Layer!',
          severity: 'error',
          position: { horizontal: "right", vertical: "top" }
        });
        console.error("There was an error deleting the map layer", error);
      });
  }



  const handleViewMapLayer = (id: number) => {
    router.push({
      pathname: '/map',
      query: { mapLayerId: id },
    });
  }

  useEffect(() => {
    fetchMapLayers();
  }, []);

  const columns: GridColDef[] = [
    {
      flex: 0.175,
      minWidth: 120,
      headerName: 'Name',
      field: 'name',
      renderCell: (params: GridRenderCellParams) => (
        <Typography variant='body2' sx={{ color: 'text.primary' }}>
          {params.row.name}
        </Typography>
      )
    },
    {
      flex: 0.175,
      minWidth: 120,
      headerName: 'Import Type',
      field: 'import_type',
      renderCell: (params: GridRenderCellParams) => (
        <Typography variant='body2' sx={{ color: 'text.primary' }}>
          {params.row.import_type}
        </Typography>
      )
    },
    {
      flex: 0.175,
      field: 'actions',
      minWidth: 200,
      headerName: 'Actions',
      headerAlign: 'center',
      renderCell: (params: GridRenderCellParams) => (
        <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
          <Button
            variant='contained'
            color='primary'
            onClick={() => handleViewMapLayer(params.row.id)}
            style={{ marginRight: '10px' }}
          >
            View
          </Button>
          <Button
            variant='contained'
            color='error'
            onClick={() => handleDeleteMapLayer(params.row.id)}
          >
            Delete
          </Button>
        </div>
      )
    }
  ]

  return (
    <Grid container spacing={6}>
      <Grid item xs={12}>
        <Card>
          <CardHeader title='Imported Maps' />
          <div style={{ height: 'auto', maxHeight: 'calc(100vh - 250px)', overflow: 'auto' }}>
            <DataGrid
              autoHeight
              rows={rows}
              columns={columns}
              checkboxSelection={false}
              disableColumnFilter={true}
              disableColumnMenu={true}
              rowSelection={false}
              hideFooter={true}
              style={{ width: '100%' }}
              slotProps={{
                baseButton: {
                  variant: 'outlined'
                }
              }}
            />
          </div>
        </Card>
      </Grid>
    </Grid>
  );
}

export default MapLayers
