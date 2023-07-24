import React, { useState } from 'react';
import {
  useJsApiLoader,
  GoogleMap,
  Autocomplete,
  Marker,
} from '@react-google-maps/api';
import {
  Container,
  Col,
  Row,
  InputGroup,
  Form,
  Button,
  Modal,
  Spinner,
  Accordion,
} from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css';
import { makeRequest } from '../helpers';
import { FilterForm } from '../components/FilterForm';
import { ListingReviews } from '../components/ListingReviews';

const libraries: 'places'[] = ['places'];

type SpaceType =
  | 'indoor-lot'
  | 'outdoor-lot'
  | 'undercover'
  | 'outside'
  | 'carport'
  | 'driveway'
  | 'locked-garage';

type VehicleType =
  | 'hatchback'
  | 'sedan'
  | 'suv'
  | 'ev'
  | 'ute'
  | 'wagon'
  | 'van'
  | 'bike';

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
	username?: string;
	id?: string;
  carspaceid?: string;
}

export const SearchPage = () => {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: 'AIzaSyB4Bsp9jhz4i39NidfXExaaZV89o8jP5To',
    libraries: libraries,
  });
  
  const navigate = useNavigate();

	const [view, setView] = useState("map view");
  const [searchValue, setSearchValue] = useState('Sydney');
  const [mapCentre, setMapCentre] = useState({ lat: -33.8688, lng: 151.2093 });
  const [addressComponents, setAddressComponents] = useState(''); // Contains all of the address components for given coordinates
  const [showList, setShowList] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [carspaces, setCarspaces] = useState({});
  const [listingInfo, setListingInfo] = useState<ListingInfo>({});
  const [modalView, setModalView] = useState("See Reviews")

  const [isExpanded, setIsExpanded] = useState(false);

  const handleExpandClick = () => {
    setIsExpanded(!isExpanded);
  };

  // Retrieves car spaces from the backend every time the mapCentre changes
  React.useEffect(() => {
    // Retrieves car spaces given the postcode
    async function retrieveCarspaces(postcode: string) {
      const body = {
        limit: '10',
        sort: 'false',
        postcode: postcode,
      };
      try {
        const response = await makeRequest(
          '/search/postcode',
          'POST',
          body,
          undefined
        );
        if (response.status !== 200) {
          console.log('There was an error!');
        } else {
          const spaces = response.resp;
          return spaces['Postcode Search Results'];
        }
      } catch (error) {
        console.log(error);
      }
      return 0;
    }

    async function addMarkers() {
      const suburbAndPostcode = await extractSuburb();
      const carspaceResults = await retrieveCarspaces(suburbAndPostcode[1]);
      setCarspaces(carspaceResults);
    }

    addMarkers();
  }, [mapCentre]);

  // Takes the search input and converts it into coordinates - moves the map to these coordinates
  const handleSearch = () => {
    if (!searchValue) return;
    const geocoder = new window.google.maps.Geocoder();
    geocoder.geocode({ address: searchValue }, (results, status) => {
      if (status === 'OK' && results && results.length > 0) {
        const { lat, lng } = results[0].geometry.location;
        setMapCentre({ lat: lat(), lng: lng() });
      } else {
        console.error('Could not find coordinates!', status);
      }
    });
  };

  // Given a location (the current mapCentre lat/lng), extracts the suburb and postcode
  const extractSuburb = async () => {
    const lat = mapCentre.lat;
    const lng = mapCentre.lng;
    let searchedSuburb: string = '';
    let searchedPostcode: string = '';

    try {
      const response = await fetch(
        `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lng}&key=AIzaSyB4Bsp9jhz4i39NidfXExaaZV89o8jP5To`
      );
      const data = await response.json();
      const allComponents = data.results[0].address_components;
      setAddressComponents(data.results[0]);
      for (const component of allComponents) {
        const types = component.types;
        if (types.includes('locality')) searchedSuburb = component.short_name;
        if (types.includes('postal_code'))
          searchedPostcode = component.short_name;
      }
    } catch (error) {
      console.error('Error retrieving information!', error);
    }
    return [searchedSuburb, searchedPostcode];
  };

  const handleShowModal = (carspace: any) => {
    let carspaceToView = null;

    for (const key in carspaces) {
			if (carspaces.hasOwnProperty(key)) {
				const listing = carspaces[key];
				if (listing._id === carspace) {
					carspaceToView = listing;
          console.log(carspaceToView)
					break;
				}
			}
		}

		setListingInfo({...listingInfo, 
			username: carspaceToView.username,
			address: carspaceToView.address,
			accessKey: carspaceToView.accesskeyrequired,
			width: carspaceToView.width,
			length: carspaceToView.breadth,
			spaceType: carspaceToView.spacetype,
			vehicleType: carspaceToView.vehiclesize,
			price: carspaceToView.price,
			suburb: carspaceToView.suburb,
			postcode: carspaceToView.postcode,
			id: carspaceToView._id,
      photo: carspaceToView.image,
      carspaceid: carspaceToView.carspaceid
		})
		setShowModal(true);
	}


  const handleCloseModal = () => setShowModal(false);

  // For debugging
  // const print = () => {
  // 	console.log(Object.entries(carspaces))
  // 	Object.entries(carspaces).map(([key, value]) => (console.log("value is:", value._id)))
  // }
  
  if (!isLoaded) {
    return (
      <Container className="text-center">
        <br />
        <br />
        <br />
        <Spinner animation="grow" variant="dark" />
      </Container>
    );
  }


  return (
    <Container fluid>
      <br />
      <Row>
        <Autocomplete>
          <InputGroup className="mb-3">
            <InputGroup.Text style={{ width: '50px' }}>🚗</InputGroup.Text>
            <Form.Control
              type="text"
              onBlur={(event) => setSearchValue(event.target.value)}
            />
            <Button variant="primary" onClick={handleSearch}>
              search
            </Button>
            <Button
              variant="secondary"
              onClick={() =>
                setView(view === 'map view' ? 'list view' : 'map view')
              }
            >
              {view === 'map view' ? 'list view' : 'map view'}
            </Button>
          </InputGroup>
        </Autocomplete>
      </Row>
      <Row>
        <FilterForm searchValue={searchValue} mapCentre={mapCentre}/>
      </Row> <br />
      <Row>
        {view === 'map view' ? (
          <div style={{ width: '100%', height: '79vh' }}>
            <GoogleMap
              center={mapCentre}
              zoom={15}
              options={{
                zoomControl: false,
                mapTypeControl: false,
                fullscreenControl: false,
              }}
              mapContainerStyle={{ width: '100%', height: '100%' }}
            >
              {carspaces &&
                Object.entries(carspaces).map(([key, value]: [any, any]) => (
                  <Marker
                    key={value._id}
                    position={{
                      lat: parseFloat(value.latitude),
                      lng: parseFloat(value.longitude),
                    }}
                    onClick={() => handleShowModal(value._id)}
                  />
                ))}
              <Marker position={{ lat: -33.86819, lng: 151.22464 }} />
            </GoogleMap>
          </div>
        ) : (
          <Container>
            {carspaces &&
              Object.entries(carspaces).map(([key, value]: [any, any]) => (
                <>
                  <Row
                    className="align-items-center"
                    onClick={() => handleShowModal(value._id)}
                    style={{
                      border: '1px solid black',
                      borderRadius: '8px',
                      padding: '10px 10px 10px 0px',
                      margin: '0px 5px',
                      cursor: 'pointer',
                    }}
                  >
                    <Col md="auto">
                      <img src={value.image} style={{ width: '150px', height: '150px' }} />
                    </Col>
                    <Col className="text-center">
                      <span style={{ fontSize: '35pt' }}>${value.price}</span>{' '}
                      <br />
                      <span>
                        <i>per day</i>
                      </span>
                    </Col>
                    <Col>
                      <span style={{ fontSize: '20pt' }}>
                        📍 {value.suburb}
                      </span>{' '}
                      <br />
                      <span style={{ fontSize: '20pt' }}>
                        📏 {value.width} m by {value.breadth} m
                      </span>
                      <br />
                      <span style={{ fontSize: '20pt' }}>
                        🚗{' '}
                        {value.vehiclesize.replace(/^\w/, (c: string) =>
                          c.toUpperCase()
                        )}
                      </span>
                    </Col>
                  </Row>
                  <br />
                </>
              ))}
          </Container>
        )}
      </Row>

      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Carspace in {listingInfo.suburb}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          { modalView === "See Reviews"
            ? <>
            <Row className="align-items-center">
              <Col className="text-center">
                <img src={listingInfo.photo} style={{ width: '200px', height: '200px' }} />
              </Col>
              <Col className="text-center">
                <span className="text-center" style={{ fontSize: '45pt' }}>
                  ${listingInfo.price}
                </span>
                <br />
                <span>
                  <i>per day</i>
                </span>
              </Col>
            </Row>
            <br />
            <Row className="text-center">
              <span>📍 {listingInfo.address}</span>
              <br />
              <br />
              <hr />
              <span>
                This carspace is{' '}
                <b>
                  {listingInfo.width} m by {listingInfo.length} m
                </b>
                . An access key <b>{listingInfo.accessKey ? 'is' : 'is not'}</b>{' '}
                required. The largest vehicle size this carspace can hold is a{' '}
                <b>{listingInfo.vehicleType}</b>. The carspace is of type{' '}
                <b>{listingInfo.spaceType}</b>.
              </span>
              <br />
              <br />
              <br />
              <br />
              <hr />
              <span>Provided by {listingInfo.username}</span>
            </Row>
            </>
            : <>
              <ListingReviews listing={listingInfo}></ListingReviews>
            </>}
        </Modal.Body>
        <Modal.Footer>
					<Button variant="warning" onClick={() => setModalView(modalView === "See Reviews" ? "Carspace Details" : "See Reviews")}>{modalView === "See Reviews" ? "See Reviews" : "Carspace Details"}</Button>
          <Button variant="primary" onClick={() => navigate(`/booking?id=${listingInfo.id}&postcode=${listingInfo.postcode}`)}>Book</Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};
