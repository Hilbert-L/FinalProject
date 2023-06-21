import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { SearchPage } from "./pages/SearchPage";
import { MyProfile } from "./pages/MyProfile";
import { Layout } from "./pages/Layout";
import { ListingForm } from "./pages/ListingForm";
import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import { PropsWithChildren } from "react";


const RequiresAuth = ({children}: PropsWithChildren) => {
  const auth = localStorage.getItem("authToken");
  const isLoggedIn = auth === "logged-in";
  // to make loggedIn true type the following into console:
  // localStorage.setItem("authToken", "logged-in")
  return isLoggedIn ? <>{children}</> : <Navigate to={"/login"} replace />
}

function App() {
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
        <Route path="/*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
