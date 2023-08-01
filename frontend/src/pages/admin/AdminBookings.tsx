import React, { useEffect, useState } from "react";
import { makeRequest } from "../../helpers";
import { ThemeProvider, createTheme } from "@mui/material";
import MaterialTable from "material-table";

type Bookings = {
  id: string;
}

export const AdminBookings = () => {
  const [bookings, setBookings] = useState<Bookings[]>([]);

  useEffect(() => {
    const token = localStorage.getItem("adminToken");
    if (!token) return;
    makeRequest("/booking/history", "GET", undefined, { token })
      .then((response) => {
        setBookings(response.resp.users.map((user: any) => ({
          id: user.userid ?? user.userId,
          firstname: user.firstname,
          lastname: user.lastname,
          username: user.username,
          email: user.email,
          phonenumber: user.phonenumber,
          active: user.isactive,
          admin: user.isadmin,
        })));
      })
  }, []);

  const theme = createTheme()

  return (
    <ThemeProvider theme={theme}>
      <MaterialTable
        title="Users"
        columns={[
          { title: "User ID", field: "id"},
          { title: "First name", field: "firstname" },
          { title: "Last name", field: "lastname" },
          { title: "Username", field: "username" },
          { title: "Email", field: "email" },
          { title: "Phone number", field: "phonenumber" },
          { title: "Active", field: "active" },
          { title: "Admin", field: "admin" },
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