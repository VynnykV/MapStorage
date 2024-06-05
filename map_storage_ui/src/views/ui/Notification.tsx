import React from 'react';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

export interface NotificationProps {
  open: boolean;
  handleClose: () => void;
  message: string;
  severity: 'error' | 'warning' | 'info' | 'success';
  position?: {
    vertical: 'top' | 'bottom';
    horizontal: 'left' | 'center' | 'right';
  };
}

const Notification: React.FC<NotificationProps> = ({
                                                     open,
                                                     handleClose,
                                                     message,
                                                     severity,
                                                     position = { vertical: 'bottom', horizontal: 'left' },
                                                   }) => {
  return (
    <Snackbar
      anchorOrigin={position}
      open={open}
      onClose={handleClose}
      autoHideDuration={6000}
    >
      <Alert onClose={handleClose} severity={severity} variant={"filled"} sx={{ width: '100%' }}>
        {message}
      </Alert>
    </Snackbar>
  );
};

export default Notification;

