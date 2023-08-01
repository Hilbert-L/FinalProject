import React, { useState, useEffect } from 'react';
import { makeRequest } from '../helpers';
import { StarRating } from './StarRating';
import {
    Container,
    Col,
    Row,
    Spinner,
  } from 'react-bootstrap';

export const ListingReviews = (props: any) => {
    //console.log(props.listing)
    let token = localStorage.getItem('authToken') || '';
    const listing = props.listing;
    const [isLoaded, setIsLoaded] = useState(false);
    const [reviews, setReviews] = useState("");

    useEffect(() => {
        // Retrieves carspace reviews
        async function retrieveReviews() {
            try {
                let response = await makeRequest(`/carspace/reviews/get_car_space_reviews_for_producer_by_carspaceid/${listing.username}/${listing.carspaceid}`, "GET", undefined, { token });
                if (response.status !== 200) {
                    console.log("There was an error!")
                } else {
                    let reviews = response.resp;
                    setReviews(reviews[`Reviews received by user: ${listing.username} and carspace: ${listing.carspaceid}`]);
                    console.log(reviews[`Reviews received by user: ${listing.username} and carspace: ${listing.carspaceid}`]);
                    setIsLoaded(true);
                }
            } catch (error) {
                console.log(error);
            }
            return 0;
        }
        retrieveReviews();
    }, [])
    

    if (!isLoaded) {
        return (
          <Container className="text-center">
            <br />
            <Spinner animation="grow" variant="dark" />
            <br />
            <br />
          </Container>
        );
      }
    
    return (
        <div style={{ overflowY: 'scroll', maxHeight: '400px' }}>
            {Object.entries(reviews).map(([key, value]: [any, any]) => (
                <>
                    <Container style={{ padding: '10px 15px' }}>
                        <Row>
                            <span><b>{value.reviewerusername}</b> says <i>"{value.writtenfeedback}"</i></span>
                        </Row><hr />
                        <Row>
                            <Col>
                                🫧 Cleanliness<br />
                                💬 Communication<br />
                                ✅ Ease of Access<br />
                                🗺️ Location<br />
                                🟰 Overall
                            </Col>
                            <Col>
                                <StarRating stars={value.cleanliness} />
                                <StarRating stars={value.communication} />
                                <StarRating stars={value.easeofaccess} />
                                <StarRating stars={value.location} />
                                <StarRating stars={value.overall} />
                            </Col>
                        </Row>
                    </Container><br />
                </>
            ))}
        </div>
    )
}