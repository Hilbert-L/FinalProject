import React, { useState } from 'react';
import { useJsApiLoader, GoogleMap, Autocomplete, Marker } from '@react-google-maps/api';
import 'bootstrap/dist/css/bootstrap.css';
import axios from 'axios';

const libraries: ("places")[] = ['places'];

export const SearchPage = (props: any) => {

    const container: React.CSSProperties = {
        width: '100%',
        height: 'calc(100vh - 150px)',
        textAlign: 'center',
    }

    const userInput: React.CSSProperties = {
        width: '550px', 
        position: 'absolute', 
        top: '120px', 
        left: 'calc(50% - 275px)',
        zIndex: '10',
        display: 'flex',
        justifyContent: 'center',
    }
    const {isLoaded} = useJsApiLoader({
        googleMapsApiKey: 'AIzaSyB4Bsp9jhz4i39NidfXExaaZV89o8jP5To',
        libraries: libraries,
    })
    const [searchValue, setSearchValue] = useState('Sydney');
    const [mapCenter, setMapCenter] = useState({lat: -33.8688, lng: 151.2093});
  
    // Finds the coordinates of the given location
    const handleSearch = () => {
        if (!searchValue) return;
        const geocoder = new window.google.maps.Geocoder();
        geocoder.geocode({ address: searchValue }, (results, status) => {
            if (status === 'OK' && results && results.length > 0) {
            const { lat, lng } = results[0].geometry.location;
            // Save coordinates in state variable
            setMapCenter({ lat: lat(), lng: lng() });
            } else {
            console.error('Could not find coordinates!', status);
            }
        });
    };

    // VERY MESSY AT THE MOMENT, WILL CLEAN UP
    // Given a location, extracts the suburb and postcode
    async function extractSuburb(address: string) {
        let searchedSuburb: any = null;
        let searchedPostcode: any = null;

        try {
          const response = await axios.get('https://maps.googleapis.com/maps/api/geocode/json', {
            params: {
              address: address,
              key: 'AIzaSyB4Bsp9jhz4i39NidfXExaaZV89o8jP5To',
            },
          });
          const results = response.data.results;
          if (results.length > 0) {
            const addressComponents = results[0].address_components;
            for (const component of addressComponents) {
              const types = component.types;
              if (types.includes('locality')) searchedSuburb = component.short_name;
              if (types.includes('postal_code')) searchedPostcode = component.short_name;
            }
          }
        } catch (error) {
          console.error('Error retrieving information!', error);
        }
        return [searchedSuburb, searchedPostcode];
      }

    React.useEffect(() => {
        // TODO
        // Add markers for all of the search results in this area
        extractSuburb(searchValue)
        .then(result => {
            console.log(result);
            // DO API CALLS HERE WITH THE RESULT (contains suburb and postcode)
        });
        
    }, [mapCenter]);

    if (!isLoaded) {
        return <div>Loading...</div>
    }

    return (
        <div style={container}>
            <Autocomplete>
                <div style={userInput} className="input-group">
                    <span className="input-group-text">🚗</span>
                    <input onBlur={(e) => setSearchValue(e.target.value)} style={{width: '400px', paddingLeft: '10px'}} type="text" placeholder='Enter a suburb or address'/>
                    <button className="btn btn-primary" type="button" id="button-addon2" onClick={handleSearch}>search</button>
                </div>
            </Autocomplete>
            <GoogleMap center={mapCenter} zoom={15} options={{zoomControl: false, mapTypeControl: false, fullscreenControl: false}} mapContainerStyle={ {width: '100%', height: '100%'} }>

            </GoogleMap>
        </div>
    )
}

