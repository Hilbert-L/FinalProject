import { PropsWithChildren } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { Register } from './pages/Register';
import Login from './pages/Login';
import { Layout } from './pages/Layout';
import { MyProfile } from './pages/MyProfile';
import { ListingForm } from './pages/ListingForm';
import { SearchPage } from './pages/SearchPage';

const RequiresAuth = ({children}: PropsWithChildren) => {
  const auth = localStorage.getItem("authToken");
  const isLoggedIn = auth === "logged-in";
  // to make loggedIn true type the following into console:
  // localStorage.setItem("authToken", "logged-in")
  return isLoggedIn ? <>{children}</> : <Navigate to={"/login"} />
}

export const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <RequiresAuth>
              <Layout />
            </RequiresAuth>
        } >
          <Route path="profile" element={<MyProfile />} />
          <Route path="listingform" element={<ListingForm />} />
          <Route path="" element={<SearchPage />} />
        </Route>
        <Route path="/*" element={
          <RequiresAuth>
            <Navigate to="/" />
          </RequiresAuth>
        } />
      </Routes>
    </BrowserRouter>
  )
}
