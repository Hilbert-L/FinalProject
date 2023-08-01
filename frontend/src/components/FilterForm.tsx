import {
  Collapse,
  Card,
  Form,
  Button,
  ToggleButton,
  ToggleButtonGroup,
  Row,
  Container,
  Spinner
} from 'react-bootstrap';

import {
  useJsApiLoader,
  GoogleMap,
  Autocomplete,
  Marker,
} from '@react-google-maps/api';

import React from 'react';
import { makeRequest } from '../helpers';
import { useState } from 'react';

export const FilterForm = (props: any) => {
  
  const [isFilterVisible, setIsFilterVisible] = React.useState(false);
  const [minPrice, setMinPrice] = React.useState('');
  const [maxPrice, setMaxPrice] = React.useState('');
  const [spaceType, setSpaceType] = React.useState('none');
  const [vehicleType, setVehicleType] = React.useState('none');
  const [distanceFromPin, setDistanceFromPin] = React.useState('');
  const [recommenderSystem, setRecommenderSystem] = React.useState('none');
  const [resultLimit, setResultLimit] = React.useState('');
  const [sortMethod, setSortMethod] = React.useState('none');
  const [latitude, setLatitude] = React.useState(0.000000);
  const [longitude, setLongitude] = React.useState(0.000000);
  const [beyondSuburb, setBeyondSuburb] = React.useState("false");
  const [loaded, setLoaded] = React.useState(true)
  const [filteredCarSpaces, setFilteredCarSpaces] = React.useState({});

  React.useEffect(() => {
    const geocoder = new window.google.maps.Geocoder();
    geocoder.geocode({ address: props.searchValue }, (results, status) => {
        console.log(results, status)
      if (status === 'OK' && results && results.length > 0) {
        const { lat, lng } = results[0].geometry.location;
        setLatitude(lat())
        setLongitude(lng())
      } else {
        console.error('Could not find coordinates!', status);
      }
    });
  }, [props.searchValue])

  React.useEffect(() => {
    if (typeof props.onUpdateState === 'function') {
      props.onUpdateState(filteredCarSpaces)
    }
  }, [filteredCarSpaces, props.onUpdateState])


  // Given a location (the current mapCentre lat/lng), extracts the suburb and postcode
  const extractSuburb = async () => {
    let searchedSuburb: string = '';
    let searchedPostcode: string = '';

    try {
      const response = await fetch(
        `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=AIzaSyB4Bsp9jhz4i39NidfXExaaZV89o8jP5To`
      );
      const data = await response.json();
      const allComponents = data.results[0].address_components;
      const addressComponents = data.results[0];
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

  async function handleFilterSubmit(event: any) {
    event.preventDefault();

    if (maxPrice !== '' && minPrice !== '' && maxPrice < minPrice) {
      alert("Max Price is less than min price");
    }

    if (recommenderSystem !== 'none' && sortMethod !== 'none') {
        alert("Cannot have recommender system and sort method both inputed")
        return
    }

    setLoaded(false);

    const suburbAndPostcode = await extractSuburb();

    const body = {
      searchvalue: props.searchValue !== '' ? props.searchValue : null,
      latitude: latitude,
      longitude: longitude,
      minprice: minPrice !== '' ? minPrice : null,
      maxprice: maxPrice !== '' ? maxPrice : null,
      spacetype: spaceType !== 'none' ? spaceType : null,
      vehicletype: vehicleType !== 'none' ? vehicleType : null,
      distancefrompin: distanceFromPin !== '' ? distanceFromPin : 5,
      recommendersystem: recommenderSystem !== 'none' ? recommenderSystem : null,
      resultlimit: resultLimit !== '' ? resultLimit : null,
      sortmethod: sortMethod !== 'none' ? sortMethod : null,
      suburb: suburbAndPostcode[0] !== 'none' ? suburbAndPostcode[0] : null
    };
    if (beyondSuburb === "true") {
      body.suburb = null
    }
    console.log(body);
    const token = localStorage.getItem('authToken') || '';

    try {
        const response = await makeRequest('/search/advancedsearch', 'POST', body, {token})
        if (response.status === 200) {
            console.log(response)
            console.log("Response is valid")
            const spaces = await response.resp;
            setFilteredCarSpaces(spaces["Filtered Car Spaces"])
            
        } else {
            alert("Invalid Response")
        }
    } catch (error) {
      console.log(error);
    }
    console.log(filteredCarSpaces)
    setLoaded(true);
    setIsFilterVisible(!isFilterVisible);
  }

  const handleFilterButtonClick = () => {
    setIsFilterVisible(!isFilterVisible);
  };

  const handleInputChange = (event: any, setState: any) => {
    setState(event.target.value);
  };

  return (
    <div>
      <Button variant="warning" style={{ width: '100%' }} onClick={handleFilterButtonClick}>
        {isFilterVisible ? 'Hide Advanced Search' : 'Advanced Search'}
      </Button>
      {isFilterVisible && (
        <Form>
          <br></br>
          <Form.Group controlId="priceRangeFilter">
            <Form.Label>Price Range:</Form.Label>
            <Form.Control
              type="number"
              placeholder="Min Price"
              value={minPrice}
              onChange={(event) => handleInputChange(event, setMinPrice)}
            />
            <Form.Control
              type="number"
              placeholder="Max Price"
              value={maxPrice}
              onChange={(event) => handleInputChange(event, setMaxPrice)}
            />
          </Form.Group>
          <br></br>
          <Form.Group controlId="CarSpaceType">
            <Form.Label>Car Space Type:</Form.Label>
            <Form.Select
              value={spaceType}
              onChange={(event) => handleInputChange(event, setSpaceType)}
            >
              <option value="none">Space Type</option>
              <option value="indoor-lot">Indoor Lot</option>
              <option value="outdoor-lot">Outdoor Lot</option>
              <option value="undercover">Undercover</option>
              <option value="outside">Outside</option>
              <option value="carport">Carport</option>
              <option value="driveway">Driveway</option>
              <option value="locked-garage">Locked Garage</option>
            </Form.Select>
          </Form.Group>
          <br></br>
          <Form.Group controlId="VehicleType">
            <Form.Label>Vehicle Type:</Form.Label>
            <Form.Select
              value={vehicleType}
              onChange={(event) => handleInputChange(event, setVehicleType)}
            >
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
          </Form.Group>
          <br></br>
          <Form.Group controlId="distanceFromPinFilter">
            <Form.Label>Distance From Pin (Kilometers):</Form.Label>
            <Form.Control
              type="number"
              placeholder="Enter Distance in Kilometers"
              value={distanceFromPin}
              onChange={(event) => handleInputChange(event, setDistanceFromPin)}
            />
          </Form.Group>
          <br></br>
          <Form.Group controlId="resultLimit">
            <Form.Label>Results Limit (Listings):</Form.Label>
            <Form.Control
              type="number"
              placeholder="Result Limit"
              value={resultLimit}
              onChange={(event) => handleInputChange(event, setResultLimit)}
            />
          </Form.Group>
          <br></br>
          <Form.Group controlId="selectRecommenderSystem">
            <Form.Label>Recommender System:</Form.Label>
            <Form.Control
              as="select"
              value={recommenderSystem}
              onChange={(event) =>
                handleInputChange(event, setRecommenderSystem)
              }
            >
              <option value="none">No Recommender System</option>
              <option value="recommender">Use Recommender System</option>
            </Form.Control>
          </Form.Group>
          <br></br>
          <Form.Group controlId="SortMethod">
            <Form.Label>Sort Listings By:</Form.Label>
            <Form.Select
              value={sortMethod}
              onChange={(event) => handleInputChange(event, setSortMethod)}
            >
              <option value="none">No Sorting</option>
              <option value="price-ascending">Price Ascending</option>
              <option value="price-descending">Price Descending</option>
              <option value="distance-from-pin-ascending">Distance from Pin Ascending</option>
              <option value="distance-from-pin-descending">Distance from Pin Descending</option>
            </Form.Select>
          </Form.Group>
          <br></br>
          <Form.Group>
            <Form.Label>Search Beyond Suburb:</Form.Label>
            <Form.Select
              value={beyondSuburb}
              onChange={(event) => handleInputChange(event, setBeyondSuburb)}
            >
              <option value="false">Suburb Only</option>
              <option value="true">Beyond Suburb</option>
            </Form.Select>
          </Form.Group>
          <br></br>
          <Button variant="primary" type="submit" onClick={handleFilterSubmit}>
            Advanced Search
          </Button>
        </Form>)
      }
      {!loaded && (
        <Container className="text-center">
        <br />
        <Spinner animation="grow" variant="dark" />
        <br />
        <br />
        </Container>
      )}
      <br></br>
    </div>
  );
};
