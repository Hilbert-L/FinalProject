import { useEffect, useState } from "react";
import { makeRequest } from "../../helpers";
import { ThemeProvider, createTheme } from "@mui/material";
import MaterialTable from 'material-table';
import { Button, Modal } from "react-bootstrap";

type Listing = {
  id: string;
  price: string;
  address: string;
  lister: string;
  vehiclesize: string;
  spacetype: string;
  width: number;
  length: number;
}

export const AdminListings = () => {
  const [listings, setListings] = useState<Listing[]>([]);
  const [showDeleteListingModal, setShowDeleteListingModal] = useState(false);
  const [selectedListing, setSelectedListing] = useState<Listing>();
  const [refresh, setRefresh] = useState(false);


  useEffect(() => {
    const token = localStorage.getItem("adminToken");
    if (!token) return;
    makeRequest("/carspace", "GET", undefined, { token })
      .then((response) => {
        setListings(response.resp.car_spaces.map((listing: any) => ({
          id: listing.carspaceid ?? listing.CarSpaceId,
          price: listing.price ?? listing.Price,
          address: listing.address ?? listing.Address,
          lister: listing.username ?? listing.UserName,
          vehiclesize: listing.vehiclesize ?? listing.VehicleSize,
          spacetype: listing.spacetype ?? listing.SpaceType,
          width: listing.width ?? listing.Width,
          length: listing.breadth ?? listing.Breadth
        })))
      })
  }, []);

  const theme = createTheme()

  return (
    <ThemeProvider theme={theme}>
      <MaterialTable
        title="Listings"
        columns={[
          { title: "Listing ID", field: "id"},
          { title: "Price per day", field: "price" },
          { title: "Address", field: "address" },
          { title: "Lister", field: "lister" },
          { title: "Max vehicle size allowed", field: "vehiclesize" },
          { title: "Space type", field: "spacetype" },
          { title: "Width", field: "width", type: "numeric" },
          { title: "Length", field: "length", type: "numeric" },
        ]}
        data={listings}
        options={{
          search: true,
          actionsColumnIndex: -1
        }}
        actions={[
          {
            icon: "delete",
            tooltip: "Delete listing",
            onClick: (_, rowData) => {
              setShowDeleteListingModal(true);
              setSelectedListing(rowData as Listing);
            }
          }
        ]}
      />
    <DeleteListingModal
      show={showDeleteListingModal}
      onHide={() => setShowDeleteListingModal(false)}
      refresh={() => setRefresh(!refresh)}
      listing={selectedListing}
    />
    </ThemeProvider>
  );
}

const DeleteListingModal = ({
  show,
  onHide,
  refresh,
  listing,
}: {
  show: boolean;
  onHide: () => void;
  refresh: () => void;
  listing?: Listing;
}) => {
  const handleSubmit = () => {
    const token = localStorage.getItem("adminToken");
    if (!token) return;
    makeRequest(
      `/admin/carspace/deletecarspace/${listing?.lister}/${listing?.id}`,
      "DELETE",
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
        <Modal.Title>Delete this listing</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        Are you sure you want to delete listing {listing?.id}? This CANNOT be undone.
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Close
        </Button>
        <Button variant="danger" onClick={handleSubmit}>
          Yes
        </Button>
      </Modal.Footer>
    </Modal>
  );
}