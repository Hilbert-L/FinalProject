import { useEffect, useState } from "react";
import MaterialTable from 'material-table';
import { ThemeProvider, createTheme } from "@mui/material";
import { makeRequest } from "../../helpers";
import { Button, Form, Modal } from "react-bootstrap";

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
  const [selectedUser, setSelectedUser] = useState<User>();
  const [showMakeUserAdminModal, setShowMakeUserAdminModal] = useState(false);
  const [showDeactivateUserModal, setShowDeactivateUserModal] = useState(false);

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
        user={selectedUser}
      />
      <DeactivateUserModal
        show={showDeactivateUserModal}
        onHide={() => setShowDeactivateUserModal(false)}
        user={selectedUser}
      />
    </ThemeProvider>
  );
}

const DeactivateUserModal = ({
  show,
  onHide,
  user,
}: {
  show: boolean;
  onHide: () => void;
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
    ).then((response) => {
      console.log(response);
      onHide();
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
}: {
  show: boolean;
  onHide: () => void;
  user?: User;
}) => {
  const handleSubmit = () => {
    console.log("TODO: how to make a user an admin?")
  }

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
          <Modal.Title>{`Make ${user?.firstname} ${user?.lastname} an admin?`}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Are you sure you want to give {user?.firstname} {user?.lastname} admin privileges?
        </Modal.Body>
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