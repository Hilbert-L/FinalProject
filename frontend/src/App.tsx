import { PropsWithChildren } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { Register } from './pages/Register';
import { Login } from './pages/Login';
import { Layout } from './pages/Layout';
import { MyProfile } from './pages/MyProfile';
import { ListingForm } from './pages/ListingForm';
import { SearchPage } from './pages/SearchPage';
import { AdminLogin } from './pages/AdminLogin';
import { Admin } from './pages/Admin';
import { BookingForm } from './pages/BookingForm';

const RequiresAuth = ({children}: PropsWithChildren) => {
  const isLoggedIn = localStorage.getItem("authToken");
  return isLoggedIn ? <>{children}</> : <Navigate to={"/login"} />
}

const RequiresAdmin = ({children}: PropsWithChildren) => {
  const isLoggedIn = localStorage.getItem("adminToken");
  return isLoggedIn ? <>{children}</> : <Navigate to={"/login/admin"} />
}

export const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/login/admin" element={<AdminLogin />} />
        <Route
          path="/admin"
          element={
            <RequiresAdmin>
              <Admin />
            </RequiresAdmin>
          }
        />
        <Route
          path="/"
          element={
            <RequiresAuth>
              <Layout />
            </RequiresAuth>
          }
        >
          <Route path="profile" element={<MyProfile />} />
          <Route path="listingform" element={<ListingForm />} />
          <Route path="" element={<SearchPage />} />
          <Route path="booking" element={<BookingForm />} />
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
