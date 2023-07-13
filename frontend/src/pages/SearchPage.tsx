import React, { useState } from 'react';
import { useJsApiLoader, GoogleMap, Autocomplete, Marker } from '@react-google-maps/api';
import { Container, Row, InputGroup, Form, Button, Modal, Spinner } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import { makeRequest } from '../helpers';

const libraries: ("places")[] = ['places'];

export const SearchPage = () => {

  const {isLoaded} = useJsApiLoader({
    googleMapsApiKey: 'AIzaSyB4Bsp9jhz4i39NidfXExaaZV89o8jP5To',
    libraries: libraries,
  })

	const [view, setView] = useState("map view");
  const [searchValue, setSearchValue] = useState('Sydney');
  const [mapCentre, setMapCentre] = useState({lat: -33.8688, lng: 151.2093});
	const [addressComponents, setAddressComponents] = useState(''); // Contains all of the address components for given coordinates
  const [showList, setShowList] = useState(false);
	const [showModal, setShowModal] = useState(false);
  const [carspaces, setCarspaces] = useState([{id: 0, lat: 0, lng: 0}]);

	// Retrieves car spaces from the backend every time the mapCentre changes
	React.useEffect(() => {

		// Retrieves car spaces given the postcode
		async function retrieveCarspaces(postcode: string) {
			let body = {
				"limit": "10",
				"sort": "false",
				"postcode": postcode,
			}
			try {
				let response = await makeRequest("/search/postcode", "POST", body, undefined);
				if (response.status !== 200) {
					console.log("There was an error!")
				} else {
					let spaces = response.resp;
					return spaces['Postcode Search Results'];
				}
			} catch (error) {
				console.log(error);
			}
			return 0;
		}

		async function addMarkers() {
			let suburbAndPostcode = await extractSuburb();
			//let carspaceResults = await retrieveCarspaces(suburbAndPostcode[1])
			//setCarspaces(carspaceResults);
			setCarspaces([
				{id: 1, lat: -33.86819, lng: 151.22464},
				{id: 2, lat: -33.87023, lng: 151.22411},
				{id: 3, lat: -33.87071, lng: 151.22299}
			])
			console.log(carspaces);
		};
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
			const response = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lng}&key=AIzaSyB4Bsp9jhz4i39NidfXExaaZV89o8jP5To`);
			const data = await response.json();
			const allComponents = data.results[0].address_components;
			setAddressComponents(data.results[0]);
			for (const component of allComponents) {
				const types = component.types;
				if (types.includes('locality')) searchedSuburb = component.short_name;
				if (types.includes('postal_code')) searchedPostcode = component.short_name;
			}
		} catch (error) {
			console.error('Error retrieving information!', error);
		}
		return [searchedSuburb, searchedPostcode];
	}

	const handleShowModal = (carspace) => {
		console.log(carspace)
		setShowModal(true);
	}

	const handleCloseModal = () => setShowModal(false);

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
    <Container fluid>
			<br />
			<Row>
				<Autocomplete>
					<InputGroup className="mb-3">
						<InputGroup.Text style={{ width: '50px' }}>🚗</InputGroup.Text>
						<Form.Control type="text" onBlur={(event) => setSearchValue(event.target.value)}/>
						<Button variant="primary" onClick={handleSearch}>search</Button>
						<Button variant="secondary" onClick={() => setView(view === "map view" ? "list view" : "map view")}>{view === "map view" ? "list view" : "map view"}</Button>
					</InputGroup>
				</Autocomplete>
			</Row>
			<Row>
				{ view === "map view" ?
					(
						<div style={{width: "100%", height: "85vh"}}>
							<GoogleMap center={mapCentre} zoom={15} options={{zoomControl: false, mapTypeControl: false, fullscreenControl: false}} mapContainerStyle={ {width: '100%', height: '100%'} }>
								{carspaces.map((carspace) => (
									<Marker key={carspace.id} position={{ lat: carspace.lat, lng: carspace.lng }} onClick={() => handleShowModal(carspace.id)} />
								))}
								<Marker position={{ lat: -33.86819, lng: 151.22464 }} />
							</GoogleMap>
						</div>
					) :
					(
						<Container>
							{carspaces.map((carspace) => (
								<Row key={carspace.id}>
									<div>Carspace: {carspace.id} Latitude: {carspace.lat} Longitude: {carspace.lng}</div>
								</Row>
							))}
						</Container>
					)
				}
			</Row>

      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Carspace</Modal.Title>
        </Modal.Header>
        <Modal.Body>Carspace Info</Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={handleCloseModal}>Book</Button>
        </Modal.Footer>
      </Modal>

    </Container>
  )
};
