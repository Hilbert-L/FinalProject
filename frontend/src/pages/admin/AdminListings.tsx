import React, { useEffect, useState } from "react";
import { makeRequest } from "../../helpers";
import { ThemeProvider, createTheme } from "@mui/material";
import MaterialTable from 'material-table';

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
      />
    </ThemeProvider>
  );
}