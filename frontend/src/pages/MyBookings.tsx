import React, { useEffect, useState } from 'react';
import { makeRequest } from '../helpers';
import { ReviewComponent } from '../components/ReviewComponent'; 
import { Button, Modal } from 'react-bootstrap';
import { ThemeProvider, createTheme } from '@mui/material';
import MaterialTable from 'material-table';
import dayjs from 'dayjs';

type Booking = {
    id: string;
    startDate: string;
    endDate: string;
    duration: number;
    price: number;
    provider: string;
    carspaceid: string;
}

export const MyBookings = () => {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [showCancelModal, setCancelListingModal] = useState(false);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [selectedBooking, setSelectedBooking] = useState<Booking>();
  const [refresh, setRefresh] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("authToken");
    const username = localStorage.getItem("username");
    if (!token || !username) return;
    makeRequest(`/booking/history/${username}`, "GET", undefined, { token })
      .then((resp) => {
        if (resp.status === 200) {
          const data = resp.resp["Booking History"];
          setBookings(data.map((booking: any) => ({
            id: booking.booking_id,
            startDate: dayjs(booking.start_date).format("YYYY-MM-DD"),
            endDate: dayjs(booking.end_date).format("YYYY-MM-DD"),
            duration: booking.duration_hours || booking.duration_days,
            price: booking.total_price,
            provider: booking.provider_username,
            carspaceid: booking.carspaceid,
          })))
        }
      })
  }, [refresh]);

  const theme = createTheme()

  return (
    <ThemeProvider theme={theme}>
      <MaterialTable
        title="My Bookings"
        columns={[
          { title: "Booking ID", field: "id", type: "numeric" },
          { title: "Provider", field: "provider" },
          { title: "Start Date", field: "startDate" },
          { title: "End Date", field: "endDate" },
          { title: "Duration (days)", field: "duration" },
          { title: "Price", field: "price" },
        ]}
        data={bookings}
        options={{
          search: false,
        }}
        // Displays the leave review and cancel booking buttons
        actions={[
          {
            icon: () => <Button variant="warning">Review</Button>,
            tooltip: "Leave a review",
            onClick: (_, rowData) => {
              setShowReviewModal(true);
              setSelectedBooking(rowData as Booking)
            }
          },
          {
            icon: () => <Button variant="danger">Cancel Booking</Button>,
            tooltip: "View lisiting",
            onClick: (_, rowData) => {
              setCancelListingModal(true);
              setSelectedBooking(rowData as Booking)
            }
          }
        ]}
      />
      <CancelListingModal
        show={showCancelModal}
        onHide={() => setCancelListingModal(false)}
        booking={selectedBooking}
        refresh={() => setRefresh(!refresh)}
      />
      <Modal show={showReviewModal} onHide={() => setShowReviewModal(false)}>
        <Modal.Header>
          <Modal.Title>leave a review 📝</Modal.Title>
        </Modal.Header>
        <ReviewComponent provider={selectedBooking?.provider} listing={selectedBooking?.carspaceid} token={localStorage.getItem("authToken")} onClose={() => setShowReviewModal(false)}></ReviewComponent>
      </Modal>
    </ThemeProvider>
  )
}

const CancelListingModal = ({ show, onHide, booking, refresh }: {
  show: boolean;
  onHide: () => void;
  booking?: Booking;
  refresh: () => void;
}) => {
  const [success, setSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleCancel = () => {
    const token = localStorage.getItem("authToken");
    const username = localStorage.getItem("username");
    if (!token || !username) return;
    makeRequest(`/booking/delete_booking/${booking?.id}`, "DELETE", undefined, { token })
      .then((resp) => {
        if (resp.status === 200) {
          setSuccess(true)
        } else {
          setErrorMessage(resp.resp.detail)
        }
      })
  }

  const handleHideSuccess = () => {
    setSuccess(false)
    onHide()
    refresh()
  }

  const handleHideError = () => {
    setErrorMessage("")
    onHide()
  }

  const old = dayjs().isAfter(dayjs(booking?.startDate))

  return (
    old
      ? (
        <Modal show={old && show} onHide={onHide}>
          <Modal.Header>
            <Modal.Title>Unable to cancel</Modal.Title>
          </Modal.Header>
          <Modal.Body>This booking is in the past, so cannot be cancelled</Modal.Body>
          <Modal.Footer>
            <Button onClick={onHide}>OK</Button>
          </Modal.Footer>
        </Modal>
      )
      : (
      <>
        <Modal show={show} onHide={onHide} >
          <Modal.Header>
            <Modal.Title>Cancel Booking</Modal.Title>
          </Modal.Header>
          <Modal.Body>Are you sure you want to cancel this booking?</Modal.Body>
          <Modal.Footer>
            <Button variant="danger" onClick={handleCancel}>Yes</Button>
            <Button onClick={onHide}>No</Button>
          </Modal.Footer>
        </Modal>
        <Modal show={success} onHide={handleHideSuccess} >
          <Modal.Header>
            <Modal.Title>Successfully cancelled booking</Modal.Title>
          </Modal.Header>
          <Modal.Body>Success!</Modal.Body>
          <Modal.Footer>
            <Button variant="danger" onClick={handleHideSuccess}>OK</Button>
          </Modal.Footer>
        </Modal>
        <Modal show={!!errorMessage} onHide={handleHideError}>
          <Modal.Header>
            <Modal.Title>Unable to cancel booking</Modal.Title>
          </Modal.Header>
          <Modal.Body>{errorMessage}</Modal.Body>
          <Modal.Footer>
            <Button variant="danger" onClick={handleHideError}>OK</Button>
          </Modal.Footer>
        </Modal>
      </>
    )
  )
}