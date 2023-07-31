import React, { useEffect, useState } from 'react';
import { makeRequest } from '../helpers';
import { Button, Col, Container, Row } from 'react-bootstrap';
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
}

export const MyBookings = () => {
    const [bookings, setBookings] = useState<Booking[]>([]);

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
                        duration: booking.duration_hours, // actually in days
                        price: booking.total_price,
                        provider: booking.provider_username,
                    })))
                }
            })
    }, []);

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
          actions={[
            {
              icon: () => <Button>View Listing</Button>,
              tooltip: "View lisiting",
              onClick: () => {
                console.log("fetch listing info");
              }
            }
          ]}
        />
      </ThemeProvider>
    )
}