import { Button, Col, FloatingLabel, Form, Row, Container, Spinner } from "react-bootstrap";
import { FormContainer } from "../components/StyledFormContainer";
import { useJsApiLoader, Autocomplete } from '@react-google-maps/api';
import { useState } from "react";
import { makeRequest } from "../helpers";
import { useNavigate } from "react-router-dom";

type SpaceType = 
  | "indoor-lot"
  | "outdoor-lot"
  | "undercover"
  | "outside"
  | "carport"
  | "driveway"
  | "locked-garage"

type VehicleType = 
  | "hatchback"
  | "sedan"
  | "suv"
  | "ev"
  | "ute"
  | "wagon"
  | "van"
  | "bike"

type ListingInfo = {
  address?: string;
  suburb?: string;
  postcode?: string;
  latitude?: string;
  longitude?: string;
  spaceType?: SpaceType;
  vehicleType?: VehicleType;
  accessKey?: boolean;
  length?: number;
  width?: number;
  price?: number;
  photo?: string;
}

const libraries: ("places")[] = ['places'];

export const ListingForm = () => {
  const [info, setInfo] = useState<ListingInfo>({});
  
  const [photo, setPhoto] = useState<string>();

  const [error, setError] = useState<string>();

  const navigate = useNavigate();

  const token = localStorage.getItem("authToken")!;

  const {isLoaded} = useJsApiLoader({
    googleMapsApiKey: 'AIzaSyB4Bsp9jhz4i39NidfXExaaZV89o8jP5To',
    libraries: libraries,
  })

  const handleSubmit = () => {
    console.log(info.latitude);
    console.log(info.longitude);
    // Need to add photo as info to send
    const body = {
      "address": String(info.address),
      "suburb": String(info.suburb),
      "postcode": String(info.postcode),
      "spacetype": String(info.spaceType),
      "vehiclesize": String(info.vehicleType),
      "accesskeyrequired": String(info.accessKey),
      "breadth": String(info.length),
      "width": String(info.width),
      "price": info.price,
      "latitude": String(info.latitude),
      "longitude": String(info.longitude)
    };
    makeRequest("/carspace/create_car_space", "POST", body, { token })
      .then((response) => {
        if (response.status === 200) navigate("/");
        else setError(response.resp.detail);
      })
  }
  const handlePhoto = (event: any) => {
    if (event.target.files) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64 = reader.result as string;
        setPhoto(base64)
      };
      reader.readAsDataURL(event.target.files[0]);
    }
  };

  // Takes the search input and converts it into coordinates
	const findCoordinates = () => {
		if (!info.address) return;
		const geocoder = new window.google.maps.Geocoder();
		geocoder.geocode({ address: info.address }, (results, status) => {
			if (status === 'OK' && results && results.length > 0) {
				const { lat, lng } = results[0].geometry.location;
        setInfo({...info, latitude: lat().toString(), longitude: lng().toString()});
			} else {
				console.error('Could not find coordinates!', status);
			}
		});
	};

  // Given coordinates, extracts suburb and postcode
  const extractSuburb = async () => {
		const lat = info.latitude;
		const lng = info.longitude;
		let searchedSuburb: string = '';
		let searchedPostcode: string = '';

		try {
			const response = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lng}&key=AIzaSyB4Bsp9jhz4i39NidfXExaaZV89o8jP5To`);
			const data = await response.json();
			const allComponents = data.results[0].address_components;
			for (const component of allComponents) {
				const types = component.types;
				if (types.includes('locality')) searchedSuburb = component.short_name;
				if (types.includes('postal_code')) searchedPostcode = component.short_name;
			}
		} catch (error) {
			console.error('Error retrieving information!', error);
		}
		setInfo({...info, suburb: searchedSuburb, postcode: searchedPostcode});;
	}

  const allFilledOut = info.address !== undefined
    && info.spaceType !== undefined
    && info.vehicleType !== undefined
    && info.accessKey !== undefined
    && info.width !== undefined
    && info.length !== undefined
    && info.price !== undefined
    && photo !== undefined
  
  if (!isLoaded) {
    return (
      <Container className="text-center">
        <br />
        <br />
        <br />
        <Spinner animation="grow" variant="dark" />
      </Container>
    )
  }

  return (
    <FormContainer width="500px" top="20px">
      <div style={{ margin: "30px 15px" }}>
        <h1 style={{textAlign: "center"}}>add your car space 🚗</h1>
        <Autocomplete>
          <Form.Group>
            <br />
            <Form.Label>What is the address?</Form.Label>
              <FloatingLabel controlId="floatingAddress" label="Address" className="mb-3">
                <Form.Control
                  type="text"
                  placeholder="Address"
                  onBlur={(event) => setInfo({...info, address: event.target.value})}
                />
              </FloatingLabel>
          </Form.Group>
        </Autocomplete>
        <Form.Group>
          <Form.Label>What type of car space is this?</Form.Label>
          <FloatingLabel controlId="floatingSpaceType" label="Space Type" className="mb-3">
            <Form.Select
              value={info.spaceType}
              onBlur={findCoordinates}
              onChange={
                (event) => setInfo({
                  ...info,
                  spaceType:
                    event.target.value === "none"
                      ? undefined
                      : event.target.value as SpaceType
                })
              }
              >
              <option value="none">Space type</option>
              <option value="indoor-lot">Indoor Lot</option>
              <option value="outdoor-lot">Outdoor Lot</option>
              <option value="undercover">Undercover</option>
              <option value="outside">Outside</option>
              <option value="carport">Carport</option>
              <option value="driveway">Driveway</option>
              <option value="locked-garage">Locked Garage</option>
            </Form.Select>
          </FloatingLabel>
        </Form.Group>
        <Form.Group>
          <Form.Label>What's the largest type of vehicle it can hold?</Form.Label>
          <FloatingLabel controlId="floatingVehicleType" label="Vehicle Type" className="mb-3">
            <Form.Select
              value={info.vehicleType}
              onChange={
                (event) => {console.log(event.target.value); setInfo({
                  ...info,
                  vehicleType:
                    event.target.value === "none"
                      ? undefined
                      : event.target.value as VehicleType
                })}
              }>
              <option value="none">Vehicle type</option>
              <option value="hatchback">Hatchback</option>
              <option value="sedan">Sedan</option>
              <option value="suv">SUV</option>
              <option value="ev">EV</option>
              <option value="ute">Ute</option>
              <option value="wagon">Wagon</option>
              <option value="van">Van</option>
              <option value="bike">Bike</option>
            </Form.Select>
          </FloatingLabel>
        </Form.Group>
        <Form.Group>
          <Form.Label>Is an access key required?</Form.Label>
          <div className="mb-1">
            <Form.Check 
              checked={info.accessKey === true}
              onChange={() => setInfo({...info, accessKey: true})}
              inline
              name="access-key"
              label="Yes"
              type="radio"
              />
            <Form.Check
              checked={info.accessKey === false}
              onChange={() => setInfo({...info, accessKey: false})}
              inline
              name="access-key"
              label="No"
              type="radio"
            />
          </div>
        </Form.Group>
        <Form.Group>
          <br />
          <Form.Label>How big is the car space (in metres)?</Form.Label>
          <Row>
            <Col>
              <FloatingLabel controlId="floatingLength" label="Length (metres)" className="mb-3">
                <Form.Control
                  type="number"
                  placeholder="Length (metres)"
                  value={info.length}
                  onBlur={extractSuburb}
                  onChange={event => setInfo({...info, length: parseInt(event.target.value, 10)})}
                  />
              </FloatingLabel>
            </Col>
            <Col>
              <FloatingLabel controlId="floatingWidth" label="Width (metres)" className="mb-3">
                <Form.Control
                  type="number"
                  placeholder="Width (metres)"
                  value={info.width}
                  onChange={event => setInfo({...info, width: parseInt(event.target.value, 10)})}
                />
              </FloatingLabel>
            </Col>
          </Row>
        </Form.Group>
        <Form.Group>
          <Form.Label>What is the price per day?</Form.Label>
            <FloatingLabel controlId="floatingPrice" label="Price" className="mb-3">
              <Form.Control
                    type="number"
                    value={info.photo}
                    placeholder="Price"
                    onChange={event => setInfo({...info, price: parseInt(event.target.value, 10)})}
                  />
            </FloatingLabel>
        </Form.Group>
        <Form.Group>
          <Form.Label>Please upload a photo of the car space:</Form.Label>
          <Form.Control
                type="file"
                value={info.photo}
                accept="image/*"
                onChange={(event) => handlePhoto(event)}
              />
        </Form.Group>
        {error && <span style={{ color: "#D7504D", fontSize: "14px" }}>{error}</span>}
        <div className="d-grid gap-2" style={{ paddingTop: "10px" }}>
          <Button
            variant="primary"
            size="lg"
            onClick={handleSubmit}
            disabled={!allFilledOut}
          >Add Listing</Button>
        </div>
      </div>
    </FormContainer>
  );
};
