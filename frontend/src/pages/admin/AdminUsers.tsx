import { useEffect, useState } from "react";
import MaterialTable from 'material-table';
import { ThemeProvider, createTheme } from "@mui/material";
import { makeRequest } from "../../helpers";

type User = {
  id: string;
  firstname: string;
  lastname: string;
  username: string;
  email: string;
  phonenumber: string;
  userSince: string;
  active: boolean;
}

export const AdminUsers = () => {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    const token = localStorage.getItem("adminToken");
    if (!token) return;
    makeRequest("/users", "GET", undefined, { token })
      .then((response) => {
        setUsers(response.resp.users.map((user: any) => ({
          id: user.userid ?? user.userId,
          firstname: user.firstname,
          lastname: user.lastname,
          username: user.username,
          email: user.email,
          phonenumber: user.phonenumber,
          active: user.isactive,
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
        ]}
        data={users}
        options={{
          search: true
        }}
      />
    </ThemeProvider>
  );
}