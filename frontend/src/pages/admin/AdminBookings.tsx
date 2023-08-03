import React, { useEffect, useState } from "react";
import { makeRequest } from "../../helpers";
import { ThemeProvider, createTheme } from "@mui/material";
import MaterialTable from "material-table";
import dayjs from "dayjs";

type Bookings = {
  id: string;
  startDate: string;
  endDate: string;
  duration: number;
  price: number;
  provider: string;
  consumer: string;
}

export const AdminBookings = () => {
  const [bookings, setBookings] = useState<Bookings[]>([]);

  useEffect(() => {
    const token = localStorage.getItem("adminToken");
    if (!token) return;
    makeRequest("/admin/Bookings/get_all_bookings", "GET", undefined, { token })
      .then((resp) => {
        setBookings(resp.resp["All Bookings"].map((booking: any) => ({
          id: booking.booking_id,
          startDate: dayjs(booking.start_date).format("YYYY-MM-DD"),
          endDate: dayjs(booking.end_date).format("YYYY-MM-DD"),
          duration: booking.duration_hours || booking.duration_days,
          price: booking.total_price,
          provider: booking.provider_username,
          consumer: booking.consumer_username,
        })));
      })
  }, []);

  const theme = createTheme()

  return (
    <ThemeProvider theme={theme}>
      <MaterialTable
        title="Bookings"
        columns={[
          { title: "Booking ID", field: "id", type: "numeric" },
          { title: "Provider", field: "provider" },
          { title: "Consumer", field: "consumer" },
          { title: "Start Date", field: "startDate" },
          { title: "End Date", field: "endDate" },
          { title: "Duration (days)", field: "duration" },
          { title: "Price", field: "price" },
        ]}
        data={bookings}
        options={{
          search: true,
          actionsColumnIndex: -1
        }}
      />
    </ThemeProvider>
  );
}