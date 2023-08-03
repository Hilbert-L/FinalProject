import { useState, useEffect } from 'react';
import { Toast, ToastContainer, ProgressBar } from 'react-bootstrap';

// Used to display a notification on the screen
export const NotificationBox = (props: any) => {
    const [show, setShow] = useState(true);
    const [progress, setProgress] = useState(100);

    useEffect(() => {
        if (show) {
          const interval = setInterval(() => {
            setProgress((progress) => progress - 1);
          }, 50);

          if (progress <= 0) {
            clearInterval(interval);
            setShow(false);
          }
          
    
          return () => clearInterval(interval);
        }
      }, [show, progress]);

    return (
        <ToastContainer className="p-3" position={props.position ? props.position : 'top-end'} style={{ zIndex: 10 }}>
            <Toast show={show}>
                <ProgressBar style={{ height: '8px', margin: '0px 0px', padding: '0px 0px', borderRadius: '3px' }} variant={props.variant ? props.variant : "warning"} now={progress} />
                <Toast.Header closeButton={false}>
                    <strong className="me-auto">{props.title}</strong>
                    <small>just now</small>
                </Toast.Header>
                <Toast.Body>{props.message}</Toast.Body>
            </Toast>
        </ToastContainer>
    )
}