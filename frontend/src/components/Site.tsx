import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

import { AddressPage } from "../pages/AddressPage";
import { AdminLogin } from "../pages/AdminLogin";
import { AdminPortal } from "../pages/AdminPortal";
import { Checkout } from "../pages/Checkout";
import { CreateListings } from "../pages/CreateListings";
import { UserLogin } from "../pages/UserLogin";
import { NotFound } from "../pages/NotFound";
import { SearchResults } from "../pages/SearchResults";
import { UserProfile } from "../pages/UserProfile";
import { UserRegistration } from "../pages/UserRegistration";
import { UserSearch } from "../pages/UserSearch";

export const Site = () => {
    const [token, setToken] = React.useState<string>('');

    React.useEffect(() => {
        const lsToken = localStorage.getItem('token');
        if (lsToken) {
            setToken(lsToken)
        }
    }, [])

    return (
        <div>
            {!token && (
                <Link to="/login">Login</Link>
            )}
            <BrowserRouter>
                <Routes>
                    <Route path="/admin/portal" element={<AdminPortal />} />
                    <Route path="/admin" element={<AdminLogin />} />
                    <Route path="/addresspage/:id/checkout" element={<Checkout />} />
                    <Route path="/addresspage/:id" element={<AddressPage />} />
                    <Route path="/createlisting" element={<CreateListings />} />
                    <Route path="/searchresults" element={<SearchResults />} />
                    <Route path="/userprofile" element={<UserProfile />} />
                    <Route path="/registration" element={<UserRegistration />} />
                    <Route path="/login" element={<UserLogin />} />
                    <Route path="/search" element={<UserSearch />} />
                    <Route path="*" element={<NotFound />} />
                </Routes>
            </BrowserRouter>
        </div>
    );
};
