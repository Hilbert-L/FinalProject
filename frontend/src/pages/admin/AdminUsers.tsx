import React, { useEffect, useState } from "react";
import MaterialTable from 'material-table';
import { ThemeProvider, createTheme } from "@mui/material";
import { makeRequest } from "../../helpers";
import { Button, Modal } from "react-bootstrap";

type User = {
  id: string;
  firstname: string;
  lastname: string;
  username: string;
  email: string;
  phonenumber: string;
  userSince: string;
  active: boolean;
  admin: boolean;
}

export const AdminUsers = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<User>();
  const [showMakeUserAdminModal, setShowMakeUserAdminModal] = useState(false);
  const [showDeactivateUserModal, setShowDeactivateUserModal] = useState(false);
  const [refresh, setRefresh] = useState(false);

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
          admin: user.isadmin,
        })));
      })
  }, [refresh]);

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
        data={users}
        options={{
          search: true,
          actionsColumnIndex: -1
        }}
        actions={[
          {
            icon: "person",
            tooltip: "Set user's admin status",
            onClick: (_, rowData) => {
              setShowMakeUserAdminModal(true)
              setSelectedUser(rowData as User)
            }
          },
          {
            icon: "edit",
            tooltip: "Set user's active status",
            onClick: (_, rowData) => {
              setShowDeactivateUserModal(true)
              setSelectedUser(rowData as User)
            }
          }
        ]}
      />
      <MakeUserAdminModal
        show={showMakeUserAdminModal}
        onHide={() => setShowMakeUserAdminModal(false)}
        refresh={() => setRefresh(!refresh)}
        user={selectedUser}
      />
      <DeactivateUserModal
        show={showDeactivateUserModal}
        onHide={() => setShowDeactivateUserModal(false)}
        refresh={() => setRefresh(!refresh)}
        user={selectedUser}
      />
    </ThemeProvider>
  );
}

const DeactivateUserModal = ({
  show,
  onHide,
  refresh,
  user,
}: {
  show: boolean;
  onHide: () => void;
  refresh: () => void;
  user?: User;
}) => {
  const handleSubmit = () => {
    const token = localStorage.getItem("adminToken");
    if (!token) return;
    makeRequest(
      `/admin/${user?.active ? "deactivate" : "activate"}_user/${user?.username}`,
      "PUT",
      undefined,
      { token }
    ).then((resp) => {
      if (resp.status === 200) {
        onHide();
        refresh();
      }
    })
  }

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>{`${user?.active ? "Deactivate" : "Reactivate"} '${user?.username}'?`}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        Are you sure you want to {user?.active ? "deactivate" : "reactivate"} user '{user?.username}'?
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Close
        </Button>
        <Button variant={user?.active ? "danger" : "primary"} onClick={handleSubmit}>
          Yes
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

const MakeUserAdminModal = ({
  show,
  onHide,
  user,
  refresh,
}: {
  show: boolean;
  onHide: () => void;
  user?: User;
  refresh: () => void;
}) => {
  const handleSubmit = () => {
    const token = localStorage.getItem("adminToken");
    if (!token) return;
    makeRequest(
      `/admin/${user?.admin ? "removeuserfromadmin" : "setuserasadmin"}/${user?.username}`,
      "PUT",
      undefined,
      { token }
    ).then((resp) => {
      if (resp.status === 200) {
        onHide();
        refresh();
      }
    })
  }

  const title = user?.admin
    ? `Remove ${user?.username}'s admin privileges?`
    : `Make ${user?.username} an admin?`

  const body = user?.admin
    ? `Are you sure you want to remove ${user?.username}'s admin privileges?`
    : `Are you sure you want to give ${user?.username} admin privileges?`

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
          <Modal.Title>{title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{body}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={onHide}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSubmit}>
            Yes
          </Button>
        </Modal.Footer>
    </Modal>
  );
}