import React, { useEffect, useState } from "react";
import MaterialTable from 'material-table';
import { ThemeProvider, createTheme } from "@mui/material";
import { makeRequest } from "../../helpers";
import { Button, Col, Container, Modal, Row } from "react-bootstrap";
import { ListingReviews } from "../../components/ListingReviews";
import { StarRating } from "../../components/StarRating";

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
  const [showViewReviewsModal, setShowViewReviewsModal] = useState(false);
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
          },
          {
            icon: "star",
            tooltip: "View reviews of this user",
            onClick: (_, rowData) => {
              setShowViewReviewsModal(true)
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
      <ViewReviewsModal
        show={showViewReviewsModal}
        onHide={() => setShowViewReviewsModal(false)}
        user={selectedUser}
      />
    </ThemeProvider>
  );
}

type Review = {
  id: string;
  cleanliness: number;
  communication: number;
  easeofaccess: number;
  location: number;
  overall: number;
  reviewer: string;
  feedback: string;
}

const ViewReviewsModal = ({
  show,
  onHide,
  user,
}: {
  show: boolean;
  onHide: () => void;
  user?: User;
}) => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [refresh, setRefresh] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("adminToken");
    if (!token || !user) return;
    makeRequest(`/admin/carspace/getcarspacereviews/${user?.username}`, "GET", undefined, { token })
      .then((resp) => {
        if (resp.status === 200) {
          setReviews(resp.resp[`carspaces for user: ${user?.username}`].map((review: any) => ({
            id: review._id,
            cleanliness: review.cleanliness,
            communication: review.communication,
            easeofaccess: review.easeofaccess,
            location: review.location,
            overall: review.overall,
            reviewer: review.reviewer_username,
            feedback: review.writtenfeedback,
          })));
        }
      })
  }, [user, refresh]);

  const handleDelete = (id: string) => {
    const token = localStorage.getItem("adminToken");
    if (!token) return;
    makeRequest(`/admin/carspacereview/${id}`, "DELETE", undefined, { token })
      .then((resp) => {
        if (resp.status === 200) {
          setRefresh(!refresh)
        }
      })
  }

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>Reviews for {user?.username}</Modal.Header>
      <Modal.Body>
        <div style={{ overflowY: 'scroll', maxHeight: '400px' }}>
          {reviews.map((review) => (
            <Container style={{ padding: '10px 15px' }}>
              <Row>
                  <span><b>{review.reviewer}</b> says <i>"{review.feedback}"</i></span>
              </Row>
              <br />
              <Row>
                <Col>
                  🫧 Cleanliness<br />
                  💬 Communication<br />
                  ✅ Ease of Access<br />
                  🗺️ Location<br />
                  🟰 Overall
                </Col>
                <Col>
                  <StarRating stars={review.cleanliness} />
                  <StarRating stars={review.communication} />
                  <StarRating stars={review.easeofaccess} />
                  <StarRating stars={review.location} />
                  <StarRating stars={review.overall} />
                </Col>
              </Row>
              <br />
              <Row>
                <div>
                  <Button variant="danger" onClick={() => handleDelete(review.id)}>
                    Delete
                  </Button>
                </div>
              </Row>
              <hr />
            </Container>
          ))}
        </div>
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={onHide}>OK</Button>
      </Modal.Footer>
    </Modal>
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