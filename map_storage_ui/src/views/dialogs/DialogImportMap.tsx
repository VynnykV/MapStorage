// ** React Imports


// ** MUI Imports
import Box from '@mui/material/Box'
import Card from '@mui/material/Card'
import Dialog from '@mui/material/Dialog'
import TextField from '@mui/material/TextField'
import IconButton from '@mui/material/IconButton'
import Typography from '@mui/material/Typography'
import DialogContent from '@mui/material/DialogContent'

// ** Icon Imports
import Icon from 'src/@core/components/icon'
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import FormControlLabel from "@mui/material/FormControlLabel";
import Switch from "@mui/material/Switch";
import {FormControl, FormHelperText} from "@mui/material";
import {Controller, useForm} from "react-hook-form";
import {IMPORT_MODES} from "../../constants/ImportModes";

interface DialogImportMapProps {
  show: boolean;
  setShow: (show: boolean) => void;
  importMode: string;
  handleImportButton: (formData: FormInputs) => void;
}

interface FormInputs {
  layerName: string
  zoomLevel: number
  threshold: number
  nonmaxSuppression: boolean
  loadDistanceM: number
}

const defaultValues = {
  layerName: '',
  zoomLevel: 19,
  threshold: 120,
  nonmaxSuppression: true,
  loadDistanceM: 50
}

const DialogImportMap: React.FC<DialogImportMapProps> = ({ show, setShow, importMode, handleImportButton }) => {
  const {
    control,
    handleSubmit,
    formState: { errors }
  } = useForm<FormInputs>({ defaultValues });

  const onSubmit = (data: FormInputs) => {
    handleImportButton(data);
    setShow(false);
  };

  const isLoadDistanceVisible = () => {
    return importMode === IMPORT_MODES.POLYLINE;
  }

  return (
    <Card>
      <Dialog
        fullWidth
        open={show}
        maxWidth='md'
        scroll='body'
        onClose={() => setShow(false)}
        onBackdropClick={() => setShow(false)}
      >
        <DialogContent
          sx={{
            position: 'relative',
            px: theme => [`${theme.spacing(5)} !important`, `${theme.spacing(15)} !important`],
            py: theme => [`${theme.spacing(8)} !important`, `${theme.spacing(12.5)} !important`]
          }}
        >
          <IconButton
            size='small'
            onClick={() => setShow(false)}
            sx={{ position: 'absolute', right: '1rem', top: '1rem' }}
          >
            <Icon icon='mdi:close'/>
          </IconButton>
          <Box sx={{ mb: 4, textAlign: 'center' }}>
            <Typography variant='h5' sx={{ mb: 3, lineHeight: '2rem' }}>
              Import Map
            </Typography>
          </Box>
          <form onSubmit={handleSubmit(onSubmit)}>
            <Grid container spacing={6}>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <Controller
                    name='layerName'
                    control={control}
                    rules={{ required: true }}
                    render={({ field: { value, onChange } }) => (
                      <TextField
                        value={value}
                        label='Layer Name'
                        onChange={onChange}
                        error={Boolean(errors.layerName)}
                      />
                    )}
                  />
                  {errors.layerName && (
                    <FormHelperText sx={{ color: 'error.main' }} id='layer-name-validation'>
                      This field is required
                    </FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <Controller
                    name='zoomLevel'
                    control={control}
                    rules={{ required: true }}
                    render={({ field: { value, onChange } }) => (
                      <TextField
                        value={value}
                        label='Zoom Level'
                        onChange={onChange}
                        error={Boolean(errors.zoomLevel)}
                      />
                    )}
                  />
                  {errors.zoomLevel && (
                    <FormHelperText sx={{ color: 'error.main' }} id='zoom-level-validation'>
                      This field is required
                    </FormHelperText>
                  )}
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <Controller
                    name='threshold'
                    control={control}
                    rules={{ required: true }}
                    render={({ field: { value, onChange } }) => (
                      <TextField
                        value={value}
                        label='Threshold'
                        onChange={onChange}
                        error={Boolean(errors.threshold)}
                      />
                    )}
                  />
                  {errors.threshold && (
                    <FormHelperText sx={{ color: 'error.main' }} id='threshold-validation'>
                      This field is required
                    </FormHelperText>
                  )}
                </FormControl>
              </Grid>
              {isLoadDistanceVisible() && (
                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <Controller
                      name='loadDistanceM'
                      control={control}
                      rules={{ required: true }}
                      render={({ field: { value, onChange } }) => (
                        <TextField
                          value={value}
                          label='Load Distance'
                          onChange={onChange}
                          error={Boolean(errors.loadDistanceM)}
                        />
                      )}
                    />
                    {errors.loadDistanceM && (
                      <FormHelperText sx={{ color: 'error.main' }} id='load-distance-m-validation'>
                        This field is required
                      </FormHelperText>
                    )}
                  </FormControl>
                </Grid>
              )}
              <Grid item xs={12}>
                <Controller
                  name="nonmaxSuppression"
                  control={control}
                  render={({ field: { onChange, value } }) => (
                    <FormControlLabel
                      control={
                        <Switch
                          checked={value}
                          onChange={onChange}
                          name="nonmaxSuppression"
                        />
                      }
                      label='Non-maximum suppression'
                    />
                  )}
                />
              </Grid>
            </Grid>
            <DialogActions
              sx={{
                justifyContent: 'right',
                px: theme => [`${theme.spacing(5)} !important`, `${theme.spacing(0)} !important`],
                pb: theme => [`${theme.spacing(8)} !important`, `${theme.spacing(0)} !important`]
              }}
            >
              <Button variant='outlined' color='secondary' onClick={() => setShow(false)}>
                Discard
              </Button>
              <Button type="submit" variant='contained' sx={{ mr: 2 }}>
                Import
              </Button>
            </DialogActions>
          </form>
        </DialogContent>
      </Dialog>
    </Card>
  );
};

export default DialogImportMap;
