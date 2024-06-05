import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import {NotificationProps} from "../views/ui/Notification";
import Notification from "../views/ui/Notification";


interface NotificationContextType {
  showNotification: (options: Omit<NotificationProps, 'open' | 'handleClose'>) => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export const NotificationProvider: React.FC<{children: ReactNode}> = ({ children }) => {
  const [notification, setNotification] = useState<Omit<NotificationProps, 'open' | 'handleClose'> & { open: boolean }>({
    open: false,
    message: '',
    severity: 'info',
    position: { vertical: 'bottom', horizontal: 'left' },
  });

  const showNotification = useCallback((options: Omit<NotificationProps, 'open' | 'handleClose'>) => {
    setNotification({ ...options, open: true });
  }, []);

  const handleClose = useCallback(() => {
    setNotification((prev) => ({ ...prev, open: false }));
  }, []);

  return (
    <NotificationContext.Provider value={{ showNotification }}>
      {children}
      <Notification
        open={notification.open}
        handleClose={handleClose}
        message={notification.message}
        severity={notification.severity}
        position={notification.position}
      />
    </NotificationContext.Provider>
  );
};

export const useNotification = (): NotificationContextType => {
  const context = useContext(NotificationContext);
  if (context === undefined) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }

  return context;
};


